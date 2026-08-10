#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="$(cd "${LAB_DIR}/.." && pwd)"

cd "${LAB_DIR}"

set -a
source .env
set +a

KEYCLOAK="http://localhost:8080"
GATEWAY="http://localhost:8000"

wait_for_url() {
    local url="$1"
    local description="$2"

    for _ in $(seq 1 90); do
        if curl -fsS "$url" >/dev/null 2>&1; then
            echo "[PASS] ${description}"
            return 0
        fi

        sleep 2
    done

    echo "[FAIL] Timed out waiting for ${description}"
    return 1
}

get_token() {
    local username="$1"
    local password="$2"
    local response
    local http_code
    local body_file

    body_file="$(mktemp)"

    http_code="$(
        curl -sS \
            -o "${body_file}" \
            -w '%{http_code}' \
            -X POST \
            "${KEYCLOAK}/realms/restech/protocol/openid-connect/token" \
            -H "Content-Type: application/x-www-form-urlencoded" \
            --data-urlencode "client_id=redoubt-test-cli" \
            --data-urlencode "username=${username}" \
            --data-urlencode "password=${password}" \
            --data-urlencode "grant_type=password"
    )"

    if [[ "${http_code}" != "200" ]]; then
        echo "[FAIL] Keycloak authentication failed for ${username}" >&2
        echo "       HTTP ${http_code}" >&2
        python3 -m json.tool "${body_file}" >&2 2>/dev/null \
            || cat "${body_file}" >&2
        rm -f "${body_file}"
        return 1
    fi

    response="$(
        python3 -c \
            'import json,sys; print(json.load(open(sys.argv[1]))["access_token"])' \
            "${body_file}"
    )"

    rm -f "${body_file}"

    printf '%s\n' "${response}"
}
expect_code() {
    local expected="$1"
    local description="$2"
    shift 2

    local code

    code="$(curl -sS -o /tmp/redoubt-response.json -w '%{http_code}' "$@")"

    if [[ "$code" == "$expected" ]]; then
        echo "[PASS] ${description} -> HTTP ${code}"
    else
        echo "[FAIL] ${description}"
        echo "       Expected: ${expected}"
        echo "       Actual:   ${code}"
        echo
        cat /tmp/redoubt-response.json || true
        echo
        exit 1
    fi
}

echo "============================================================"
echo " PROJECT REDOUBT — PHASE 5 SMOKE TEST"
echo "============================================================"

wait_for_url \
    "${KEYCLOAK}/realms/restech/.well-known/openid-configuration" \
    "Keycloak realm"

wait_for_url \
    "${GATEWAY}/health" \
    "Policy Enforcement Gateway"

ALICE_TOKEN="$(get_token alice.employee "${ALICE_PASSWORD}")"
BOB_TOKEN="$(get_token bob.developer "${BOB_PASSWORD}")"
CAROL_TOKEN="$(get_token carol.finance "${CAROL_PASSWORD}")"
ERIN_TOKEN="$(get_token erin.contractor "${ERIN_PASSWORD}")"

echo "[PASS] Test identities authenticated"

expect_code \
    401 \
    "Unauthenticated request denied" \
    "${GATEWAY}/employee/profile"

expect_code \
    200 \
    "Employee may access Employee API" \
    "${GATEWAY}/employee/profile" \
    -H "Authorization: Bearer ${ALICE_TOKEN}" \
    -H "X-Device-Trusted: true"

expect_code \
    403 \
    "Employee denied Finance API" \
    "${GATEWAY}/finance/summary" \
    -H "Authorization: Bearer ${ALICE_TOKEN}" \
    -H "X-Device-Trusted: true"

expect_code \
    403 \
    "Finance user denied from untrusted device" \
    "${GATEWAY}/finance/summary" \
    -H "Authorization: Bearer ${CAROL_TOKEN}" \
    -H "X-Device-Trusted: false"

expect_code \
    200 \
    "Finance user allowed from trusted device" \
    "${GATEWAY}/finance/summary" \
    -H "Authorization: Bearer ${CAROL_TOKEN}" \
    -H "X-Device-Trusted: true"

expect_code \
    403 \
    "Developer denied Finance API" \
    "${GATEWAY}/finance/summary" \
    -H "Authorization: Bearer ${BOB_TOKEN}" \
    -H "X-Device-Trusted: true"

expect_code \
    403 \
    "Contractor denied Employee API" \
    "${GATEWAY}/employee/profile" \
    -H "Authorization: Bearer ${ERIN_TOKEN}" \
    -H "X-Device-Trusted: true"

echo
echo "Finance response:"
curl -fsS \
    "${GATEWAY}/finance/summary" \
    -H "Authorization: Bearer ${CAROL_TOKEN}" \
    -H "X-Device-Trusted: true" \
    | python3 -m json.tool

echo
echo "Recent central security telemetry:"

if [[ -f "${PROJECT_DIR}/evidence/runtime/security-events.jsonl" ]]; then
    tail -n 10 \
        "${PROJECT_DIR}/evidence/runtime/security-events.jsonl" \
        | python3 -c '
import json
import sys

for line in sys.stdin:
    try:
        obj = json.loads(line)
        print(
            "{} {} {} {} {} {}".format(
                obj.get("timestamp"),
                obj.get("source"),
                obj.get("event_type"),
                obj.get("outcome"),
                obj.get("subject"),
                obj.get("resource"),
            )
        )
    except Exception:
        print(line.rstrip())
'
else
    echo "[WARN] No telemetry file found."
fi

echo
echo "============================================================"
echo " PHASE 5 SMOKE TEST: PASS"
echo "============================================================"
