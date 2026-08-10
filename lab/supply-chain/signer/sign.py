import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization


PROVENANCE = Path("/out/provenance.json")

PRIVATE_KEY = Path(
    "/private/release-signing-key.pem"
)

SIGNATURE = Path(
    "/out/provenance.sig"
)

if not PROVENANCE.is_file():
    raise SystemExit(
        "SIGNING DENIED: provenance missing"
    )

if not PRIVATE_KEY.is_file():
    raise SystemExit(
        "SIGNING DENIED: signing key missing"
    )

private_key = serialization.load_pem_private_key(
    PRIVATE_KEY.read_bytes(),
    password=None,
)

signature = private_key.sign(
    PROVENANCE.read_bytes()
)

SIGNATURE.write_text(
    base64.b64encode(signature).decode("ascii")
    + "\n",
    encoding="utf-8",
)

print("PROVENANCE SIGNED")
