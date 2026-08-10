import os
import time
import uuid
from typing import Any

import httpx
import jwt

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
)

from jwt import PyJWKClient
from pydantic import BaseModel, Field


app = FastAPI(
    title="Project Redoubt Privilege Broker",
    version="0.1.0",
)


KEYCLOAK_ISSUER = os.environ[
    "KEYCLOAK_ISSUER"
]

KEYCLOAK_JWKS_URL = os.environ[
    "KEYCLOAK_JWKS_URL"
]

EXPECTED_AZP = os.environ[
    "EXPECTED_AZP"
]

ELEVATION_SIGNING_KEY = os.environ[
    "ELEVATION_SIGNING_KEY"
]

ELEVATION_ISSUER = os.environ.get(
    "ELEVATION_ISSUER",
    "project-redoubt-privilege-broker",
)

ELEVATION_AUDIENCE = os.environ.get(
    "ELEVATION_AUDIENCE",
    "project-redoubt-management-plane",
)

MAX_ELEVATION_TTL_SECONDS = int(
    os.environ.get(
        "MAX_ELEVATION_TTL_SECONDS",
        "120",
    )
)

TELEMETRY_URL = os.environ[
    "TELEMETRY_URL"
]

TELEMETRY_INGEST_TOKEN = os.environ[
    "TELEMETRY_INGEST_TOKEN"
]


jwks = PyJWKClient(
    KEYCLOAK_JWKS_URL
)


DOMAIN_POLICY = {
    "infrastructure": {
        "role":
            "infrastructure-admin",
        "resource":
            "infrastructure-management",
        "actions": [
            "read",
            "restart-service",
        ],
    },
    "security": {
        "role":
            "security-admin",
        "resource":
            "security-management",
        "actions": [
            "read",
            "update-detection",
        ],
    },
}


class ElevationRequest(BaseModel):
    ttl_seconds: int = Field(
        default=120,
        ge=1,
    )


async def emit_event(
    outcome: str,
    subject: str,
    domain: str,
    details: dict[str, Any],
    correlation_id: str,
) -> None:
    payload = {
        "source":
            "privilege-broker",
        "event_type":
            "privileged_elevation",
        "outcome":
            outcome,
        "subject":
            subject,
        "resource":
            domain,
        "correlation_id":
            correlation_id,
        "details":
            details,
    }

    try:
        async with httpx.AsyncClient(
            timeout=1.5
        ) as client:
            await client.post(
                f"{TELEMETRY_URL}/event",
                json=payload,
                headers={
                    "X-Redoubt-Telemetry-Token":
                        TELEMETRY_INGEST_TOKEN
                },
            )

    except Exception:
        print(
            "telemetry_delivery_failed",
            payload,
        )


def bearer_token(
    authorization: str | None,
) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing bearer token",
        )

    scheme, _, token = (
        authorization.partition(" ")
    )

    if (
        scheme.lower() != "bearer"
        or not token
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    return token


def validate_token(
    token: str,
) -> dict[str, Any]:
    try:
        signing_key = (
            jwks.get_signing_key_from_jwt(
                token
            )
        )

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            options={
                "verify_aud": False,
            },
            leeway=5,
        )

        if (
            claims.get("azp")
            != EXPECTED_AZP
        ):
            raise HTTPException(
                status_code=401,
                detail=(
                    "Token was not issued "
                    "to the privileged "
                    "administration client"
                ),
            )

        return claims

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=(
                "Privileged token "
                f"validation failed: "
                f"{type(exc).__name__}"
            ),
        ) from exc


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "component":
            "privilege-broker",
    }


@app.post("/elevate/{domain}")
async def elevate(
    domain: str,
    request: ElevationRequest,
    authorization:
        str | None = Header(default=None),
    x_admin_device_trusted:
        str = Header(default="false"),
):
    token = bearer_token(
        authorization
    )

    claims = validate_token(
        token
    )

    username = claims.get(
        "preferred_username",
        "unknown",
    )

    roles = claims.get(
        "realm_access",
        {},
    ).get(
        "roles",
        [],
    )

    correlation_id = str(
        uuid.uuid4()
    )

    policy = DOMAIN_POLICY.get(
        domain
    )

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Unknown privileged domain",
        )

    trusted = (
        x_admin_device_trusted.lower()
        == "true"
    )

    if not trusted:
        await emit_event(
            "deny",
            username,
            domain,
            {
                "reason":
                    "untrusted_admin_device",
            },
            correlation_id,
        )

        raise HTTPException(
            status_code=403,
            detail=(
                "Privileged elevation "
                "requires trusted admin device"
            ),
        )

    required_role = policy[
        "role"
    ]

    if required_role not in roles:
        await emit_event(
            "deny",
            username,
            domain,
            {
                "reason":
                    "missing_privileged_role",
                "required_role":
                    required_role,
            },
            correlation_id,
        )

        raise HTTPException(
            status_code=403,
            detail=(
                "Identity is not eligible "
                "for this privileged domain"
            ),
        )

    if (
        request.ttl_seconds
        > MAX_ELEVATION_TTL_SECONDS
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Requested elevation "
                "duration exceeds policy"
            ),
        )

    now = int(
        time.time()
    )

    grant_id = str(
        uuid.uuid4()
    )

    grant_claims = {
        "iss":
            ELEVATION_ISSUER,
        "aud":
            ELEVATION_AUDIENCE,
        "sub":
            username,
        "jti":
            grant_id,
        "iat":
            now,
        "nbf":
            now,
        "exp":
            now
            + request.ttl_seconds,
        "domain":
            domain,
        "resource":
            policy["resource"],
        "actions":
            policy["actions"],
        "admin_device_trusted":
            True,
    }

    elevation_grant = jwt.encode(
        grant_claims,
        ELEVATION_SIGNING_KEY,
        algorithm="HS256",
    )

    await emit_event(
        "allow",
        username,
        domain,
        {
            "grant_id":
                grant_id,
            "resource":
                policy["resource"],
            "actions":
                policy["actions"],
            "ttl_seconds":
                request.ttl_seconds,
        },
        correlation_id,
    )

    return {
        "elevation_grant":
            elevation_grant,
        "grant_id":
            grant_id,
        "subject":
            username,
        "domain":
            domain,
        "resource":
            policy["resource"],
        "actions":
            policy["actions"],
        "expires_in":
            request.ttl_seconds,
    }
