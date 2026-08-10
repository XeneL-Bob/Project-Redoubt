#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd
)"

LAB_DIR="${PROJECT_ROOT}/lab"

SOURCE_DIR="${LAB_DIR}/supply-chain/source"
POLICY_DIR="${LAB_DIR}/supply-chain/policy"

SPOOL_DIR="${LAB_DIR}/supply-chain/runtime/telemetry"

ALERTS="${PROJECT_ROOT}/evidence/runtime/security-alerts.jsonl"

BUILDER_IMAGE="project-redoubt-supply-builder"
SIGNER_IMAGE="project-redoubt-supply-signer"
VERIFIER_IMAGE="project-redoubt-supply-verifier"

HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

SOURCE_COMMIT="$(
    git -C "${PROJECT_ROOT}" rev-parse HEAD
)"

SOURCE_BRANCH="$(
    git -C "${PROJECT_ROOT}" branch --show-current
)"

SOURCE_REF="refs/heads/${SOURCE_BRANCH}"

TMP_ROOT="$(
    mktemp -d /tmp/project-redoubt-supply-live.XXXXXX
)"

trap 'rm -rf "${TMP_ROOT}"' EXIT

mkdir -p "${SPOOL_DIR}"


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


assert_no_alert() {
    local detection="$1"
    local start="$2"
    local correlation="$3"

    sleep 4

    if [[ ! -f "${ALERTS}" ]]; then
        return 0
    fi

    if tail \
        -n "+$((start + 1))" \
        "${ALERTS}" \
        | grep -F "\"detection_id\": \"${detection}\"" \
        | grep -Fq "\"correlation_id\": \"${correlation}\""
    then
        return 1
    fi

    return 0
}


new_runtime() {
    local runtime="$1"

    mkdir -p \
        "${runtime}/private" \
        "${runtime}/trust" \
        "${runtime}/out"
}


generate_keys() {
    local runtime="$1"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${runtime}/private:/private" \
        -v "${runtime}/trust:/trust" \
        "${SIGNER_IMAGE}" \
        python /app/keygen.py \
        >/dev/null
}


build_artifact() {
    local runtime="$1"
    local dirty="$2"
    local builder="$3"
    local correlation="$4"
    local telemetry="$5"

    local telemetry_args=()

    if [[ "${telemetry}" == "true" ]]; then
        telemetry_args=(
            -e EVENTS_FILE=/telemetry/security-events.jsonl
            -e CORRELATION_ID="${correlation}"
            -v "${SPOOL_DIR}:/telemetry"
        )
    fi

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e SOURCE_COMMIT="${SOURCE_COMMIT}" \
        -e SOURCE_REF="${SOURCE_REF}" \
        -e SOURCE_DIRTY="${dirty}" \
        -e BUILDER_ID="${builder}" \
        "${telemetry_args[@]}" \
        -v "${SOURCE_DIR}:/source:ro" \
        -v "${runtime}/out:/out" \
        "${BUILDER_IMAGE}"
}


sign_provenance() {
    local runtime="$1"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${runtime}/private:/private:ro" \
        -v "${runtime}/out:/out" \
        "${SIGNER_IMAGE}" \
        python /app/sign.py \
        >/dev/null
}


verify_release() {
    local runtime="$1"
    local correlation="$2"
    local telemetry="$3"

    local telemetry_args=()

    if [[ "${telemetry}" == "true" ]]; then
        telemetry_args=(
            -e EVENTS_FILE=/telemetry/security-events.jsonl
            -e CORRELATION_ID="${correlation}"
            -v "${SPOOL_DIR}:/telemetry"
        )
    fi

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        "${telemetry_args[@]}" \
        -v "${runtime}/out:/out:ro" \
        -v "${runtime}/trust:/trust:ro" \
        -v "${POLICY_DIR}:/policy:ro" \
        "${VERIFIER_IMAGE}"
}


prepare_signed_release() {
    local runtime="$1"
    local builder="${2:-project-redoubt/trusted-builder}"

    new_runtime "${runtime}"
    generate_keys "${runtime}"

    build_artifact \
        "${runtime}" \
        false \
        "${builder}" \
        "no-telemetry" \
        false \
        >/dev/null

    sign_provenance "${runtime}"
}


echo "============================================================"
echo " PROJECT REDOUBT — SUPPLY CHAIN LIVE DETECTIONS"
echo "============================================================"


echo
echo "[1] DET-013 artifact integrity failure"

RUNTIME="${TMP_ROOT}/det013"
CORRELATION="phase10.det013.$(date +%s%N)"

prepare_signed_release "${RUNTIME}"

printf '\nTAMPERED\n' \
    >>"${RUNTIME}/out/restech-release-component.tar"

START="$(alert_count)"

if verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Tampered artifact accepted"
fi

if wait_alert \
    "DET-013" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-013 live alert generated"
else
    fail "DET-013 live alert missing"
fi


echo
echo "[2] DET-014 provenance signature failure"

RUNTIME="${TMP_ROOT}/det014"
CORRELATION="phase10.det014.$(date +%s%N)"

prepare_signed_release "${RUNTIME}"

python3 - \
    "${RUNTIME}/out/provenance.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])

data = json.loads(
    path.read_text(encoding="utf-8")
)

data["builder"]["id"] = "attacker/forged-builder"

path.write_text(
    json.dumps(
        data,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)
PY

START="$(alert_count)"

if verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Forged provenance accepted"
fi

if wait_alert \
    "DET-014" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-014 live alert generated"
else
    fail "DET-014 live alert missing"
fi


echo
echo "[3] DET-015 untrusted builder"

RUNTIME="${TMP_ROOT}/det015"
CORRELATION="phase10.det015.$(date +%s%N)"

prepare_signed_release \
    "${RUNTIME}" \
    "attacker/untrusted-builder"

START="$(alert_count)"

if verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Untrusted builder accepted"
fi

if wait_alert \
    "DET-015" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-015 live alert generated"
else
    fail "DET-015 live alert missing"
fi


echo
echo "[4] DET-016 dirty source build"

RUNTIME="${TMP_ROOT}/det016"
CORRELATION="phase10.det016.$(date +%s%N)"

new_runtime "${RUNTIME}"

START="$(alert_count)"

if build_artifact \
    "${RUNTIME}" \
    true \
    "project-redoubt/trusted-builder" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Dirty source build accepted"
fi

if wait_alert \
    "DET-016" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-016 live alert generated"
else
    fail "DET-016 live alert missing"
fi


echo
echo "[5] DET-017 unsigned release"

RUNTIME="${TMP_ROOT}/det017"
CORRELATION="phase10.det017.$(date +%s%N)"

new_runtime "${RUNTIME}"
generate_keys "${RUNTIME}"

build_artifact \
    "${RUNTIME}" \
    false \
    "project-redoubt/trusted-builder" \
    "no-telemetry" \
    false \
    >/dev/null

START="$(alert_count)"

if verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null 2>&1
then
    fail "Unsigned release accepted"
fi

if wait_alert \
    "DET-017" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-017 live alert generated"
else
    fail "DET-017 live alert missing"
fi


echo
echo "[6] Legitimate trusted release correlation"

RUNTIME="${TMP_ROOT}/legitimate"
CORRELATION="phase10.legitimate.$(date +%s%N)"

new_runtime "${RUNTIME}"
generate_keys "${RUNTIME}"

START="$(alert_count)"

build_artifact \
    "${RUNTIME}" \
    false \
    "project-redoubt/trusted-builder" \
    "${CORRELATION}" \
    true \
    >/dev/null

sign_provenance "${RUNTIME}"

verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null

if assert_no_alert \
    "DET-018" \
    "${START}" \
    "${CORRELATION}"
then
    pass "Legitimate release suppressed DET-018"
else
    fail "Legitimate release triggered DET-018"
fi


echo
echo "[7] DET-018 release without trusted build"

RUNTIME="${TMP_ROOT}/det018"
CORRELATION="phase10.det018.$(date +%s%N)"

prepare_signed_release "${RUNTIME}"

START="$(alert_count)"

verify_release \
    "${RUNTIME}" \
    "${CORRELATION}" \
    true \
    >/dev/null

if wait_alert \
    "DET-018" \
    "${START}" \
    "${CORRELATION}"
then
    pass "DET-018 live alert generated"
else
    fail "DET-018 live alert missing"
fi


echo
echo "============================================================"
echo " PHASE 10 SUPPLY CHAIN LIVE DETECTIONS: PASS"
echo "============================================================"
