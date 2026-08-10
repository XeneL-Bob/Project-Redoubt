#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd
)"

SOURCE_DIR="${PROJECT_ROOT}/lab/supply-chain/source"
POLICY_DIR="${PROJECT_ROOT}/lab/supply-chain/policy"

BUILDER_IMAGE="project-redoubt-supply-builder"
SIGNER_IMAGE="project-redoubt-supply-signer"
VERIFIER_IMAGE="project-redoubt-supply-verifier"

SOURCE_COMMIT="${REDOUBT_SOURCE_COMMIT:-$(git -C "${PROJECT_ROOT}" rev-parse HEAD)}"

SOURCE_BRANCH="$(
    git -C "${PROJECT_ROOT}" branch --show-current
)"

if [[ -n "${REDOUBT_SOURCE_REF:-}" ]]; then
    SOURCE_REF="${REDOUBT_SOURCE_REF}"
elif [[ -n "${SOURCE_BRANCH}" ]]; then
    SOURCE_REF="refs/heads/${SOURCE_BRANCH}"
else
    SOURCE_REF="detached/${SOURCE_COMMIT}"
fi

HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

TMP_ROOT="$(
    mktemp -d /tmp/project-redoubt-supply-chain.XXXXXX
)"

trap 'rm -rf "${TMP_ROOT}"' EXIT


pass() {
    printf '[PASS] %s\n' "$1"
}


fail() {
    printf '[FAIL] %s\n' "$1"
    exit 1
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
    local builder_id="$3"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -e SOURCE_COMMIT="${SOURCE_COMMIT}" \
        -e SOURCE_REF="${SOURCE_REF}" \
        -e SOURCE_DIRTY="${dirty}" \
        -e BUILDER_ID="${builder_id}" \
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
        python /app/sign.py
}


verify_release() {
    local runtime="$1"

    docker run --rm \
        --network none \
        --user "${HOST_UID}:${HOST_GID}" \
        -v "${runtime}/out:/out:ro" \
        -v "${runtime}/trust:/trust:ro" \
        -v "${POLICY_DIR}:/policy:ro" \
        "${VERIFIER_IMAGE}"
}


prepare_signed_release() {
    local runtime="$1"
    local builder_id="${2:-project-redoubt/trusted-builder}"

    new_runtime "${runtime}"
    generate_keys "${runtime}"

    build_artifact \
        "${runtime}" \
        false \
        "${builder_id}" \
        >/dev/null

    sign_provenance \
        "${runtime}" \
        >/dev/null
}


echo "============================================================"
echo " PROJECT REDOUBT — SUPPLY CHAIN SECURITY VALIDATION"
echo "============================================================"


echo
echo "[1] Trusted release baseline"

RUNTIME="${TMP_ROOT}/baseline"

prepare_signed_release "${RUNTIME}"

if verify_release "${RUNTIME}" \
    >"${TMP_ROOT}/baseline.log" 2>&1
then
    grep -q '"decision": "ALLOW"' \
        "${TMP_ROOT}/baseline.log" \
        || fail "Trusted release did not return ALLOW"

    pass "Trusted signed release accepted"
else
    cat "${TMP_ROOT}/baseline.log"
    fail "Trusted release unexpectedly denied"
fi


echo
echo "[2] Unsigned artifact"

RUNTIME="${TMP_ROOT}/unsigned"

new_runtime "${RUNTIME}"
generate_keys "${RUNTIME}"

build_artifact \
    "${RUNTIME}" \
    false \
    "project-redoubt/trusted-builder" \
    >/dev/null

if verify_release "${RUNTIME}" \
    >"${TMP_ROOT}/unsigned.log" 2>&1
then
    fail "Unsigned release was accepted"
fi

grep -q \
    'required object missing: provenance.sig' \
    "${TMP_ROOT}/unsigned.log" \
    || {
        cat "${TMP_ROOT}/unsigned.log"
        fail "Unsigned release failed for unexpected reason"
    }

pass "Unsigned release denied"


echo
echo "[3] Post-build artifact tampering"

RUNTIME="${TMP_ROOT}/artifact-tamper"

prepare_signed_release "${RUNTIME}"

printf '\nATTACKER-MODIFIED-ARTIFACT\n' \
    >>"${RUNTIME}/out/restech-release-component.tar"

if verify_release "${RUNTIME}" \
    >"${TMP_ROOT}/artifact-tamper.log" 2>&1
then
    fail "Tampered artifact was accepted"
fi

grep -q \
    'artifact digest mismatch' \
    "${TMP_ROOT}/artifact-tamper.log" \
    || {
        cat "${TMP_ROOT}/artifact-tamper.log"
        fail "Artifact tampering failed for unexpected reason"
    }

pass "Post-build artifact tampering detected"


echo
echo "[4] Provenance forgery after signing"

RUNTIME="${TMP_ROOT}/provenance-forgery"

prepare_signed_release "${RUNTIME}"

python3 - \
    "${RUNTIME}/out/provenance.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])

document = json.loads(
    path.read_text(encoding="utf-8")
)

document["builder"]["id"] = (
    "attacker/forged-builder"
)

path.write_text(
    json.dumps(
        document,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)
PY

if verify_release "${RUNTIME}" \
    >"${TMP_ROOT}/provenance-forgery.log" 2>&1
then
    fail "Forged provenance was accepted"
fi

grep -q \
    'provenance signature invalid' \
    "${TMP_ROOT}/provenance-forgery.log" \
    || {
        cat "${TMP_ROOT}/provenance-forgery.log"
        fail "Forged provenance failed for unexpected reason"
    }

pass "Signed provenance tampering detected"


echo
echo "[5] Validly signed artifact from untrusted builder"

RUNTIME="${TMP_ROOT}/untrusted-builder"

prepare_signed_release \
    "${RUNTIME}" \
    "attacker/untrusted-builder"

if verify_release "${RUNTIME}" \
    >"${TMP_ROOT}/untrusted-builder.log" 2>&1
then
    fail "Untrusted builder release was accepted"
fi

grep -q \
    'untrusted builder identity' \
    "${TMP_ROOT}/untrusted-builder.log" \
    || {
        cat "${TMP_ROOT}/untrusted-builder.log"
        fail "Untrusted builder failed for unexpected reason"
    }

pass "Untrusted builder denied by release policy"


echo
echo "[6] Dirty source repository"

RUNTIME="${TMP_ROOT}/dirty-source"

new_runtime "${RUNTIME}"

if build_artifact \
    "${RUNTIME}" \
    true \
    "project-redoubt/trusted-builder" \
    >"${TMP_ROOT}/dirty-source.log" 2>&1
then
    fail "Dirty source repository was built"
fi

grep -q \
    'BUILD DENIED: source repository is dirty' \
    "${TMP_ROOT}/dirty-source.log" \
    || {
        cat "${TMP_ROOT}/dirty-source.log"
        fail "Dirty source failed for unexpected reason"
    }

pass "Dirty source build denied"


echo
echo "[7] Read-only source boundary"

RUNTIME="${TMP_ROOT}/readonly-source"

new_runtime "${RUNTIME}"

if docker run --rm \
    --network none \
    --entrypoint sh \
    -v "${SOURCE_DIR}:/source:ro" \
    -v "${RUNTIME}/out:/out" \
    "${BUILDER_IMAGE}" \
    -c 'printf attack > /source/.redoubt-write-test' \
    >"${TMP_ROOT}/readonly-source.log" 2>&1
then
    fail "Builder modified read-only source"
fi

test ! -e \
    "${SOURCE_DIR}/.redoubt-write-test" \
    || fail "Source tree was modified"

pass "Builder cannot modify source repository"


echo
echo "[8] Builder signing-key isolation"

if docker run --rm \
    --network none \
    --entrypoint python \
    -v "${SOURCE_DIR}:/source:ro" \
    "${BUILDER_IMAGE}" \
    -c '
from pathlib import Path
import sys

key = Path(
    "/private/release-signing-key.pem"
)

sys.exit(
    1 if key.exists() else 0
)
'
then
    pass "Builder has no release signing key"
else
    fail "Builder can access release signing key"
fi


echo
echo "[9] Verifier private-key isolation"

RUNTIME="${TMP_ROOT}/verifier-isolation"

prepare_signed_release "${RUNTIME}"

if docker run --rm \
    --network none \
    --entrypoint python \
    -v "${RUNTIME}/out:/out:ro" \
    -v "${RUNTIME}/trust:/trust:ro" \
    -v "${POLICY_DIR}:/policy:ro" \
    "${VERIFIER_IMAGE}" \
    -c '
from pathlib import Path
import sys

key = Path(
    "/private/release-signing-key.pem"
)

sys.exit(
    1 if key.exists() else 0
)
'
then
    pass "Verifier has no release private key"
else
    fail "Verifier can access release private key"
fi


echo
echo "============================================================"
echo " PHASE 10 SUPPLY CHAIN SECURITY TEST: PASS"
echo "============================================================"
