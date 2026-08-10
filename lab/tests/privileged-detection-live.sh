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

set -a
source .env
set +a

COMPOSE=(
    docker compose
    --env-file .env
    -f compose.yaml
)

TOKEN_URL="http://127.0.0.1:8080/realms/restech/protocol/openid-connect/token"
BROKER="http://127.0.0.1:8101"
MANAGEMENT="http://127.0.0.1:8100"

EVENTS="${PROJECT_DIR}/evidence/runtime/security-events.jsonl"
ALERTS="${PROJECT_DIR}/evidence/runtime/security-alerts.jsonl"


token() {
    local username="$1"
    local password="$2"

    curl -fsS \
      -X POST \
      "${TOKEN_URL}" \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'grant_type=password' \
      --data-urlencode 'client_id=redoubt-admin-cli' \
      --data-urlencode "username=${username}" \
      --data-urlencode "password=${password}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["access_token"])
'
}


alert_count() {
    if [[ -f "${ALERTS}" ]]; then
        wc -l < "${ALERTS}"
    else
        echo 0
    fi
}


wait_alert() {
    local detection="$1"
    local start="$2"
    local match="$3"

    for _ in $(seq 1 20); do
        if [[ -f "${ALERTS}" ]]; then
            if tail \
                -n "+$((start + 1))" \
                "${ALERTS}" \
                | grep -F "\"detection_id\": \"${detection}\"" \
                | grep -Fq "${match}"
            then
                return 0
            fi
        fi

        sleep 1
    done

    return 1
}


echo "============================================================"
echo " PROJECT REDOUBT — PHASE 9 PRIVILEGED DETECTION TEST"
echo "============================================================"


echo
echo "[1] Authenticate administrators"

IAN="$(
    token \
      "ian.infrastructure" \
      "${IAN_ADMIN_PASSWORD}"
)"

SOPHIE="$(
    token \
      "sophie.security" \
      "${SOPHIE_ADMIN_PASSWORD}"
)"

ALICE="$(
    token \
      "alice.employee" \
      "${ALICE_PASSWORD}"
)"

echo "[PASS] Identities authenticated"


echo
echo "[2] DET-007 denied privileged elevation"

START="$(alert_count)"

curl -sS \
  -o /dev/null \
  -X POST \
  "${BROKER}/elevate/infrastructure" \
  -H "Authorization: Bearer ${ALICE}" \
  -H 'X-Admin-Device-Trusted: true' \
  -H 'Content-Type: application/json' \
  -d '{"ttl_seconds":30}'

if wait_alert \
    "DET-007" \
    "${START}" \
    '"subject": "alice.employee"'
then
    echo "[PASS] DET-007 live alert generated"
else
    echo "[FAIL] DET-007 not generated"
    exit 1
fi


echo
echo "[3] DET-008 repeated privileged elevation denials"

SUBJECT="phase9.elevation.$(date +%s%N)"
START="$(alert_count)"

python3 - \
    "${EVENTS}" \
    "${SUBJECT}" <<'PY'
import json
import sys

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from pathlib import Path

path = Path(sys.argv[1])
subject = sys.argv[2]

base = datetime.now(timezone.utc)

with path.open("a", encoding="utf-8") as handle:
    for index in range(3):
        event = {
            "timestamp": (
                base + timedelta(seconds=index)
            ).isoformat(),
            "source": "privilege-broker",
            "event_type": "privileged_elevation",
            "outcome": "deny",
            "subject": subject,
            "resource": "infrastructure",
            "correlation_id": f"{subject}-{index}",
            "details": {
                "synthetic": True,
                "reason": "repeated-privileged-denial",
            },
        }

        handle.write(
            json.dumps(event, sort_keys=True)
            + "\n"
        )
PY

if wait_alert \
    "DET-008" \
    "${START}" \
    "\"subject\": \"${SUBJECT}\""
then
    echo "[PASS] DET-008 live alert generated"
else
    echo "[FAIL] DET-008 not generated"
    exit 1
fi


echo
echo "[4] DET-009 direct management backend bypass"

CORRELATION="phase9.backend.$(date +%s%N)"
SUBJECT="phase9.backend-attacker"
START="$(alert_count)"

CODE="$(
    "${COMPOSE[@]}" exec -T \
      management-gateway \
      python - \
      "${CORRELATION}" \
      "${SUBJECT}" <<'PY'
import sys
import httpx

correlation = sys.argv[1]
subject = sys.argv[2]

response = httpx.get(
    "http://management-api:8201/infrastructure/status",
    headers={
        "X-Redoubt-Management-Token": "invalid",
        "X-Redoubt-Admin": subject,
        "X-Redoubt-Correlation-ID": correlation,
    },
)

print(response.status_code)
PY
)"

test "${CODE}" = "403"

if wait_alert \
    "DET-009" \
    "${START}" \
    "\"correlation_id\": \"${CORRELATION}\""
then
    echo "[PASS] DET-009 live alert generated"
else
    echo "[FAIL] DET-009 not generated"
    exit 1
fi


echo
echo "[5] DET-010 privileged request from untrusted device"

GRANT_JSON="$(
    curl -fsS \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${IAN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

GRANT="$(
    printf '%s' "${GRANT_JSON}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["elevation_grant"])
'
)"

START="$(alert_count)"

CODE="$(
    curl \
      -sS \
      -o /dev/null \
      -w '%{http_code}' \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN}" \
      -H "X-Redoubt-Elevation-Grant: ${GRANT}" \
      -H 'X-Admin-Device-Trusted: false'
)"

test "${CODE}" = "403"

if wait_alert \
    "DET-010" \
    "${START}" \
    '"subject": "ian.infrastructure"'
then
    echo "[PASS] DET-010 live alert generated"
else
    echo "[FAIL] DET-010 not generated"
    exit 1
fi


echo
echo "[6] DET-011 security-control modification"

SECURITY_GRANT_JSON="$(
    curl -fsS \
      -X POST \
      "${BROKER}/elevate/security" \
      -H "Authorization: Bearer ${SOPHIE}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

SECURITY_GRANT="$(
    printf '%s' "${SECURITY_GRANT_JSON}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["elevation_grant"])
'
)"

START="$(alert_count)"

CODE="$(
    curl \
      -sS \
      -o /dev/null \
      -w '%{http_code}' \
      -X POST \
      "${MANAGEMENT}/security/update-detection" \
      -H "Authorization: Bearer ${SOPHIE}" \
      -H "X-Redoubt-Elevation-Grant: ${SECURITY_GRANT}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "200"

if wait_alert \
    "DET-011" \
    "${START}" \
    '"subject": "sophie.security"'
then
    echo "[PASS] DET-011 live alert generated"
else
    echo "[FAIL] DET-011 not generated"
    exit 1
fi


echo
echo "[7] DET-012 management policy bypass"

CORRELATION="phase9.policy-bypass.$(date +%s%N)"
START="$(alert_count)"

python3 - \
    "${EVENTS}" \
    "${CORRELATION}" <<'PY'
import json
import sys

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path

path = Path(sys.argv[1])
correlation = sys.argv[2]

event = {
    "timestamp": datetime.now(
        timezone.utc
    ).isoformat(),
    "source": "management-api",
    "event_type": "privileged_operation",
    "outcome": "allow",
    "subject": "phase9.synthetic-bypass",
    "resource": "security-management",
    "correlation_id": correlation,
    "details": {
        "action": "read",
        "synthetic": True,
    },
}

with path.open("a", encoding="utf-8") as handle:
    handle.write(
        json.dumps(event, sort_keys=True)
        + "\n"
    )
PY

if wait_alert \
    "DET-012" \
    "${START}" \
    "\"correlation_id\": \"${CORRELATION}\""
then
    echo "[PASS] DET-012 live alert generated"
else
    echo "[FAIL] DET-012 not generated"
    exit 1
fi


echo
echo "============================================================"
echo " PHASE 9 PRIVILEGED DETECTION TEST: PASS"
echo "============================================================"
