import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Project Redoubt Security Telemetry Collector",
    version="0.1.0",
)

INGEST_TOKEN = os.environ["TELEMETRY_INGEST_TOKEN"]

LOG_PATH = Path("/data/security-events.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

lock = Lock()


class SecurityEvent(BaseModel):
    source: str
    event_type: str
    outcome: str
    subject: str | None = None
    resource: str | None = None
    correlation_id: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "component": "telemetry-collector",
    }


@app.post("/event", status_code=202)
def event(
    event: SecurityEvent,
    x_redoubt_telemetry_token: str | None = Header(default=None),
):
    if x_redoubt_telemetry_token != INGEST_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Telemetry ingestion denied",
        )

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event.model_dump(),
    }

    with lock:
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    print(json.dumps(record, sort_keys=True))

    return {"accepted": True}
