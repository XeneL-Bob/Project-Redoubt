import base64
import hashlib
import json
import os
import shutil
import time
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


RELEASE = Path("/release")

ARTIFACT = (
    RELEASE
    / "restech-release-component.tar"
)

APPROVAL = Path(
    "/approval/deployment-approval.json"
)

APPROVAL_SIGNATURE = Path(
    "/approval/deployment-approval.sig"
)

APPROVAL_PUBLIC_KEY = Path(
    "/approval-trust/deployment-approval-public.pem"
)

DEPLOY = Path("/deploy")

TARGET_ENVIRONMENT = os.environ.get(
    "DEPLOYMENT_ENVIRONMENT",
    "staging",
)

CORRELATION_ID = os.environ.get(
    "CORRELATION_ID"
)

EVENTS_FILE_RAW = os.environ.get(
    "EVENTS_FILE"
)

EVENTS_FILE = (
    Path(EVENTS_FILE_RAW)
    if EVENTS_FILE_RAW
    else None
)


def approval_correlation():
    if CORRELATION_ID:
        return CORRELATION_ID

    if not APPROVAL.is_file():
        return None

    try:
        return json.loads(
            APPROVAL.read_text(
                encoding="utf-8"
            )
        ).get(
            "correlation_id"
        )

    except Exception:
        return None


def emit_event(
    outcome: str,
    *,
    reason: str | None = None,
    details: dict | None = None,
) -> None:

    if EVENTS_FILE is None:
        return

    event_details = {
        "environment":
            TARGET_ENVIRONMENT,
    }

    if reason is not None:
        event_details["reason"] = reason

    if details:
        event_details.update(details)

    event = {
        "source":
            "deployment-gate",
        "event_type":
            "deployment_decision",
        "outcome":
            outcome,
        "subject":
            "project-redoubt-deployer",
        "resource":
            "software-deployment",
        "correlation_id":
            approval_correlation(),
        "details":
            event_details,
    }

    EVENTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with EVENTS_FILE.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json.dumps(
                event,
                sort_keys=True,
            )
            + "\n"
        )


def deny(
    reason: str,
    message: str,
    *,
    details: dict | None = None,
) -> None:

    emit_event(
        "deny",
        reason=reason,
        details=details,
    )

    raise SystemExit(
        f"DEPLOYMENT DENIED: {message}"
    )


def sha256_file(path: Path) -> str:
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


for item in (
    ARTIFACT,
    APPROVAL,
    APPROVAL_SIGNATURE,
    APPROVAL_PUBLIC_KEY,
):
    if not item.is_file():
        deny(
            "required_object_missing",
            f"required object missing: {item.name}",
            details={
                "missing_object":
                    item.name,
            },
        )


approval_bytes = (
    APPROVAL.read_bytes()
)

approval = json.loads(
    approval_bytes
)


public_key = (
    serialization.load_pem_public_key(
        APPROVAL_PUBLIC_KEY.read_bytes()
    )
)


try:
    public_key.verify(
        base64.b64decode(
            APPROVAL_SIGNATURE.read_text(
                encoding="utf-8"
            ).strip()
        ),
        approval_bytes,
    )

except InvalidSignature:
    deny(
        "approval_signature_invalid",
        "deployment approval signature invalid",
    )


if approval.get("decision") != "ALLOW":
    deny(
        "deployment_approval_not_allow",
        "deployment approval is not ALLOW",
    )


if (
    approval.get("environment")
    != TARGET_ENVIRONMENT
):
    deny(
        "approval_environment_mismatch",
        "deployment approval environment mismatch",
    )


now = int(time.time())


if now > int(
    approval.get(
        "expires_at",
        0,
    )
):
    deny(
        "approval_expired",
        "deployment approval expired",
    )


actual_digest = sha256_file(
    ARTIFACT
)

approved_digest = (
    approval
    .get("artifact", {})
    .get("sha256")
)


if actual_digest != approved_digest:
    deny(
        "artifact_differs_from_approved_release",
        "artifact differs from approved release",
        details={
            "approved_digest":
                approved_digest,
            "actual_digest":
                actual_digest,
        },
    )


DEPLOY.mkdir(
    parents=True,
    exist_ok=True,
)


destination = (
    DEPLOY
    / ARTIFACT.name
)


shutil.copyfile(
    ARTIFACT,
    destination,
)


record = {
    "schema":
        "project-redoubt.deployment-record/v1",
    "status":
        "DEPLOYED",
    "environment":
        TARGET_ENVIRONMENT,
    "artifact": {
        "name":
            ARTIFACT.name,
        "sha256":
            actual_digest,
    },
    "approver":
        approval["approver"],
    "source":
        approval["source"],
    "correlation_id":
        approval["correlation_id"],
}


(
    DEPLOY
    / "deployment-record.json"
).write_text(
    json.dumps(
        record,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


emit_event(
    "allow",
    details={
        "artifact":
            ARTIFACT.name,
        "artifact_digest":
            actual_digest,
        "approver":
            approval["approver"],
    },
)


print(
    json.dumps(
        record,
        sort_keys=True,
    )
)
