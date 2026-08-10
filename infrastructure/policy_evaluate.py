#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(
    __file__
).resolve().parents[1]

POLICY = (
    ROOT
    / "infrastructure"
    / "policies"
    / "iac-security.rego"
)

OPA_IMAGE = "openpolicyagent/opa:1.17.0"

QUERY = "data.redoubt.iac.security.deny"


def evaluate_plan(plan):
    command = [
        "docker",
        "run",
        "--rm",
        "-i",
        "-v",
        f"{POLICY}:/policy/iac-security.rego:ro",
        OPA_IMAGE,
        "eval",
        "--format=json",
        "--data",
        "/policy/iac-security.rego",
        "--stdin-input",
        QUERY,
    ]

    proc = subprocess.run(
        command,
        input=json.dumps(plan),
        text=True,
        capture_output=True,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            "OPA evaluation failed:\n"
            + proc.stderr
        )

    result = json.loads(
        proc.stdout
    )

    rows = result.get(
        "result",
        [],
    )

    if not rows:
        return []

    expressions = rows[0].get(
        "expressions",
        [],
    )

    if not expressions:
        return []

    violations = expressions[0].get(
        "value",
        [],
    )

    return sorted(
        violations,
        key=lambda item: (
            item.get("id", ""),
            item.get("resource", ""),
        ),
    )


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: policy_evaluate.py <plan.json>"
        )

    plan_path = Path(
        sys.argv[1]
    )

    if not plan_path.is_file():
        raise SystemExit(
            f"[FAIL] Plan not found: {plan_path}"
        )

    plan = json.loads(
        plan_path.read_text(
            encoding="utf-8"
        )
    )

    violations = evaluate_plan(
        plan
    )

    print(
        "==============================================="
    )
    print(
        " PROJECT REDOUBT — IaC POLICY EVALUATION"
    )
    print(
        "==============================================="
    )

    if not violations:
        print()
        print(
            "[ALLOW] Infrastructure plan satisfies "
            "Project Redoubt security policy"
        )
        return 0

    print()

    for violation in violations:
        print(
            f"[DENY] {violation['id']} "
            f"{violation['resource']}"
        )

        print(
            f"       {violation['message']}"
        )

    print()
    print(
        f"[DENY] {len(violations)} "
        "security policy violation(s)"
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
