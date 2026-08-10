import os
from typing import Any

import httpx
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
)


app = FastAPI(
    title="Project Redoubt Management API",
    version="0.1.0",
)

MANAGEMENT_GATEWAY_TOKEN = os.environ[
    "MANAGEMENT_GATEWAY_TOKEN"
]

TELEMETRY_URL = os.environ[
    "TELEMETRY_URL"
]

TELEMETRY_INGEST_TOKEN = os.environ[
    "TELEMETRY_INGEST_TOKEN"
]


async def emit_event(
    event_type: str,
    outcome: str,
    subject: str,
    resource: str,
    details: dict[str, Any] | None = None,
    correlation_id: str | None = None,
) -> None:
    payload = {
        "source": "management-api",
        "event_type": event_type,
        "outcome": outcome,
        "subject": subject,
        "resource": resource,
        "correlation_id": correlation_id,
        "details": details or {},
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


async def validate_management_gateway(
    token: str | None,
    subject: str,
    resource: str,
    correlation_id: str | None,
) -> None:
    if token != MANAGEMENT_GATEWAY_TOKEN:
        await emit_event(
            "direct_management_access_denied",
            "deny",
            subject,
            resource,
            {
                "reason":
                    "invalid_management_gateway_credential"
            },
            correlation_id,
        )

        raise HTTPException(
            status_code=403,
            detail="Direct management-plane access denied",
        )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "component": "management-api",
    }


@app.get("/infrastructure/status")
async def infrastructure_status(
    x_redoubt_management_token:
        str | None = Header(default=None),
    x_redoubt_admin:
        str = Header(default="unknown"),
    x_redoubt_correlation_id:
        str | None = Header(default=None),
):
    await validate_management_gateway(
        x_redoubt_management_token,
        x_redoubt_admin,
        "infrastructure-management",
        x_redoubt_correlation_id,
    )

    await emit_event(
        "privileged_operation",
        "allow",
        x_redoubt_admin,
        "infrastructure-management",
        {
            "action": "read",
        },
        x_redoubt_correlation_id,
    )

    return {
        "management_domain":
            "infrastructure",
        "status":
            "operational",
        "administrator":
            x_redoubt_admin,
    }


@app.post("/infrastructure/restart-service")
async def restart_service(
    x_redoubt_management_token:
        str | None = Header(default=None),
    x_redoubt_admin:
        str = Header(default="unknown"),
    x_redoubt_correlation_id:
        str | None = Header(default=None),
):
    await validate_management_gateway(
        x_redoubt_management_token,
        x_redoubt_admin,
        "infrastructure-management",
        x_redoubt_correlation_id,
    )

    await emit_event(
        "privileged_operation",
        "allow",
        x_redoubt_admin,
        "infrastructure-management",
        {
            "action":
                "restart-service",
            "mode":
                "simulated",
        },
        x_redoubt_correlation_id,
    )

    return {
        "status": "accepted",
        "action": "restart-service",
        "mode": "simulated",
        "administrator":
            x_redoubt_admin,
    }


@app.get("/security/status")
async def security_status(
    x_redoubt_management_token:
        str | None = Header(default=None),
    x_redoubt_admin:
        str = Header(default="unknown"),
    x_redoubt_correlation_id:
        str | None = Header(default=None),
):
    await validate_management_gateway(
        x_redoubt_management_token,
        x_redoubt_admin,
        "security-management",
        x_redoubt_correlation_id,
    )

    await emit_event(
        "privileged_operation",
        "allow",
        x_redoubt_admin,
        "security-management",
        {
            "action": "read",
        },
        x_redoubt_correlation_id,
    )

    return {
        "management_domain":
            "security",
        "status":
            "operational",
        "administrator":
            x_redoubt_admin,
    }


@app.post("/security/update-detection")
async def update_detection(
    x_redoubt_management_token:
        str | None = Header(default=None),
    x_redoubt_admin:
        str = Header(default="unknown"),
    x_redoubt_correlation_id:
        str | None = Header(default=None),
):
    await validate_management_gateway(
        x_redoubt_management_token,
        x_redoubt_admin,
        "security-management",
        x_redoubt_correlation_id,
    )

    await emit_event(
        "privileged_operation",
        "allow",
        x_redoubt_admin,
        "security-management",
        {
            "action":
                "update-detection",
            "mode":
                "simulated",
        },
        x_redoubt_correlation_id,
    )

    return {
        "status":
            "accepted",
        "action":
            "update-detection",
        "mode":
            "simulated",
        "administrator":
            x_redoubt_admin,
    }
