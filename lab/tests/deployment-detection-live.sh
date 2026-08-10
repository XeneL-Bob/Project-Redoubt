#!/usr/bin/env bash

set -euo pipefail

ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd
)"

LAB="${ROOT}/lab"

SOURCE="${LAB}/supply-chain/source"
POLICY="${LAB}/supply-chain/policy"
SPOOL="${LAB}/supply-chain/runtime/telemetry"

ALERTS="${ROOT}/evidence/runtime/security-alerts.jsonl"

HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

BUILDER="project-redoubt-supply-builder"
SIGNER="project-redoubt-supply-signer"
VERIFIER="project-redoubt-supply-verifier"
APPROVER="project-redoubt-release-approver"
DEPLOYER="project-redoubt-deployer"

SOURCE_COMMIT="$(
    git -C "${ROOT}" rev-parse HEAD
)"

SOURCE_BRANCH="$(
    git -C "${ROOT}" branch --show-current
)"

if [[ -n "${SOURCE_BRANCH}" ]]; then
    SOURCE_REF="refs/heads/${SOURCE_BRANCH}"
else
    SOURCE_REF="detached/${SOURCE_COMMIT}"
fi

TMP="$(
    mktemp -d /tmp/project-redoubt-deployment-live.XXXXXX
)"

trap 'rm -rf "${TMP}"' EXIT

mkdir -p \
    "${SPOOL}" \
    "${TMP}/release-private" \
    "${TMP}/release-trust" \
    "${TMP}/approval-private" \
    "${TMP}/approval-trust"


pass() {
    printf '[PASS] %s\n' "$1"
}


fail() {
    printf '[FAIL] %s\n' "$1"
    exit 1
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
    local correlation="$3"

    for _ in $(seq 1 30); do
        if [[ -f "${ALERTS}" ]]; then
            if tail \
                -n "+$((start + 1))" \
                "${ALERTS}" \
                | grep -F "\"detection_id\": \"${detection}\"" \
                | grep -Fq "\"correlation_id\": \"${correlation}\""
            then
                return 0
            fi
        fi

        sleep 1
    done

    return 1
}


new_case() {
    local name="$1"

    mkdir -p \
        "${TMP}/${name}/out" \
        "${TMP}/${name}/receipt" \
        "${TMP}/${name}/approval" \
        "${TMP}/${name}/deploy"
}


generate_keys() {
    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${TMP}/release-private:/private" \
        -v "${TMP}/release-trust:/trust" \
        "${SIGNER}" \
        python /app/keygen.py \
        >/dev/null

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${TMP}/approval-private:/approval-private" \
        -v "${TMP}/approval-trust:/approval-trust" \
        "${APPROVER}" \
        python /app/keygen.py \
        >/dev/null
}


build_release() {
    local case_name="$1"
    local correlation="$2"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e SOURCE_COMMIT="${SOURCE_COMMIT}" \
        -e SOURCE_REF="${SOURCE_REF}" \
        -e SOURCE_DIRTY=false \
        -e BUILDER_ID="project-redoubt/trusted-builder" \
        -e CORRELATION_ID="${correlation}" \
        -v "${SOURCE}:/source:ro" \
        -v "${TMP}/${case_name}/out:/out" \
        "${BUILDER}" \
        >/dev/null

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${TMP}/release-private:/private:ro" \
        -v "${TMP}/${case_name}/out:/out" \
        "${SIGNER}" \
        python /app/sign.py \
        >/dev/null
}


verify_release() {
    local case_name="$1"
    local correlation="$2"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e CORRELATION_ID="${correlation}" \
        -e RECEIPT_FILE=/receipt/verification-receipt.json \
        -v "${TMP}/${case_name}/out:/out:ro" \
        -v "${TMP}/release-trust:/trust:ro" \
        -v "${POLICY}:/policy:ro" \
        -v "${TMP}/${case_name}/receipt:/receipt" \
        "${VERIFIER}" \
        >/dev/null
}


approve_release() {
    local case_name="$1"
    local correlation="$2"
    local telemetry="$3"

    local telemetry_args=()

    if [[ "${telemetry}" == "true" ]]; then
        telemetry_args=(
            -e EVENTS_FILE=/telemetry/security-events.jsonl
            -e CORRELATION_ID="${correlation}"
            -v "${SPOOL}:/telemetry"
        )
    fi

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e APPROVER_ID="restech/release-approver" \
        -e DEPLOYMENT_ENVIRONMENT=staging \
        "${telemetry_args[@]}" \
        -v "${TMP}/${case_name}/out:/release:ro" \
        -v "${TMP}/release-trust:/release-trust:ro" \
        -v "${TMP}/${case_name}/receipt:/receipt:ro" \
        -v "${POLICY}:/policy:ro" \
        -v "${TMP}/approval-private:/approval-private:ro" \
        -v "${TMP}/${case_name}/approval:/approval" \
        "${APPROVER}"
}


deploy_release() {
    local release_dir="$1"
    local case_name="$2"
    local correlation="$3"
    local telemetry="$4"

    local telemetry_args=()

    if [[ "${telemetry}" == "true" ]]; then
        telemetry_args=(
            -e EVENTS_FILE=/telemetry/security-events.jsonl
            -e CORRELATION_ID="${correlation}"
            -v "${SPOOL}:/telemetry"
        )
    fi

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e DEPLOYMENT_ENVIRONMENT=staging \
        "${telemetry_args[@]}" \
        -v "${release_dir}:/release:ro" \
        -v "${TMP}/${case_name}/approval:/approval:ro" \
        -v "${TMP}/approval-trust:/approval-trust:ro" \
        -v "${TMP}/${case_name}/deploy:/deploy" \
        "${DEPLOYER}"
}


echo "============================================================"
echo " PROJECT REDOUBT — LIVE DEPLOYMENT DETECTIONS"
echo "============================================================"


echo
echo "[Preflight] Generate independent trust keys"

generate_keys

pass "Release and deployment-approval trust domains ready"


echo
echo "[1] DET-019 trusted-build correlation bypass"

CASE="det019"
BUILD_CORRELATION="phase10.det019.build.$(date +%s%N)"
ATTACK_CORRELATION="phase10.det019.attack.$(date +%s%N)"

new_case "${CASE}"

build_release \
    "${CASE}" \
    "${BUILD_CORRELATION}"

verify_release \
    "${CASE}" \
    "${ATTACK_CORRELATION}"

START="$(alert_count)"

if approve_release \
    "${CASE}" \
    "${ATTACK_CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Mismatched trusted-build correlation was approved"
fi

if wait_alert \
    "DET-019" \
    "${START}" \
    "${ATTACK_CORRELATION}"
then
    pass "DET-019 live alert generated"
else
    fail "DET-019 live alert missing"
fi


echo
echo "[2] DET-020 post-approval artifact tampering"

CASE="det020"
CORRELATION="phase10.det020.$(date +%s%N)"

new_case "${CASE}"

build_release \
    "${CASE}" \
    "${CORRELATION}"

verify_release \
    "${CASE}" \
    "${CORRELATION}"

approve_release \
    "${CASE}" \
    "${CORRELATION}" \
    false \
    >/dev/null

TAMPER="${TMP}/${CASE}/tampered"

mkdir -p "${TAMPER}"

cp \
    "${TMP}/${CASE}/out/restech-release-component.tar" \
    "${TAMPER}/restech-release-component.tar"

printf '\nATTACKER-POST-APPROVAL-TAMPER\n' \
    >> "${TAMPER}/restech-release-component.tar"

START="$(alert_count)"

if deploy_release \
    "${TAMPER}" \
    "${CASE}" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Tampered approved artifact was deployed"
fi

if wait_alert \
    "DET-020" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-020 live alert generated"
else
    fail "DET-020 live alert missing"
fi


echo
echo "============================================================"
echo " PHASE 10 LIVE DEPLOYMENT DETECTIONS: PASS"
echo "============================================================"
