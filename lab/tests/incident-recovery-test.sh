#!/usr/bin/env bash

set -euo pipefail

LAB_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

PROJECT_DIR="$(
    cd "${LAB_DIR}/.."
    pwd
)"

cd "${LAB_DIR}"

COMPOSE=(
    docker compose
    --env-file .env
    -f compose.yaml
)

EVENTS="${PROJECT_DIR}/evidence/runtime/security-events.jsonl"
ALERTS="${PROJECT_DIR}/evidence/runtime/security-alerts.jsonl"
INCIDENTS="${PROJECT_DIR}/evidence/runtime/incidents.jsonl"
ACTIONS="${PROJECT_DIR}/evidence/runtime/containment-actions.jsonl"

echo "============================================================"
echo " PROJECT REDOUBT — PHASE 8 INCIDENT & RECOVERY TEST"
echo "============================================================"


echo
echo "[1] Required services"

for service in \
    detection \
    incident-response \
    finance-db \
    backup-agent \
    recovery-db
do
    id="$("${COMPOSE[@]}" ps -q "${service}")"

    if [[ -z "${id}" ]]; then
        echo "[FAIL] ${service} is not running"
        exit 1
    fi

    echo "[PASS] ${service} running"
done


echo
echo "[2] Incident responder isolation"

INCIDENT_ID="$(
    "${COMPOSE[@]}" ps -q incident-response
)"

MODE="$(
    docker inspect \
        "${INCIDENT_ID}" \
        --format '{{.HostConfig.NetworkMode}}'
)"

if [[ "${MODE}" != "none" ]]; then
    echo "[FAIL] Incident responder network mode: ${MODE}"
    exit 1
fi

echo "[PASS] Incident responder has no Docker network"


echo
echo "[3] Generate fresh critical detection"

SUBJECT="phase8.incident.$(date +%s%N)"
CORRELATION="phase8.correlation.$(date +%s%N)"

python3 - \
    "${EVENTS}" \
    "${SUBJECT}" \
    "${CORRELATION}" <<'PY'
import json
import sys

from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
subject = sys.argv[2]
correlation = sys.argv[3]

event = {
    "timestamp": datetime.now(
        timezone.utc
    ).isoformat(),
    "source": "finance-api",
    "event_type": "application_access",
    "outcome": "allow",
    "subject": subject,
    "resource": "finance-api",
    "correlation_id": correlation,
    "details": {
        "synthetic": True,
        "phase": 8,
        "purpose": "incident-response-validation",
    },
}

with path.open(
    "a",
    encoding="utf-8",
) as handle:
    handle.write(
        json.dumps(
            event,
            sort_keys=True,
        )
        + "\n"
    )
PY


FOUND=0

for _ in $(seq 1 20); do
    if python3 - \
        "${INCIDENTS}" \
        "${CORRELATION}" <<'PY'
import json
import sys

from pathlib import Path

path = Path(sys.argv[1])
correlation = sys.argv[2]

if not path.exists():
    raise SystemExit(1)

for line in path.read_text(
    encoding="utf-8"
).splitlines():
    row = json.loads(line)

    if (
        row.get("correlation_id") == correlation
        and row.get("detection_id") == "DET-004"
        and row.get("severity") == "SEV-1"
    ):
        raise SystemExit(0)

raise SystemExit(1)
PY
    then
        FOUND=1
        break
    fi

    sleep 1
done

if [[ "${FOUND}" -ne 1 ]]; then
    echo "[FAIL] SEV-1 incident was not generated"
    exit 1
fi

echo "[PASS] DET-004 produced SEV-1 incident"


echo
echo "[4] Verify containment record"

INCIDENT_RECORD="$(
    python3 - \
        "${INCIDENTS}" \
        "${CORRELATION}" <<'PY'
import json
import sys

from pathlib import Path

path = Path(sys.argv[1])
correlation = sys.argv[2]

for line in path.read_text(
    encoding="utf-8"
).splitlines():
    row = json.loads(line)

    if row.get("correlation_id") == correlation:
        print(row["incident_id"])
        raise SystemExit(0)

raise SystemExit(1)
PY
)"

python3 - \
    "${ACTIONS}" \
    "${INCIDENT_RECORD}" <<'PY'
import json
import sys

from pathlib import Path

path = Path(sys.argv[1])
incident_id = sys.argv[2]

assert path.exists()

for line in path.read_text(
    encoding="utf-8"
).splitlines():
    row = json.loads(line)

    if row.get("incident_id") == incident_id:
        assert row["mode"] == "simulated"
        assert row["status"] == "RECORDED"
        assert row["action_type"] == "isolate_resource_path"
        assert row["target"] == "finance-api"

        print(
            "[PASS] Critical incident containment action recorded"
        )

        raise SystemExit(0)

raise SystemExit(
    "[FAIL] No containment action found"
)
PY


echo
echo "[5] Recovery-plane isolation"

NETWORKS="$(
    docker inspect \
        "$("${COMPOSE[@]}" ps -q recovery-db)" \
        --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
)"

if [[ "${NETWORKS}" != *"recovery_net"* ]]; then
    echo "[FAIL] recovery-db missing recovery network"
    exit 1
fi

if [[ "${NETWORKS}" == *"data_net"* ]] \
    || [[ "${NETWORKS}" == *"finance_net"* ]] \
    || [[ "${NETWORKS}" == *"edge_net"* ]]
then
    echo "[FAIL] recovery-db attached to production network"
    exit 1
fi

echo "[PASS] Recovery database isolated from production networks"


echo
echo "[6] Production cannot resolve recovery database"

RESULT="$(
    "${COMPOSE[@]}" exec -T finance-api \
    python - <<'PY'
import socket

try:
    socket.getaddrinfo(
        "recovery-db",
        5432,
    )

except socket.gaierror:
    print("ISOLATED")
    raise SystemExit(0)

print("REACHABLE")
raise SystemExit(1)
PY
)"

if [[ "${RESULT}" != *"ISOLATED"* ]]; then
    echo "[FAIL] Finance API can resolve recovery-db"
    exit 1
fi

echo "[PASS] Finance workload cannot reach recovery database"


echo
echo "[7] Create known-good Finance recovery marker"

MARKER="trusted-phase8-$(date +%s%N)"

"${COMPOSE[@]}" exec -T finance-db \
    psql \
    -U finance_app \
    -d finance \
    -v ON_ERROR_STOP=1 \
    -c '
        CREATE TABLE IF NOT EXISTS recovery_validation (
            id integer PRIMARY KEY,
            marker text NOT NULL
        );
    ' \
    -c "
        INSERT INTO recovery_validation (id, marker)
        VALUES (1, '${MARKER}')
        ON CONFLICT (id)
        DO UPDATE SET marker = EXCLUDED.marker;
    " \
    >/dev/null

echo "[PASS] Known-good marker written: ${MARKER}"


echo
echo "[8] Create protected Finance backup"

"${COMPOSE[@]}" exec -T \
    backup-agent \
    /usr/local/bin/redoubt-backup

echo "[PASS] Backup completed"


echo
echo "[9] Verify recovery-store integrity"

"${COMPOSE[@]}" exec -T \
    recovery-db \
    sh -c '
        expected="$(cat /recovery/finance.sql.sha256)"
        actual="$(sha256sum /recovery/finance.sql | awk "{print \$1}")"

        test "${expected}" = "${actual}"
    '

echo "[PASS] SHA-256 backup integrity verified"


echo
echo "[10] Simulate production corruption"

CORRUPTED="CORRUPTED-$(date +%s%N)"

"${COMPOSE[@]}" exec -T finance-db \
    psql \
    -U finance_app \
    -d finance \
    -v ON_ERROR_STOP=1 \
    -c "
        UPDATE recovery_validation
        SET marker = '${CORRUPTED}'
        WHERE id = 1;
    " \
    >/dev/null

CURRENT="$(
    "${COMPOSE[@]}" exec -T finance-db \
        psql \
        -U finance_app \
        -d finance \
        -Atc '
            SELECT marker
            FROM recovery_validation
            WHERE id = 1;
        '
)"

if [[ "${CURRENT}" != "${CORRUPTED}" ]]; then
    echo "[FAIL] Production corruption simulation failed"
    exit 1
fi

echo "[PASS] Production marker changed after backup"


echo
echo "[11] Restore protected copy into isolated recovery database"

"${COMPOSE[@]}" exec -T \
    recovery-db \
    /usr/local/bin/redoubt-restore

RECOVERED="$(
    "${COMPOSE[@]}" exec -T recovery-db \
        psql \
        -U recovery_admin \
        -d recovery \
        -Atc '
            SELECT marker
            FROM recovery_validation
            WHERE id = 1;
        '
)"

if [[ "${RECOVERED}" != "${MARKER}" ]]; then
    echo "[FAIL] Restored data does not match known-good backup"
    echo "Expected: ${MARKER}"
    echo "Actual:   ${RECOVERED}"
    exit 1
fi

echo "[PASS] Restored data matches pre-corruption state"


echo
echo "[12] Confirm production remains corrupted"

PRODUCTION="$(
    "${COMPOSE[@]}" exec -T finance-db \
        psql \
        -U finance_app \
        -d finance \
        -Atc '
            SELECT marker
            FROM recovery_validation
            WHERE id = 1;
        '
)"

if [[ "${PRODUCTION}" != "${CORRUPTED}" ]]; then
    echo "[FAIL] Test cannot distinguish production and recovery state"
    exit 1
fi

echo "[PASS] Recovery validation occurred independently of production"


echo
echo "============================================================"
echo " PHASE 8 INCIDENT & RECOVERY TEST: PASS"
echo "============================================================"
