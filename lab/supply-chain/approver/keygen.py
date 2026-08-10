from pathlib import Path

from cryptography.hazmat.primitives import (
    serialization,
)

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


PRIVATE = Path(
    "/approval-private/deployment-approval-key.pem"
)

PUBLIC = Path(
    "/approval-trust/deployment-approval-public.pem"
)


PRIVATE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

PUBLIC.parent.mkdir(
    parents=True,
    exist_ok=True,
)


private_key = Ed25519PrivateKey.generate()

public_key = private_key.public_key()


PRIVATE.write_bytes(
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
)

PUBLIC.write_bytes(
    public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
)


print(
    "DEPLOYMENT APPROVAL KEY GENERATED"
)
