#!/usr/bin/env bash

set -euo pipefail

ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd
)"

LAB="${ROOT}/lab"

SOURCE="${LAB}/supply-chain/source"
POLICY="${LAB}/supply-chain/policy"

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
    mktemp -d /tmp/project-redoubt-deployment.XXXXXX
)"

trap 'rm -rf "${TMP}"' EXIT


mkdir -p \
    "${TMP}/release-private" \
    "${TMP}/release-trust" \
    "${TMP}/out" \
    "${TMP}/receipt" \
    "${TMP}/approval-private" \
    "${TMP}/approval-trust" \
    "${TMP}/approval-valid" \
    "${TMP}/approval-bypass" \
    "${TMP}/deploy"


echo "============================================================"
echo " PROJECT REDOUBT — DEPLOYMENT APPROVAL GATE"
echo "============================================================"


echo
echo "[1] Generate separate release and approval keys"

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

echo "[PASS] Independent signing domains created"


echo
echo "[2] Build trusted release"

CORRELATION="phase10.deployment.$(date +%s%N)"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e SOURCE_COMMIT="${SOURCE_COMMIT}" \
    -e SOURCE_REF="${SOURCE_REF}" \
    -e SOURCE_DIRTY=false \
    -e BUILDER_ID="project-redoubt/trusted-builder" \
    -e CORRELATION_ID="${CORRELATION}" \
    -v "${SOURCE}:/source:ro" \
    -v "${TMP}/out:/out" \
    "${BUILDER}" \
    >/dev/null

echo "[PASS] Trusted build completed"


echo
echo "[3] Sign release provenance"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -v "${TMP}/release-private:/private:ro" \
    -v "${TMP}/out:/out" \
    "${SIGNER}" \
    python /app/sign.py \
    >/dev/null

echo "[PASS] Release provenance signed"


echo
echo "[4] Verify release and issue verification receipt"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e CORRELATION_ID="${CORRELATION}" \
    -e RECEIPT_FILE=/receipt/verification-receipt.json \
    -v "${TMP}/out:/out:ro" \
    -v "${TMP}/release-trust:/trust:ro" \
    -v "${POLICY}:/policy:ro" \
    -v "${TMP}/receipt:/receipt" \
    "${VERIFIER}" \
    >/dev/null

test -s \
    "${TMP}/receipt/verification-receipt.json"

echo "[PASS] Release verification receipt issued"


echo
echo "[5] Independent release approval"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e APPROVER_ID="restech/release-approver" \
    -e DEPLOYMENT_ENVIRONMENT=staging \
    -v "${TMP}/out:/release:ro" \
    -v "${TMP}/release-trust:/release-trust:ro" \
    -v "${TMP}/receipt:/receipt:ro" \
    -v "${POLICY}:/policy:ro" \
    -v "${TMP}/approval-private:/approval-private:ro" \
    -v "${TMP}/approval-valid:/approval" \
    "${APPROVER}" \
    >/dev/null

test -s \
    "${TMP}/approval-valid/deployment-approval.json"

test -s \
    "${TMP}/approval-valid/deployment-approval.sig"

echo "[PASS] Independent deployment approval issued"


echo
echo "[6] Approved deployment succeeds"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e DEPLOYMENT_ENVIRONMENT=staging \
    -v "${TMP}/out:/release:ro" \
    -v "${TMP}/approval-valid:/approval:ro" \
    -v "${TMP}/approval-trust:/approval-trust:ro" \
    -v "${TMP}/deploy:/deploy" \
    "${DEPLOYER}" \
    >/dev/null

test -s \
    "${TMP}/deploy/deployment-record.json"

echo "[PASS] Approved release deployed"


echo
echo "[7] Direct deployment without approval denied"

mkdir -p "${TMP}/no-approval"

if docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e DEPLOYMENT_ENVIRONMENT=staging \
    -v "${TMP}/out:/release:ro" \
    -v "${TMP}/no-approval:/approval:ro" \
    -v "${TMP}/approval-trust:/approval-trust:ro" \
    -v "${TMP}/deploy:/deploy" \
    "${DEPLOYER}" \
    >/dev/null 2>&1
then
    echo "[FAIL] Deployment succeeded without approval"
    exit 1
fi

echo "[PASS] Deployment without approval rejected"


echo
echo "[8] Trusted-build correlation bypass denied"

mkdir -p "${TMP}/bypass-receipt"

docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e CORRELATION_ID="attacker-bypass-correlation" \
    -e RECEIPT_FILE=/receipt/verification-receipt.json \
    -v "${TMP}/out:/out:ro" \
    -v "${TMP}/release-trust:/trust:ro" \
    -v "${POLICY}:/policy:ro" \
    -v "${TMP}/bypass-receipt:/receipt" \
    "${VERIFIER}" \
    >/dev/null

if docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e APPROVER_ID="restech/release-approver" \
    -e DEPLOYMENT_ENVIRONMENT=staging \
    -v "${TMP}/out:/release:ro" \
    -v "${TMP}/release-trust:/release-trust:ro" \
    -v "${TMP}/bypass-receipt:/receipt:ro" \
    -v "${POLICY}:/policy:ro" \
    -v "${TMP}/approval-private:/approval-private:ro" \
    -v "${TMP}/approval-bypass:/approval" \
    "${APPROVER}" \
    >/dev/null 2>&1
then
    echo "[FAIL] Correlation-bypass release was approved"
    exit 1
fi

echo "[PASS] Trusted-build correlation bypass rejected"


echo
echo "[9] Post-approval artifact tampering denied"

rm -rf "${TMP}/tamper"
mkdir -p "${TMP}/tamper"

cp \
    "${TMP}/out/restech-release-component.tar" \
    "${TMP}/tamper/restech-release-component.tar"

printf '\nPOST-APPROVAL-TAMPER\n' \
    >> "${TMP}/tamper/restech-release-component.tar"

if docker run --rm \
    --network none \
    --user "${HOST_UID}:${HOST_GID}" \
    -e DEPLOYMENT_ENVIRONMENT=staging \
    -v "${TMP}/tamper:/release:ro" \
    -v "${TMP}/approval-valid:/approval:ro" \
    -v "${TMP}/approval-trust:/approval-trust:ro" \
    -v "${TMP}/deploy:/deploy" \
    "${DEPLOYER}" \
    >/dev/null 2>&1
then
    echo "[FAIL] Modified artifact deployed"
    exit 1
fi

echo "[PASS] Post-approval artifact modification rejected"


echo
echo "[10] Deployer cannot access approval private key"

RESULT="$(
    docker run --rm \
        --network none \
        --entrypoint python \
        "${DEPLOYER}" \
        -c '
from pathlib import Path

path = Path(
    "/approval-private/deployment-approval-key.pem"
)

print(
    "KEY_PRESENT"
    if path.exists()
    else "KEY_ISOLATED"
)
'
)"

test "${RESULT}" = "KEY_ISOLATED"

echo "[PASS] Deployment approval private key isolated from deployer"


echo
echo "[11] Approver does not receive release private key"

RESULT="$(
    docker run --rm \
        --network none \
        --entrypoint python \
        "${APPROVER}" \
        -c '
from pathlib import Path

path = Path(
    "/private/release-signing-key.pem"
)

print(
    "KEY_PRESENT"
    if path.exists()
    else "KEY_ISOLATED"
)
'
)"

test "${RESULT}" = "KEY_ISOLATED"

echo "[PASS] Release signing private key isolated from approver"


echo
echo "============================================================"
echo " PHASE 10 DEPLOYMENT APPROVAL GATE: PASS"
echo "============================================================"
