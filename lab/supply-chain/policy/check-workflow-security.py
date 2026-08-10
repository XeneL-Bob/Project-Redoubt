import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

WORKFLOW_DIR = ROOT / ".github" / "workflows"

SHA_PATTERN = re.compile(
    r"^[0-9a-f]{40}$"
)

USES_PATTERN = re.compile(
    r"^\s*(?:-\s*)?uses:\s*([^@\s]+)@([^\s#]+)"
)


def fail(message: str) -> None:
    print(
        f"[FAIL] {message}",
        file=sys.stderr,
    )
    raise SystemExit(1)


if not WORKFLOW_DIR.is_dir():
    fail(
        ".github/workflows does not exist"
    )

workflows = sorted(
    list(WORKFLOW_DIR.glob("*.yml"))
    + list(WORKFLOW_DIR.glob("*.yaml"))
)

if not workflows:
    fail(
        "No GitHub Actions workflows found"
    )

action_count = 0

for workflow in workflows:
    text = workflow.read_text(
        encoding="utf-8"
    )

    if "pull_request_target:" in text:
        fail(
            f"{workflow}: pull_request_target is prohibited"
        )

    if "permissions:" not in text:
        fail(
            f"{workflow}: explicit permissions missing"
        )

    if "contents: read" not in text:
        fail(
            f"{workflow}: contents: read baseline missing"
        )

    for line_number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        stripped = line.strip()

        if "persist-credentials: true" in stripped:
            fail(
                f"{workflow}:{line_number}: "
                "checkout credential persistence enabled"
            )

        match = USES_PATTERN.match(line)

        if not match:
            continue

        action, reference = match.groups()

        if action.startswith("./"):
            continue

        if action.startswith("docker://"):
            continue

        action_count += 1

        if not SHA_PATTERN.fullmatch(
            reference.lower()
        ):
            fail(
                f"{workflow}:{line_number}: "
                f"{action}@{reference} is not pinned "
                "to a full commit SHA"
            )

print(
    f"[PASS] {len(workflows)} workflow(s) checked"
)

print(
    f"[PASS] {action_count} external action reference(s) "
    "pinned to immutable SHAs"
)

print(
    "[PASS] pull_request_target prohibited"
)

print(
    "[PASS] explicit least-privilege permissions present"
)
