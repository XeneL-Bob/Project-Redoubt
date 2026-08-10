from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


PRIVATE_PATH = Path(
    "/private/release-signing-key.pem"
)

PUBLIC_PATH = Path(
    "/trust/release-signing-public.pem"
)

PRIVATE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

PUBLIC_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

private_key = Ed25519PrivateKey.generate()

PRIVATE_PATH.write_bytes(
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
)

PUBLIC_PATH.write_bytes(
    private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
)

print("SUPPLY CHAIN SIGNING KEY GENERATED")
