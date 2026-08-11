#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path


INFRASTRUCTURE = (
    Path(__file__)
    .resolve()
    .parents[1]
)

REPO = INFRASTRUCTURE.parent

REFERENCE = (
    INFRASTRUCTURE
    / "environments"
    / "reference-aws"
)

RUNTIME = (
    INFRASTRUCTURE
    / "runtime"
    / "real-plan-tests"
)

sys.path.insert(
    0,
    str(INFRASTRUCTURE),
)

from policy_evaluate import evaluate_plan


SCENARIOS = {
    "public-http": {
        "IAC-001",
    },

    "public-ssh": {
        "IAC-001",
        "IAC-002",
    },

    "management-public-ip": {
        "IAC-003",
    },

    "private-default-route": {
        "IAC-004",
    },

    "evidence-public-access": {
        "IAC-005",
    },

    "evidence-no-kms": {
        "IAC-006",
    },

    "evidence-versioning-off": {
        "IAC-007",
    },

    "kms-rotation-off": {
        "IAC-008",
    },

    "flow-logs-incomplete": {
        "IAC-009",
    },

    "missing-security-tags": {
        "IAC-010",
    },

    "unrestricted-egress": {
        "IAC-011",
    },
}


ENV = os.environ.copy()

ENV.update(
    {
        "AWS_ACCESS_KEY_ID":
            "project-redoubt-reference",

        "AWS_SECRET_ACCESS_KEY":
            "project-redoubt-reference",

        "AWS_EC2_METADATA_DISABLED":
            "true",
    }
)


def run(
    command,
    *,
    capture=False,
):
    return subprocess.run(
        command,
        cwd=REFERENCE,
        env=ENV,
        text=True,
        capture_output=capture,
    )


def create_plan(
    scenario,
):
    RUNTIME.mkdir(
        parents=True,
        exist_ok=True,
    )

    plan_path = (
        RUNTIME
        / f"{scenario}.tfplan"
    )

    json_path = (
        RUNTIME
        / f"{scenario}.json"
    )

    proc = run(
        [
            "tofu",
            "plan",
            "-refresh=false",
            "-input=false",
            "-lock=false",
            "-var",
            (
                "security_test_scenario="
                f"{scenario}"
            ),
            "-out",
            str(plan_path),
        ],
        capture=True,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            f"OpenTofu plan failed for {scenario}\n"
            + proc.stdout
            + proc.stderr
        )

    proc = run(
        [
            "tofu",
            "show",
            "-json",
            str(plan_path),
        ],
        capture=True,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            f"OpenTofu JSON conversion failed for {scenario}\n"
            + proc.stdout
            + proc.stderr
        )

    json_path.write_text(
        proc.stdout,
        encoding="utf-8",
    )

    return json.loads(
        proc.stdout
    )


def violation_ids(
    plan,
):
    return {
        item["id"]
        for item in evaluate_plan(
            plan
        )
    }


def assert_result(
    scenario,
    expected,
):
    plan = create_plan(
        scenario
    )

    actual = violation_ids(
        plan
    )

    if actual != expected:
        raise AssertionError(
            f"{scenario}: expected "
            f"{sorted(expected)}, "
            f"received {sorted(actual)}"
        )

    print(
        "[PASS] "
        f"{scenario:<28} "
        + ", ".join(
            sorted(actual)
        )
    )


print(
    "============================================================"
)

print(
    " PROJECT REDOUBT — REAL IaC MISCONFIGURATION VALIDATION"
)

print(
    "============================================================"
)


print()
print(
    "[Baseline] Compliant reference architecture"
)

baseline = create_plan(
    "none"
)

baseline_violations = (
    violation_ids(
        baseline
    )
)

if baseline_violations:
    raise AssertionError(
        "Compliant reference plan unexpectedly denied: "
        + str(
            sorted(
                baseline_violations
            )
        )
    )

print(
    "[PASS] reference architecture ALLOW"
)


print()
print(
    "[Adversarial infrastructure changes]"
)

for scenario, expected in SCENARIOS.items():
    assert_result(
        scenario,
        expected,
    )


print()
print(
    "============================================================"
)

print(
    " PHASE 11 REAL IaC MISCONFIGURATION TESTS: PASS"
)

print(
    "============================================================"
)
