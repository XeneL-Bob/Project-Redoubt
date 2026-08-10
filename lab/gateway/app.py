import os
from typing import Any

import httpx
import jwt
from fastapi import FastAPI, Header, HTTPException
from jwt import PyJWKClient

app = FastAPI(
    title="Project Redoubt Policy Enforcement Gateway",
    version="0.1.0",
)

KEYCLOAK_ISSUER = os.environ["KEYCLOAK_ISSUER"]
KEYCLOAK_JWKS_URL = os.environ["KEYCLOAK_JWKS_URL"]
EXPECTED_AZP = os.environ["EXPECTED_AZP"]

OPA_DECISION_URL = os.environ["OPA_DECISION_URL"]

EMPLOYEE_API_URL = os.environ["EMPLOYEE_API_URL"]
FINANCE_API_URL = os.environ["FINANCE_API_URL"]

GATEWAY_EMPLOYEE_TOKEN = os.environ["GATEWAY_EMPLOYEE_TOKEN"]
GATEWAY_FINANCE_TOKEN = os.environ["GATEWAY_FINANCE_TOKEN"]

TELEMETRY_URL = os.environ["TELEMETRY_URL"]
TELEMETRY_INGEST_TOKEN = os.environ["TELEMETRY_INGEST_TOKEN"]

jwks = PyJWKClient(KEYCLOAK_JWKS_URL)


async def emit_event(
    event_type: str,
    outcome: str,
    subject: str | None = None,
    resource: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    payload = {
        "source": "gateway",
        "event_type": event_type,
        "outcome": outcome,
        "subject": subject,
        "resource": resource,
        "details": details or {},
    }

    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            await client.post(
                f"{TELEMETRY_URL}/event",
                json=payload,
                headers={
                    "X-Redoubt-Telemetry-Token": TELEMETRY_INGEST_TOKEN
                },
            )
    except Exception:
        # Security telemetry failure is visible in gateway stdout.
        # It does not silently convert a DENY into an ALLOW.
        print("telemetry_delivery_failed", payload)


def bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing bearer token")

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    return token


def validate_token(token: str) -> dict[str, Any]:
    try:
        signing_key = jwks.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            options={
                "verify_aud": False
            },
            leeway=5,
        )

        # Phase-5 test tokens must originate from the dedicated lab client.
        if claims.get("azp") != EXPECTED_AZP:
            raise HTTPException(
                status_code=401,
                detail="Token was not issued to the expected Project Redoubt client",
            )

        return claims

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=f"Token validation failed: {type(exc).__name__}",
        ) from exc


async def authorize(
    claims: dict[str, Any],
    resource: str,
    action: str,
    device_trusted: bool,
) -> None:
    username = claims.get("preferred_username", "unknown")
    roles = claims.get("realm_access", {}).get("roles", [])

    policy_input = {
        "input": {
            "subject": {
                "username": username,
                "roles": roles,
            },
            "resource": resource,
            "action": action,
            "context": {
                "device_trusted": device_trusted,
            },
        }
    }

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.post(
                OPA_DECISION_URL,
                json=policy_input,
            )
            response.raise_for_status()

        decision = response.json().get("result")

        if not decision:
            raise RuntimeError("OPA returned no decision")

    except Exception as exc:
        await emit_event(
            "policy_decision",
            "error",
            username,
            resource,
            {"error": type(exc).__name__},
        )

        # Fail closed if the Policy Decision Point is unavailable.
        raise HTTPException(
            status_code=503,
            detail="Policy decision unavailable; request denied",
        ) from exc

    allowed = bool(decision.get("allow", False))

    await emit_event(
        "policy_decision",
        "allow" if allowed else "deny",
        username,
        resource,
        {
            "action": action,
            "device_trusted": device_trusted,
            "roles": roles,
            "reason": decision.get("reason"),
        },
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Access denied by Project Redoubt policy",
        )


async def call_backend(
    url: str,
    username: str,
    gateway_token: str,
) -> dict[str, Any]:
    headers = {
        "X-Redoubt-Gateway-Token": gateway_token,
        "X-Redoubt-User": username,
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Protected backend request failed",
        )

    return response.json()


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "component": "policy-enforcement-gateway",
    }


@app.get("/employee/profile")
async def employee_profile(
    authorization: str | None = Header(default=None),
    x_device_trusted: str = Header(default="false"),
) -> dict[str, Any]:
    token = bearer_token(authorization)
    claims = validate_token(token)

    trusted = x_device_trusted.lower() == "true"

    await authorize(
        claims,
        resource="employee-api",
        action="read",
        device_trusted=trusted,
    )

    return await call_backend(
        f"{EMPLOYEE_API_URL}/profile",
        claims.get("preferred_username", "unknown"),
        GATEWAY_EMPLOYEE_TOKEN,
    )


@app.get("/finance/summary")
async def finance_summary(
    authorization: str | None = Header(default=None),
    x_device_trusted: str = Header(default="false"),
) -> dict[str, Any]:
    token = bearer_token(authorization)
    claims = validate_token(token)

    trusted = x_device_trusted.lower() == "true"

    await authorize(
        claims,
        resource="finance-api",
        action="read",
        device_trusted=trusted,
    )

    return await call_backend(
        f"{FINANCE_API_URL}/summary",
        claims.get("preferred_username", "unknown"),
        GATEWAY_FINANCE_TOKEN,
    )
