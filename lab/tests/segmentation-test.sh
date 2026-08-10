#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${LAB_DIR}"

COMPOSE=(
    docker compose
    --env-file .env
    -f compose.yaml
)

FAIL=0

resolves_from() {
    local source="$1"
    local target="$2"

    "${COMPOSE[@]}" exec -T \
        "${source}" \
        python - "${target}" <<'PY'
import socket
import sys

target = sys.argv[1]

try:
    socket.getaddrinfo(target, None)
    raise SystemExit(0)
except socket.gaierror:
    raise SystemExit(1)
PY
}

expect_isolated() {
    local source="$1"
    local target="$2"

    if resolves_from "${source}" "${target}"; then
        echo "[FAIL] ${source} can resolve ${target}"
        FAIL=1
    else
        echo "[PASS] ${source} isolated from ${target}"
    fi
}

expect_reachable() {
    local source="$1"
    local target="$2"

    if resolves_from "${source}" "${target}"; then
        echo "[PASS] ${source} can resolve required service ${target}"
    else
        echo "[FAIL] ${source} cannot resolve required service ${target}"
        FAIL=1
    fi
}

expect_secret_absent() {
    local service="$1"
    local variable="$2"

    if "${COMPOSE[@]}" exec -T "${service}" \
        sh -c "test -z \"\${${variable}:-}\""
    then
        echo "[PASS] ${service} does not possess ${variable}"
    else
        echo "[FAIL] ${service} possesses ${variable}"
        FAIL=1
    fi
}

expect_not_published() {
    local service="$1"
    local port="$2"
    local container_id
    local bindings

    container_id="$("${COMPOSE[@]}" ps -q "${service}")"

    if [[ -z "${container_id}" ]]; then
        echo "[FAIL] Could not resolve running container for ${service}"
        FAIL=1
        return
    fi

    bindings="$(
        docker inspect "${container_id}" \
            --format '{{json .NetworkSettings.Ports}}'
    )"

    if python3 - "${port}" "${bindings}" <<'PYPORT'
import json
import sys

port = f"{sys.argv[1]}/tcp"
ports = json.loads(sys.argv[2] or "{}") or {}

binding = ports.get(port)

# Docker represents an exposed but unpublished port as null.
# A non-empty binding list indicates a host publication.
raise SystemExit(0 if not binding else 1)
PYPORT
    then
        echo "[PASS] ${service}:${port} has no Docker host port binding"
    else
        echo "[FAIL] ${service}:${port} has a Docker host port binding"
        echo "       Port state: ${bindings}"
        FAIL=1
    fi
}


echo "============================================================"
echo " PROJECT REDOUBT — NETWORK SEGMENTATION TEST"
echo "============================================================"

echo
echo "[1] Employee workload isolation"

expect_isolated employee-api finance-api
expect_isolated employee-api finance-db
expect_isolated employee-api vault
expect_isolated employee-api opa
expect_isolated employee-api keycloak

echo
echo "[2] Finance workload isolation"

expect_isolated finance-api employee-api
expect_isolated finance-api opa
expect_isolated finance-api keycloak

echo
echo "[3] Required Finance dependencies"

expect_reachable finance-api finance-db
expect_reachable finance-api vault
expect_reachable finance-api telemetry

echo
echo "[4] Required Employee dependencies"

expect_reachable employee-api telemetry

echo
echo "[5] Gateway isolation"

expect_isolated gateway finance-db
expect_isolated gateway vault

expect_reachable gateway keycloak
expect_reachable gateway opa
expect_reachable gateway employee-api
expect_reachable gateway finance-api

echo
echo "[6] Credential compartmentalisation"

expect_secret_absent \
    employee-api \
    GATEWAY_FINANCE_TOKEN

expect_secret_absent \
    finance-api \
    GATEWAY_EMPLOYEE_TOKEN

echo
echo "[7] Docker host port publication"

expect_not_published finance-db 5432
expect_not_published vault 8200
expect_not_published opa 8181
expect_not_published employee-api 8000
expect_not_published finance-api 8000
expect_not_published telemetry 9000

echo
echo "============================================================"

if [[ "${FAIL}" -eq 0 ]]; then
    echo " PHASE 5 SEGMENTATION TEST: PASS"
else
    echo " PHASE 5 SEGMENTATION TEST: FAIL"
    exit 1
fi

echo "============================================================"
