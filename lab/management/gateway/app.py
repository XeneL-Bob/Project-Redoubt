import os
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


app = FastAPI(
    title="Project Redoubt Management PEP",
    version="0.2.0",
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

ADMIN_OPA_DECISION_URL = os.environ[
    "ADMIN_OPA_DECISION_URL"
]

MANAGEMENT_API_URL = os.environ[
    "MANAGEMENT_API_URL"
]

MANAGEMENT_GATEWAY_TOKEN = os.environ[
    "MANAGEMENT_GATEWAY_TOKEN"
]

ELEVATION_SIGNING_KEY = os.environ[
    "ELEVATION_SIGNING_KEY"
]

ELEVATION_ISSUER = os.environ[
    "ELEVATION_ISSUER"
]

ELEVATION_AUDIENCE = os.environ[
    "ELEVATION_AUDIENCE"
]

TELEMETRY_URL = os.environ[
    "TELEMETRY_URL"
]

TELEMETRY_INGEST_TOKEN = os.environ[
    "TELEMETRY_INGEST_TOKEN"
]


jwks = PyJWKClient(
    KEYCLOAK_JWKS_URL
)


async def emit_event(
    event_type: str,
    outcome: str,
    subject: str | None,
    resource: str,
    details: dict[str, Any],
    correlation_id: str,
) -> None:
    payload = {
        "source":
            "management-gateway",
        "event_type":
            event_type,
        "outcome":
            outcome,
        "subject":
            subject,
        "resource":
            resource,
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


def validate_elevation_grant(
    grant: str | None,
    username: str,
    resource: str,
    action: str,
) -> dict[str, Any]:
    if not grant:
        raise HTTPException(
            status_code=403,
            detail=(
                "Active JIT elevation "
                "grant required"
            ),
        )

    try:
        claims = jwt.decode(
            grant,
            ELEVATION_SIGNING_KEY,
            algorithms=["HS256"],
            issuer=ELEVATION_ISSUER,
            audience=ELEVATION_AUDIENCE,
            leeway=1,
        )

    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=403,
            detail="JIT elevation grant expired",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=(
                "Invalid JIT elevation grant"
            ),
        ) from exc

    if claims.get("sub") != username:
        raise HTTPException(
            status_code=403,
            detail=(
                "Elevation grant subject "
                "does not match identity"
            ),
        )

    if claims.get("resource") != resource:
        raise HTTPException(
            status_code=403,
            detail=(
                "Elevation grant does not "
                "cover requested resource"
            ),
        )

    actions = claims.get(
        "actions",
        [],
    )

    if action not in actions:
        raise HTTPException(
            status_code=403,
            detail=(
                "Elevation grant does not "
                "cover requested action"
            ),
        )

    if (
        claims.get(
            "admin_device_trusted"
        )
        is not True
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Elevation grant lacks "
                "trusted-device context"
            ),
        )

    return claims


async def authorize(
    claims: dict[str, Any],
    resource: str,
    action: str,
    admin_device_trusted: bool,
    elevation_grant_id: str,
    correlation_id: str,
) -> None:
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

    payload = {
        "input": {
            "subject": {
                "username":
                    username,
                "roles":
                    roles,
            },
            "resource":
                resource,
            "action":
                action,
            "context": {
                "admin_device_trusted":
                    admin_device_trusted,
                "elevation_active":
                    True,
                "elevation_grant_id":
                    elevation_grant_id,
            },
        }
    }

    try:
        async with httpx.AsyncClient(
            timeout=2.0
        ) as client:
            response = await client.post(
                ADMIN_OPA_DECISION_URL,
                json=payload,
            )

            response.raise_for_status()

        decision = response.json().get(
            "result"
        )

        if not decision:
            raise RuntimeError(
                "Admin OPA returned no decision"
            )

    except Exception as exc:
        await emit_event(
            "privileged_policy_decision",
            "error",
            username,
            resource,
            {
                "action":
                    action,
                "error":
                    type(exc).__name__,
            },
            correlation_id,
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Privileged policy "
                "decision unavailable"
            ),
        ) from exc

    allowed = bool(
        decision.get(
            "allow",
            False,
        )
    )

    await emit_event(
        "privileged_policy_decision",
        "allow" if allowed else "deny",
        username,
        resource,
        {
            "action":
                action,
            "admin_device_trusted":
                admin_device_trusted,
            "elevation_active":
                True,
            "elevation_grant_id":
                elevation_grant_id,
            "roles":
                roles,
            "reason":
                decision.get("reason"),
        },
        correlation_id,
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail=(
                "Privileged access denied "
                "by Project Redoubt policy"
            ),
        )


async def call_backend(
    method: str,
    path: str,
    username: str,
    correlation_id: str,
) -> dict[str, Any]:
    headers = {
        "X-Redoubt-Management-Token":
            MANAGEMENT_GATEWAY_TOKEN,
        "X-Redoubt-Admin":
            username,
        "X-Redoubt-Correlation-ID":
            correlation_id,
    }

    async with httpx.AsyncClient(
        timeout=5.0
    ) as client:
        response = await client.request(
            method,
            f"{MANAGEMENT_API_URL}{path}",
            headers=headers,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=(
                "Protected management "
                "request failed"
            ),
        )

    return response.json()


async def privileged_request(
    authorization: str | None,
    elevation_grant: str | None,
    admin_device_trusted: str,
    resource: str,
    action: str,
    method: str,
    backend_path: str,
):
    token = bearer_token(
        authorization
    )

    identity_claims = validate_token(
        token
    )

    username = identity_claims.get(
        "preferred_username",
        "unknown",
    )

    grant_claims = (
        validate_elevation_grant(
            elevation_grant,
            username,
            resource,
            action,
        )
    )

    device_trusted = (
        admin_device_trusted.lower()
        == "true"
    )

    correlation_id = str(
        uuid.uuid4()
    )

    await authorize(
        identity_claims,
        resource,
        action,
        device_trusted,
        grant_claims["jti"],
        correlation_id,
    )

    return await call_backend(
        method,
        backend_path,
        username,
        correlation_id,
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "component":
            "management-policy-enforcement-point",
    }


@app.get("/infrastructure/status")
async def infrastructure_status(
    authorization:
        str | None = Header(default=None),
    x_redoubt_elevation_grant:
        str | None = Header(default=None),
    x_admin_device_trusted:
        str = Header(default="false"),
):
    return await privileged_request(
        authorization,
        x_redoubt_elevation_grant,
        x_admin_device_trusted,
        "infrastructure-management",
        "read",
        "GET",
        "/infrastructure/status",
    )


@app.post("/infrastructure/restart-service")
async def restart_service(
    authorization:
        str | None = Header(default=None),
    x_redoubt_elevation_grant:
        str | None = Header(default=None),
    x_admin_device_trusted:
        str = Header(default="false"),
):
    return await privileged_request(
        authorization,
        x_redoubt_elevation_grant,
        x_admin_device_trusted,
        "infrastructure-management",
        "restart-service",
        "POST",
        "/infrastructure/restart-service",
    )


@app.get("/security/status")
async def security_status(
    authorization:
        str | None = Header(default=None),
    x_redoubt_elevation_grant:
        str | None = Header(default=None),
    x_admin_device_trusted:
        str = Header(default="false"),
):
    return await privileged_request(
        authorization,
        x_redoubt_elevation_grant,
        x_admin_device_trusted,
        "security-management",
        "read",
        "GET",
        "/security/status",
    )


@app.post("/security/update-detection")
async def update_detection(
    authorization:
        str | None = Header(default=None),
    x_redoubt_elevation_grant:
        str | None = Header(default=None),
    x_admin_device_trusted:
        str = Header(default="false"),
):
    return await privileged_request(
        authorization,
        x_redoubt_elevation_grant,
        x_admin_device_trusted,
        "security-management",
        "update-detection",
        "POST",
        "/security/update-detection",
    )
