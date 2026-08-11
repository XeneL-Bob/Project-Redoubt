#!/usr/bin/env bash

set -euo pipefail


ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd
)"

INFRA="${ROOT}/infrastructure"

REFERENCE="$(
    cd "${INFRA}/environments/reference-aws"
    pwd
)"

RUNTIME="${INFRA}/runtime/ci"

PLAN="${RUNTIME}/reference.tfplan"

PLAN_JSON="${RUNTIME}/reference-plan.json"

EVIDENCE="${RUNTIME}/policy-evidence.json"

MANIFEST="${RUNTIME}/policy-evidence.sha256"


export AWS_ACCESS_KEY_ID="project-redoubt-reference"

export AWS_SECRET_ACCESS_KEY="project-redoubt-reference"

export AWS_EC2_METADATA_DISABLED="true"


mkdir -p \
    "${RUNTIME}"


echo "============================================================"
echo " PROJECT REDOUBT — IaC SECURITY GATE"
echo "============================================================"


echo
echo "[1] OpenTofu formatting"

tofu fmt \
    -check \
    -recursive \
    "${INFRA}"

echo "[PASS] OpenTofu formatting"


echo
echo "[2] Provider dependency lock"

test -s \
    "${REFERENCE}/.terraform.lock.hcl"

echo "[PASS] Provider lockfile present"


echo
echo "[3] OpenTofu initialisation"

(
    cd "${REFERENCE}"

    tofu init \
        -backend=false \
        -input=false \
        -lockfile=readonly
)

echo "[PASS] OpenTofu initialised with locked providers"


echo
echo "[4] OpenTofu validation"

(
    cd "${REFERENCE}"

    tofu validate
)

echo "[PASS] Infrastructure configuration valid"


echo
echo "[5] Generate compliant reference plan"

(
    cd "${REFERENCE}"

    tofu plan \
        -refresh=false \
        -input=false \
        -lock=false \
        -var security_test_scenario=none \
        -out="${PLAN}"
)

(
    cd "${REFERENCE}"

    tofu show \
        -json \
        "${PLAN}" \
        > "${PLAN_JSON}"
)

echo "[PASS] Reference plan generated"


echo
echo "[6] Generate policy decision evidence"

set +e

python3 \
    "${INFRA}/generate_policy_evidence.py" \
    "${PLAN_JSON}" \
    "${EVIDENCE}"

POLICY_RESULT="$?"

set -e


sha256sum \
    "${EVIDENCE}" \
    "${INFRA}/policies/iac-security.rego" \
    "${REFERENCE}/.terraform.lock.hcl" \
    > "${MANIFEST}"


if [[ "${POLICY_RESULT}" -ne 0 ]]; then
    echo
    echo "[FAIL] Reference architecture rejected by policy"
    exit "${POLICY_RESULT}"
fi

echo "[PASS] Reference architecture ALLOW"


echo
echo "[7] Policy unit validation"

python3 \
    "${INFRA}/tests/policy-test.py"


echo
echo "[8] Real OpenTofu attack-plan validation"

python3 \
    "${INFRA}/tests/real-plan-test.py"


echo
echo "[9] Evidence integrity"

sha256sum \
    --check \
    "${MANIFEST}" \
    >/dev/null

echo "[PASS] Policy evidence integrity verified"


echo
echo "============================================================"
echo " PHASE 11 IaC SECURITY GATE: PASS"
echo "============================================================"
