#!/usr/bin/env bash

set -euo pipefail

LAB_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

cd "${LAB_DIR}"

set -a
source .env
set +a

TOKEN_URL="http://127.0.0.1:8080/realms/restech/protocol/openid-connect/token"
BROKER="http://127.0.0.1:8101"
MANAGEMENT="http://127.0.0.1:8100"

TMP="$(
    mktemp
)"

trap 'rm -f "${TMP}"' EXIT


token() {
    local username="$1"
    local password="$2"
    local client="$3"

    curl -fsS \
      -X POST \
      "${TOKEN_URL}" \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'grant_type=password' \
      --data-urlencode "client_id=${client}" \
      --data-urlencode "username=${username}" \
      --data-urlencode "password=${password}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["access_token"])
'
}


http_code() {
    curl \
      -sS \
      -o "${TMP}" \
      -w '%{http_code}' \
      "$@"
}


echo "============================================================"
echo " PROJECT REDOUBT — PHASE 9 PRIVILEGED ACCESS TEST"
echo "============================================================"


echo
echo "[1] Authenticate test identities"

IAN_ADMIN_TOKEN="$(
    token \
      "ian.infrastructure" \
      "${IAN_ADMIN_PASSWORD}" \
      "redoubt-admin-cli"
)"

IAN_NORMAL_TOKEN="$(
    token \
      "ian.infrastructure" \
      "${IAN_ADMIN_PASSWORD}" \
      "redoubt-test-cli"
)"

SOPHIE_ADMIN_TOKEN="$(
    token \
      "sophie.security" \
      "${SOPHIE_ADMIN_PASSWORD}" \
      "redoubt-admin-cli"
)"

ALICE_ADMIN_TOKEN="$(
    token \
      "alice.employee" \
      "${ALICE_PASSWORD}" \
      "redoubt-admin-cli"
)"

echo "[PASS] Privileged test identities authenticated"


echo
echo "[2] Standard identity cannot elevate"

CODE="$(
    http_code \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${ALICE_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

test "${CODE}" = "403"

echo "[PASS] Standard employee denied elevation"


echo
echo "[3] Admin cannot elevate from untrusted device"

CODE="$(
    http_code \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: false' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

test "${CODE}" = "403"

echo "[PASS] Untrusted admin device denied elevation"


echo
echo "[4] Normal-client admin token rejected"

CODE="$(
    http_code \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN_NORMAL_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "401"

echo "[PASS] Normal client cannot enter privileged path"


echo
echo "[5] Admin identity without JIT grant denied"

CODE="$(
    http_code \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "403"

echo "[PASS] Privileged identity alone is insufficient"


echo
echo "[6] Issue infrastructure JIT grant"

IAN_GRANT_JSON="$(
    curl -fsS \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

IAN_GRANT="$(
    printf '%s' "${IAN_GRANT_JSON}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["elevation_grant"])
'
)"

echo "[PASS] Infrastructure JIT grant issued"


echo
echo "[7] Correct role + trusted device + JIT grant allowed"

CODE="$(
    http_code \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H "X-Redoubt-Elevation-Grant: ${IAN_GRANT}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "200"

echo "[PASS] JIT privileged infrastructure access allowed"


echo
echo "[8] Valid grant cannot be reused from untrusted device"

CODE="$(
    http_code \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H "X-Redoubt-Elevation-Grant: ${IAN_GRANT}" \
      -H 'X-Admin-Device-Trusted: false'
)"

test "${CODE}" = "403"

echo "[PASS] Device posture remains required after elevation"


echo
echo "[9] Wrong privileged role cannot obtain infrastructure grant"

CODE="$(
    http_code \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${SOPHIE_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

test "${CODE}" = "403"

echo "[PASS] Administrative role separation enforced"


echo
echo "[10] Security administrator obtains security grant"

SOPHIE_GRANT_JSON="$(
    curl -fsS \
      -X POST \
      "${BROKER}/elevate/security" \
      -H "Authorization: Bearer ${SOPHIE_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":30}'
)"

SOPHIE_GRANT="$(
    printf '%s' "${SOPHIE_GRANT_JSON}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["elevation_grant"])
'
)"

CODE="$(
    http_code \
      "${MANAGEMENT}/security/status" \
      -H "Authorization: Bearer ${SOPHIE_ADMIN_TOKEN}" \
      -H "X-Redoubt-Elevation-Grant: ${SOPHIE_GRANT}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "200"

echo "[PASS] Security administrator JIT access allowed"


echo
echo "[11] Infrastructure grant cannot cross management domains"

CODE="$(
    http_code \
      "${MANAGEMENT}/security/status" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H "X-Redoubt-Elevation-Grant: ${IAN_GRANT}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "403"

echo "[PASS] JIT grant scope cannot cross domains"


echo
echo "[12] Expired JIT grant denied"

SHORT_GRANT_JSON="$(
    curl -fsS \
      -X POST \
      "${BROKER}/elevate/infrastructure" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H 'X-Admin-Device-Trusted: true' \
      -H 'Content-Type: application/json' \
      -d '{"ttl_seconds":2}'
)"

SHORT_GRANT="$(
    printf '%s' "${SHORT_GRANT_JSON}" \
    | python3 -c '
import json
import sys
print(json.load(sys.stdin)["elevation_grant"])
'
)"

sleep 4

CODE="$(
    http_code \
      "${MANAGEMENT}/infrastructure/status" \
      -H "Authorization: Bearer ${IAN_ADMIN_TOKEN}" \
      -H "X-Redoubt-Elevation-Grant: ${SHORT_GRANT}" \
      -H 'X-Admin-Device-Trusted: true'
)"

test "${CODE}" = "403"

echo "[PASS] Expired elevation grant rejected"


echo
echo "[13] Direct management backend bypass denied"

CODE="$(
    docker compose \
      --env-file .env \
      -f compose.yaml \
      exec -T management-gateway \
      python - <<'PY'
import httpx

response = httpx.get(
    "http://management-api:8201/infrastructure/status",
    headers={
        "X-Redoubt-Management-Token":
            "invalid-token",
        "X-Redoubt-Admin":
            "attacker",
    },
)

print(response.status_code)
PY
)"

test "${CODE}" = "403"

echo "[PASS] Management backend workload credential enforced"


echo
echo "============================================================"
echo " PHASE 9 PRIVILEGED ACCESS TEST: PASS"
echo "============================================================"
