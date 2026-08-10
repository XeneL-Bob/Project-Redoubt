import base64
import hashlib
import json
import os
import time
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


RELEASE = Path("/release")

ARTIFACT = RELEASE / "restech-release-component.tar"
PROVENANCE = RELEASE / "provenance.json"
RELEASE_SIGNATURE = RELEASE / "provenance.sig"

RELEASE_PUBLIC_KEY = Path(
    "/release-trust/release-signing-public.pem"
)

VERIFICATION_RECEIPT = Path(
    "/receipt/verification-receipt.json"
)

POLICY = Path(
    "/policy/deployment-policy.json"
)

APPROVAL_PRIVATE_KEY = Path(
    "/approval-private/deployment-approval-key.pem"
)

APPROVAL_DIR = Path("/approval")

APPROVAL_FILE = (
    APPROVAL_DIR
    / "deployment-approval.json"
)

APPROVAL_SIGNATURE = (
    APPROVAL_DIR
    / "deployment-approval.sig"
)

APPROVER_ID = os.environ.get(
    "APPROVER_ID",
    "restech/release-approver",
)

DEPLOYMENT_ENVIRONMENT = os.environ.get(
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


def emit_event(
    outcome: str,
    *,
    reason: str | None = None,
    correlation_id: str | None = None,
    details: dict | None = None,
) -> None:

    if EVENTS_FILE is None:
        return

    event_details = {
        "environment":
            DEPLOYMENT_ENVIRONMENT,
        "approver":
            APPROVER_ID,
    }

    if reason is not None:
        event_details["reason"] = reason

    if details:
        event_details.update(details)

    event = {
        "source":
            "release-approver",
        "event_type":
            "deployment_approval",
        "outcome":
            outcome,
        "subject":
            APPROVER_ID,
        "resource":
            "software-deployment",
        "correlation_id":
            correlation_id
            or CORRELATION_ID,
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
        f"DEPLOYMENT APPROVAL DENIED: {message}"
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


required = (
    ARTIFACT,
    PROVENANCE,
    RELEASE_SIGNATURE,
    RELEASE_PUBLIC_KEY,
    VERIFICATION_RECEIPT,
    POLICY,
    APPROVAL_PRIVATE_KEY,
)

for item in required:
    if not item.is_file():
        deny(
            "required_object_missing",
            f"required object missing: {item.name}",
            details={
                "missing_object":
                    item.name,
            },
        )


policy = json.loads(
    POLICY.read_text(
        encoding="utf-8"
    )
)

provenance_bytes = (
    PROVENANCE.read_bytes()
)

provenance = json.loads(
    provenance_bytes
)

receipt = json.loads(
    VERIFICATION_RECEIPT.read_text(
        encoding="utf-8"
    )
)

release_public_key = (
    serialization.load_pem_public_key(
        RELEASE_PUBLIC_KEY.read_bytes()
    )
)


try:
    release_public_key.verify(
        base64.b64decode(
            RELEASE_SIGNATURE.read_text(
                encoding="utf-8"
            ).strip()
        ),
        provenance_bytes,
    )

except InvalidSignature:
    deny(
        "release_provenance_signature_invalid",
        "release provenance signature invalid",
    )


artifact_digest = sha256_file(
    ARTIFACT
)

provenance_digest = (
    provenance
    .get("artifact", {})
    .get("digest", {})
    .get("value")
)


if artifact_digest != provenance_digest:
    deny(
        "release_artifact_digest_mismatch",
        "release artifact digest mismatch",
    )


builder = (
    provenance
    .get("builder", {})
    .get("id")
)


if builder != policy["required_builder"]:
    deny(
        "untrusted_builder",
        "untrusted builder",
        details={
            "builder":
                builder,
        },
    )


if receipt.get("decision") != "ALLOW":
    deny(
        "release_verifier_not_allow",
        "release verifier did not allow release",
    )


if (
    receipt
    .get("artifact", {})
    .get("sha256")
    != artifact_digest
):
    deny(
        "verification_receipt_digest_mismatch",
        "verification receipt digest mismatch",
    )


if receipt.get("builder") != builder:
    deny(
        "verification_receipt_builder_mismatch",
        "verification receipt builder mismatch",
    )


build_correlation = (
    provenance
    .get("build", {})
    .get("correlation_id")
)

receipt_build_correlation = (
    receipt.get(
        "build_correlation_id"
    )
)

verification_correlation = (
    receipt.get(
        "verification_correlation_id"
    )
)


if policy[
    "require_correlated_trusted_build"
]:

    if not build_correlation:
        deny(
            "trusted_build_correlation_missing",
            "trusted build correlation missing",
        )

    if (
        build_correlation
        != receipt_build_correlation
    ):
        deny(
            "trusted_build_receipt_mismatch",
            "trusted build receipt mismatch",
            details={
                "build_correlation":
                    build_correlation,
                "receipt_build_correlation":
                    receipt_build_correlation,
            },
        )

    if (
        build_correlation
        != verification_correlation
    ):
        deny(
            "trusted_build_correlation_mismatch",
            "trusted build correlation mismatch",
            details={
                "build_correlation":
                    build_correlation,
                "verification_correlation":
                    verification_correlation,
            },
        )


if (
    DEPLOYMENT_ENVIRONMENT
    not in policy[
        "allowed_environments"
    ]
):
    deny(
        "deployment_environment_not_permitted",
        "deployment environment not permitted",
    )


now = int(time.time())

ttl = int(
    policy[
        "approval_ttl_seconds"
    ]
)


approval = {
    "schema":
        "project-redoubt.deployment-approval/v1",
    "decision":
        "ALLOW",
    "approver":
        APPROVER_ID,
    "environment":
        DEPLOYMENT_ENVIRONMENT,
    "artifact": {
        "name":
            ARTIFACT.name,
        "sha256":
            artifact_digest,
    },
    "builder":
        builder,
    "source": {
        "commit":
            provenance["source"]["commit"],
        "ref":
            provenance["source"]["ref"],
    },
    "correlation_id":
        build_correlation,
    "issued_at":
        now,
    "expires_at":
        now + ttl,
}


APPROVAL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


approval_bytes = (
    json.dumps(
        approval,
        indent=2,
        sort_keys=True,
    )
    + "\n"
).encode()


APPROVAL_FILE.write_bytes(
    approval_bytes
)


approval_private_key = (
    serialization.load_pem_private_key(
        APPROVAL_PRIVATE_KEY.read_bytes(),
        password=None,
    )
)


signature = (
    approval_private_key.sign(
        approval_bytes
    )
)


APPROVAL_SIGNATURE.write_text(
    base64.b64encode(
        signature
    ).decode()
    + "\n",
    encoding="utf-8",
)


emit_event(
    "allow",
    correlation_id=build_correlation,
    details={
        "artifact":
            ARTIFACT.name,
        "artifact_digest":
            artifact_digest,
        "builder":
            builder,
        "expires_at":
            now + ttl,
    },
)


print(
    json.dumps(
        {
            "decision":
                "ALLOW",
            "approver":
                APPROVER_ID,
            "environment":
                DEPLOYMENT_ENVIRONMENT,
            "artifact_sha256":
                artifact_digest,
            "correlation_id":
                build_correlation,
        },
        sort_keys=True,
    )
)
