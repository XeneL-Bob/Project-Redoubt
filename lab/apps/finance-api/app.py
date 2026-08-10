import os
from pathlib import Path
from typing import Any

import httpx
import psycopg
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="ResTech Finance API",
    version="0.1.0",
)

GATEWAY_FINANCE_TOKEN = os.environ["GATEWAY_FINANCE_TOKEN"]

VAULT_ADDR = os.environ["VAULT_ADDR"]
VAULT_ROLE_ID_FILE = os.environ["VAULT_ROLE_ID_FILE"]
VAULT_SECRET_ID_FILE = os.environ["VAULT_SECRET_ID_FILE"]

TELEMETRY_URL = os.environ["TELEMETRY_URL"]
TELEMETRY_INGEST_TOKEN = os.environ["TELEMETRY_INGEST_TOKEN"]


def validate_gateway(token: str | None) -> None:
    if token != GATEWAY_FINANCE_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Direct workload access denied",
        )


def read_credential(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()


async def vault_database_secret() -> dict[str, Any]:
    role_id = read_credential(VAULT_ROLE_ID_FILE)
    secret_id = read_credential(VAULT_SECRET_ID_FILE)

    async with httpx.AsyncClient(timeout=3.0) as client:
        login = await client.post(
            f"{VAULT_ADDR}/v1/auth/approle/login",
            json={
                "role_id": role_id,
                "secret_id": secret_id,
            },
        )
        login.raise_for_status()

        vault_token = login.json()["auth"]["client_token"]

        secret = await client.get(
            f"{VAULT_ADDR}/v1/secret/data/finance/db",
            headers={"X-Vault-Token": vault_token},
        )
        secret.raise_for_status()

    return secret.json()["data"]["data"]


async def emit_event(
    event_type: str,
    outcome: str,
    subject: str,
    details: dict[str, Any] | None = None,
    correlation_id: str | None = None,
) -> None:
    payload = {
        "source": "finance-api",
        "event_type": event_type,
        "outcome": outcome,
        "subject": subject,
        "resource": "finance-api",
        "correlation_id": correlation_id,
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
        print("telemetry_delivery_failed", payload)


@app.get("/health")
async def health():
    return {"status": "ok", "component": "finance-api"}


@app.get("/summary")
async def finance_summary(
    x_redoubt_gateway_token: str | None = Header(default=None),
    x_redoubt_user: str = Header(default="unknown"),
    x_redoubt_correlation_id: str | None = Header(default=None),
):
    if x_redoubt_gateway_token != GATEWAY_FINANCE_TOKEN:
        await emit_event(
            "direct_backend_access_denied",
            "deny",
            x_redoubt_user,
            {
                "reason": "invalid_gateway_credential"
            },
            x_redoubt_correlation_id,
        )

        raise HTTPException(
            status_code=403,
            detail="Direct workload access denied",
        )

    try:
        secret = await vault_database_secret()

        await emit_event(
            "vault_secret_access",
            "allow",
            x_redoubt_user,
            {"secret_path": "secret/finance/db"},
            x_redoubt_correlation_id,
        )

        with psycopg.connect(
            host=secret["host"],
            port=int(secret["port"]),
            dbname=secret["database"],
            user=secret["username"],
            password=secret["password"],
            connect_timeout=3,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT current_database(), current_user, CURRENT_TIMESTAMP"
                )
                database, database_user, timestamp = cursor.fetchone()

    except Exception as exc:
        await emit_event(
            "application_access",
            "error",
            x_redoubt_user,
            {"error": type(exc).__name__},
            x_redoubt_correlation_id,
        )

        raise HTTPException(
            status_code=503,
            detail="Finance dependency unavailable",
        ) from exc

    await emit_event(
        "application_access",
        "allow",
        x_redoubt_user,
        {"classification": "RESTRICTED"},
        x_redoubt_correlation_id,
    )

    return {
        "application": "finance-api",
        "user": x_redoubt_user,
        "classification": "RESTRICTED",
        "database": database,
        "database_user": database_user,
        "database_time": timestamp.isoformat(),
        "demo_financial_position": 125000,
    }
