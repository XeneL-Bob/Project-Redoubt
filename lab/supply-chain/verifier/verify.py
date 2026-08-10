import base64
import hashlib
import json
import os
import re
from pathlib import Path

from cryptography.exceptions import (
    InvalidSignature,
)

from cryptography.hazmat.primitives import (
    serialization,
)


OUT = Path("/out")

ARTIFACT = (
    OUT
    / "restech-release-component.tar"
)

PROVENANCE = (
    OUT
    / "provenance.json"
)

SIGNATURE = (
    OUT
    / "provenance.sig"
)

PUBLIC_KEY = Path(
    "/trust/release-signing-public.pem"
)

POLICY = Path(
    "/policy/release-policy.json"
)

COMPONENT = "restech-release-component"

CORRELATION_ID = os.environ.get(
    "CORRELATION_ID",
)

EVENTS_FILE_RAW = os.environ.get(
    "EVENTS_FILE",
)

EVENTS_FILE = (
    Path(EVENTS_FILE_RAW)
    if EVENTS_FILE_RAW
    else None
)

RECEIPT_FILE_RAW = os.environ.get(
    "RECEIPT_FILE"
)

RECEIPT_FILE = (
    Path(RECEIPT_FILE_RAW)
    if RECEIPT_FILE_RAW
    else None
)


def emit_event(
    outcome: str,
    *,
    reason: str | None = None,
    details: dict | None = None,
) -> None:

    if EVENTS_FILE is None:
        return

    event_details = {}

    if reason is not None:
        event_details["reason"] = reason

    if details:
        event_details.update(details)

    event = {
        "source": "release-verifier",
        "event_type":
            "release_verification",
        "outcome": outcome,
        "subject": COMPONENT,
        "resource":
            "software-release",
        "correlation_id":
            CORRELATION_ID,
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
        f"RELEASE DENIED: {message}"
    )


def sha256_file(
    path: Path,
) -> str:

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


required_files = (
    ARTIFACT,
    PROVENANCE,
    SIGNATURE,
    PUBLIC_KEY,
    POLICY,
)

for required in required_files:

    if required.is_file():
        continue

    if required == SIGNATURE:
        deny(
            "provenance_signature_missing",
            "required object missing: "
            f"{required.name}",
        )

    deny(
        "required_object_missing",
        "required object missing: "
        f"{required.name}",
        details={
            "missing_object":
                required.name,
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

public_key = (
    serialization.load_pem_public_key(
        PUBLIC_KEY.read_bytes()
    )
)


try:
    public_key.verify(
        base64.b64decode(
            SIGNATURE.read_text(
                encoding="utf-8"
            ).strip()
        ),
        provenance_bytes,
    )

except InvalidSignature:
    deny(
        "provenance_signature_invalid",
        "provenance signature invalid",
    )


artifact = provenance.get(
    "artifact",
    {},
)

digest = artifact.get(
    "digest",
    {},
)

builder = provenance.get(
    "builder",
    {},
)

source = provenance.get(
    "source",
    {},
)


if provenance.get("schema") != (
    "project-redoubt.provenance/v1"
):
    deny(
        "provenance_schema_invalid",
        "provenance schema invalid",
    )


if artifact.get("name") != (
    ARTIFACT.name
):
    deny(
        "artifact_name_mismatch",
        "artifact name mismatch",
    )


if digest.get("algorithm") != policy[
    "required_digest_algorithm"
]:
    deny(
        "digest_algorithm_not_permitted",
        "digest algorithm not permitted",
    )


actual_digest = sha256_file(
    ARTIFACT
)

expected_digest = digest.get(
    "value"
)


if actual_digest != expected_digest:
    deny(
        "artifact_digest_mismatch",
        "artifact digest mismatch",
        details={
            "expected_digest":
                expected_digest,
            "actual_digest":
                actual_digest,
        },
    )


builder_id = builder.get(
    "id"
)


if builder_id != policy[
    "required_builder"
]:
    deny(
        "untrusted_builder_identity",
        "untrusted builder identity",
        details={
            "builder":
                builder_id,
        },
    )


if (
    policy["require_clean_source"]
    and source.get("dirty") is not False
):
    deny(
        "dirty_source_provenance",
        "source repository was dirty",
    )


commit = source.get(
    "commit",
    "",
)


if (
    policy["require_source_commit"]
    and not re.fullmatch(
        r"[0-9a-fA-F]{40,64}",
        commit,
    )
):
    deny(
        "source_commit_invalid",
        "source commit invalid",
    )


if (
    policy["require_source_ref"]
    and not source.get("ref")
):
    deny(
        "source_ref_missing",
        "source ref missing",
    )


emit_event(
    "allow",
    details={
        "builder":
            builder_id,
        "artifact":
            ARTIFACT.name,
        "artifact_digest":
            actual_digest,
        "source_commit":
            commit,
        "source_ref":
            source["ref"],
    },
)


if RECEIPT_FILE is not None:
    build_correlation_id = (
        provenance.get(
            "build",
            {},
        ).get(
            "correlation_id"
        )
    )

    receipt = {
        "schema":
            "project-redoubt.verification-receipt/v1",
        "decision":
            "ALLOW",
        "artifact": {
            "name":
                ARTIFACT.name,
            "sha256":
                actual_digest,
        },
        "builder":
            builder_id,
        "source": {
            "commit":
                commit,
            "ref":
                source["ref"],
        },
        "build_correlation_id":
            build_correlation_id,
        "verification_correlation_id":
            CORRELATION_ID,
    }

    RECEIPT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RECEIPT_FILE.write_text(
        json.dumps(
            receipt,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


print(
    json.dumps(
        {
            "decision": "ALLOW",
            "artifact":
                ARTIFACT.name,
            "sha256":
                actual_digest,
            "builder":
                builder_id,
            "source_commit":
                commit,
            "source_ref":
                source["ref"],
        },
        sort_keys=True,
    )
)
