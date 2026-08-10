import os
from typing import Any

import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="ResTech Employee API",
    version="0.1.0",
)

GATEWAY_EMPLOYEE_TOKEN = os.environ["GATEWAY_EMPLOYEE_TOKEN"]

TELEMETRY_URL = os.environ["TELEMETRY_URL"]
TELEMETRY_INGEST_TOKEN = os.environ["TELEMETRY_INGEST_TOKEN"]


def validate_gateway(token: str | None) -> None:
    if token != GATEWAY_EMPLOYEE_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Direct workload access denied",
        )


async def emit_event(
    outcome: str,
    subject: str,
) -> None:
    payload: dict[str, Any] = {
        "source": "employee-api",
        "event_type": "application_access",
        "outcome": outcome,
        "subject": subject,
        "resource": "employee-api",
        "details": {},
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
        print("telemetry_delivery_failed", payload)


@app.get("/health")
async def health():
    return {"status": "ok", "component": "employee-api"}


@app.get("/profile")
async def profile(
    x_redoubt_gateway_token: str | None = Header(default=None),
    x_redoubt_user: str = Header(default="unknown"),
):
    validate_gateway(x_redoubt_gateway_token)

    await emit_event("allow", x_redoubt_user)

    return {
        "application": "employee-api",
        "user": x_redoubt_user,
        "classification": "INTERNAL",
        "message": "ResTech employee profile access permitted",
    }
