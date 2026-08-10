#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="$(cd "${LAB_DIR}/.." && pwd)"

cd "${LAB_DIR}"

COMPOSE=(
    docker compose
    --env-file .env
    -f compose.yaml
)

EVENTS="${PROJECT_DIR}/evidence/runtime/security-events.jsonl"
ALERTS="${PROJECT_DIR}/evidence/runtime/security-alerts.jsonl"

echo "============================================================"
echo " PROJECT REDOUBT — PHASE 6 DETECTION TEST"
echo "============================================================"

echo
echo "[1] Detection unit tests"

python3 tests/detection-test.py


echo
echo "[2] Detection service"

DETECTION_ID="$("${COMPOSE[@]}" ps -q detection)"

if [[ -z "${DETECTION_ID}" ]]; then
    echo "[FAIL] Detection container not running"
    exit 1
fi

echo "[PASS] Detection container running"


echo
echo "[3] Detection engine network isolation"

NETWORK_MODE="$(
    docker inspect "${DETECTION_ID}" \
        --format '{{.HostConfig.NetworkMode}}'
)"

if [[ "${NETWORK_MODE}" == "none" ]]; then
    echo "[PASS] Detection engine has no Docker network"
else
    echo "[FAIL] Detection network mode: ${NETWORK_MODE}"
    exit 1
fi


echo
echo "[4] Live repeated-denial detection"

SUBJECT="phase6.threshold.$(date +%s%N)"

python3 - "${EVENTS}" "${SUBJECT}" <<'PY'
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

path = Path(sys.argv[1])
subject = sys.argv[2]

base = datetime.now(timezone.utc)

with path.open("a", encoding="utf-8") as handle:
    for i in range(3):
        event = {
            "timestamp": (
                base + timedelta(seconds=i)
            ).isoformat(),
            "source": "gateway",
            "event_type": "policy_decision",
            "outcome": "deny",
            "subject": subject,
            "resource": "finance-api",
            "correlation_id": f"{subject}-{i}",
            "details": {
                "device_trusted": True,
                "synthetic": True
            }
        }

        handle.write(
            json.dumps(event, sort_keys=True) + "\n"
        )
PY

FOUND=0

for _ in $(seq 1 15); do
    if [[ -f "${ALERTS}" ]] &&
       grep -F "\"detection_id\": \"DET-003\"" "${ALERTS}" |
       grep -Fq "\"subject\": \"${SUBJECT}\""
    then
        FOUND=1
        break
    fi

    sleep 1
done

if [[ "${FOUND}" -eq 1 ]]; then
    echo "[PASS] DET-003 live alert generated"
else
    echo "[FAIL] DET-003 live alert not generated"
    "${COMPOSE[@]}" logs --tail=50 detection
    exit 1
fi


echo
echo "[5] Live policy-bypass detection"

CORRELATION="phase6.bypass.$(date +%s%N)"

python3 - "${EVENTS}" "${CORRELATION}" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
correlation = sys.argv[2]

event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "source": "finance-api",
    "event_type": "application_access",
    "outcome": "allow",
    "subject": "phase6.synthetic-bypass",
    "resource": "finance-api",
    "correlation_id": correlation,
    "details": {
        "synthetic": True
    }
}

with path.open("a", encoding="utf-8") as handle:
    handle.write(
        json.dumps(event, sort_keys=True) + "\n"
    )
PY

FOUND=0

for _ in $(seq 1 15); do
    if [[ -f "${ALERTS}" ]] &&
       grep -F "\"detection_id\": \"DET-004\"" "${ALERTS}" |
       grep -Fq "\"correlation_id\": \"${CORRELATION}\""
    then
        FOUND=1
        break
    fi

    sleep 1
done

if [[ "${FOUND}" -eq 1 ]]; then
    echo "[PASS] DET-004 live alert generated"
else
    echo "[FAIL] DET-004 live alert not generated"
    "${COMPOSE[@]}" logs --tail=50 detection
    exit 1
fi


echo
echo "[6] Recent alert evidence"

tail -n 6 "${ALERTS}" |
python3 -c '
import json
import sys

for line in sys.stdin:
    alert = json.loads(line)

    print(
        "{} {} {:8} {} {}".format(
            alert.get("timestamp"),
            alert.get("detection_id"),
            alert.get("severity"),
            alert.get("subject"),
            alert.get("resource"),
        )
    )
'


echo
echo "============================================================"
echo " PHASE 6 DETECTION TEST: PASS"
echo "============================================================"
