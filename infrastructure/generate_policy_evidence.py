#!/usr/bin/env python3

import hashlib
import json
import os
import subprocess
import sys

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path


INFRASTRUCTURE = (
    Path(__file__)
    .resolve()
    .parent
)

REPO = (
    INFRASTRUCTURE
    .parent
)

POLICY = (
    INFRASTRUCTURE
    / "policies"
    / "iac-security.rego"
)

LOCKFILE = (
    INFRASTRUCTURE
    / "environments"
    / "reference-aws"
    / ".terraform.lock.hcl"
)

sys.path.insert(
    0,
    str(INFRASTRUCTURE),
)

from policy_evaluate import evaluate_plan


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def command_output(command):
    proc = subprocess.run(
        command,
        cwd=REPO,
        text=True,
        capture_output=True,
    )

    if proc.returncode != 0:
        return "unknown"

    return proc.stdout.strip()


def git_value(
    env_name,
    git_command,
):
    value = os.environ.get(
        env_name
    )

    if value:
        return value

    return command_output(
        git_command
    )


def main():
    if len(sys.argv) not in (
        2,
        3,
    ):
        raise SystemExit(
            "Usage: generate_policy_evidence.py "
            "<plan.json> [evidence.json]"
        )

    plan_path = Path(
        sys.argv[1]
    ).resolve()

    if len(sys.argv) == 3:
        evidence_path = Path(
            sys.argv[2]
        ).resolve()
    else:
        evidence_path = (
            INFRASTRUCTURE
            / "runtime"
            / "policy-evidence.json"
        )

    if not plan_path.is_file():
        raise SystemExit(
            f"[FAIL] Plan not found: {plan_path}"
        )

    if not POLICY.is_file():
        raise SystemExit(
            f"[FAIL] Policy not found: {POLICY}"
        )

    if not LOCKFILE.is_file():
        raise SystemExit(
            f"[FAIL] Provider lockfile not found: {LOCKFILE}"
        )

    plan = json.loads(
        plan_path.read_text(
            encoding="utf-8"
        )
    )

    violations = evaluate_plan(
        plan
    )

    decision = (
        "ALLOW"
        if not violations
        else "DENY"
    )

    tofu_version = (
        command_output(
            [
                "tofu",
                "version",
            ]
        )
        .splitlines()[0]
    )

    evidence = {
        "schema":
            "project-redoubt.iac-policy-evidence/v1",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "project":
            "Project Redoubt",

        "organisation":
            "ResTech",

        "phase":
            "Phase 11",

        "control":
            "Infrastructure Policy Gate",

        "source": {
            "commit":
                git_value(
                    "GITHUB_SHA",
                    [
                        "git",
                        "rev-parse",
                        "HEAD",
                    ],
                ),

            "ref":
                git_value(
                    "GITHUB_REF",
                    [
                        "git",
                        "branch",
                        "--show-current",
                    ],
                ),
        },

        "toolchain": {
            "opentofu":
                tofu_version,

            "opa":
                "openpolicyagent/opa:1.17.0",
        },

        "inputs": {
            "plan": {
                "path":
                    str(
                        plan_path.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    sha256_file(
                        plan_path
                    ),
            },

            "policy": {
                "path":
                    str(
                        POLICY.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    sha256_file(
                        POLICY
                    ),
            },

            "provider_lock": {
                "path":
                    str(
                        LOCKFILE.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    sha256_file(
                        LOCKFILE
                    ),
            },
        },

        "decision":
            decision,

        "violation_count":
            len(
                violations
            ),

        "violations":
            violations,
    }

    evidence_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    evidence_path.write_text(
        json.dumps(
            evidence,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "==============================================="
    )

    print(
        " PROJECT REDOUBT — IaC POLICY EVIDENCE"
    )

    print(
        "==============================================="
    )

    print()
    print(
        f"Decision: {decision}"
    )

    print(
        "Plan SHA256: "
        + evidence[
            "inputs"
        ][
            "plan"
        ][
            "sha256"
        ]
    )

    print(
        "Policy SHA256: "
        + evidence[
            "inputs"
        ][
            "policy"
        ][
            "sha256"
        ]
    )

    print(
        "Provider Lock SHA256: "
        + evidence[
            "inputs"
        ][
            "provider_lock"
        ][
            "sha256"
        ]
    )

    print()
    print(
        f"Evidence: {evidence_path}"
    )

    if violations:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
