import base64
import hashlib
import json
import re
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


OUT = Path("/out")

ARTIFACT = OUT / "restech-release-component.tar"
PROVENANCE = OUT / "provenance.json"
SIGNATURE = OUT / "provenance.sig"

PUBLIC_KEY = Path(
    "/trust/release-signing-public.pem"
)

POLICY = Path(
    "/policy/release-policy.json"
)


def deny(reason: str) -> None:
    raise SystemExit(
        f"RELEASE DENIED: {reason}"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


for required in (
    ARTIFACT,
    PROVENANCE,
    SIGNATURE,
    PUBLIC_KEY,
    POLICY,
):
    if not required.is_file():
        deny(
            f"required object missing: {required.name}"
        )

policy = json.loads(
    POLICY.read_text(
        encoding="utf-8"
    )
)

provenance_bytes = PROVENANCE.read_bytes()

provenance = json.loads(
    provenance_bytes
)

public_key = serialization.load_pem_public_key(
    PUBLIC_KEY.read_bytes()
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
        "provenance signature invalid"
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
        "provenance schema invalid"
    )

if artifact.get("name") != ARTIFACT.name:
    deny(
        "artifact name mismatch"
    )

if digest.get("algorithm") != policy[
    "required_digest_algorithm"
]:
    deny(
        "digest algorithm not permitted"
    )

actual_digest = sha256_file(
    ARTIFACT
)

if actual_digest != digest.get("value"):
    deny(
        "artifact digest mismatch"
    )

if builder.get("id") != policy[
    "required_builder"
]:
    deny(
        "untrusted builder identity"
    )

if (
    policy["require_clean_source"]
    and source.get("dirty") is not False
):
    deny(
        "source repository was dirty"
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
        "source commit invalid"
    )

if (
    policy["require_source_ref"]
    and not source.get("ref")
):
    deny(
        "source ref missing"
    )

print(
    json.dumps(
        {
            "decision": "ALLOW",
            "artifact": ARTIFACT.name,
            "sha256": actual_digest,
            "builder": builder["id"],
            "source_commit": commit,
            "source_ref": source["ref"],
        },
        sort_keys=True,
    )
)
