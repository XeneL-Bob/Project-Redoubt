#!/usr/bin/env python3

import json
import os
import time
import uuid

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALERTS_FILE = Path(
    os.environ.get(
        "ALERTS_FILE",
        "/data/security-alerts.jsonl",
    )
)

INCIDENTS_FILE = Path(
    os.environ.get(
        "INCIDENTS_FILE",
        "/data/incidents.jsonl",
    )
)

ACTIONS_FILE = Path(
    os.environ.get(
        "ACTIONS_FILE",
        "/data/containment-actions.jsonl",
    )
)

STATE_FILE = Path(
    os.environ.get(
        "STATE_FILE",
        "/data/incident-state.json",
    )
)


def utcnow() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def read_jsonl(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records = []

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        if not line.strip():
            continue

        try:
            records.append(
                json.loads(line)
            )
        except json.JSONDecodeError:
            continue

    return records


def append_jsonl(
    path: Path,
    record: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json.dumps(
                record,
                sort_keys=True,
            )
            + "\n"
        )


def load_state() -> dict[str, Any] | None:
    if not STATE_FILE.exists():
        return None

    try:
        return json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return None


def save_state(
    processed_lines: int,
    handled_alert_ids: set[str],
) -> None:
    STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    STATE_FILE.write_text(
        json.dumps(
            {
                "processed_lines":
                    processed_lines,
                "handled_alert_ids":
                    sorted(
                        handled_alert_ids
                    ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def severity_class(
    severity: str,
) -> str:
    return {
        "critical": "SEV-1",
        "high": "SEV-2",
        "medium": "SEV-3",
        "low": "SEV-4",
    }.get(
        severity.lower(),
        "SEV-4",
    )


def containment_action(
    alert: dict[str, Any],
    incident_id: str,
) -> dict[str, Any]:
    severity = str(
        alert.get(
            "severity",
            "low",
        )
    ).lower()

    if severity == "critical":
        action_type = (
            "isolate_resource_path"
        )
        target = alert.get(
            "resource",
            "unknown",
        )

    else:
        action_type = "suspend_subject"
        target = alert.get(
            "subject",
            "unknown",
        )

    return {
        "action_id":
            str(uuid.uuid4()),
        "incident_id":
            incident_id,
        "timestamp":
            utcnow(),
        "action_type":
            action_type,
        "target":
            target,
        "mode":
            "simulated",
        "status":
            "RECORDED",
        "source_detection":
            alert.get("detection_id"),
        "source_alert_id":
            alert.get("alert_id"),
    }


def create_incident(
    alert: dict[str, Any],
) -> None:
    severity = str(
        alert.get(
            "severity",
            "low",
        )
    ).lower()

    if severity not in {
        "high",
        "critical",
    }:
        return

    incident_id = str(
        uuid.uuid4()
    )

    incident = {
        "incident_id":
            incident_id,
        "created_at":
            utcnow(),
        "status":
            "OPEN",
        "severity":
            severity_class(
                severity
            ),
        "source_alert_id":
            alert.get("alert_id"),
        "detection_id":
            alert.get("detection_id"),
        "subject":
            alert.get("subject"),
        "resource":
            alert.get("resource"),
        "correlation_id":
            alert.get(
                "correlation_id"
            ),
        "risk_ids":
            alert.get(
                "risk_ids",
                [],
            ),
        "attack_techniques":
            alert.get(
                "attack_techniques",
                [],
            ),
        "triage": {
            "classification":
                "SECURITY_INCIDENT",
            "priority":
                (
                    "IMMEDIATE"
                    if severity
                    == "critical"
                    else "HIGH"
                ),
        },
    }

    action = containment_action(
        alert,
        incident_id,
    )

    append_jsonl(
        INCIDENTS_FILE,
        incident,
    )

    append_jsonl(
        ACTIONS_FILE,
        action,
    )

    print(
        json.dumps(
            {
                "component":
                    "incident-response",
                "status":
                    "incident-created",
                "incident_id":
                    incident_id,
                "severity":
                    incident["severity"],
                "detection_id":
                    alert.get(
                        "detection_id"
                    ),
                "subject":
                    alert.get("subject"),
            },
            sort_keys=True,
        ),
        flush=True,
    )


def main() -> None:
    alerts = read_jsonl(
        ALERTS_FILE
    )

    state = load_state()

    if state is None:
        processed = len(alerts)
        handled = set()

        save_state(
            processed,
            handled,
        )

        print(
            json.dumps(
                {
                    "component":
                        "incident-response",
                    "status":
                        "baseline-established",
                    "historical_alerts_skipped":
                        processed,
                },
                sort_keys=True,
            ),
            flush=True,
        )

    else:
        processed = min(
            int(
                state.get(
                    "processed_lines",
                    0,
                )
            ),
            len(alerts),
        )

        handled = set(
            state.get(
                "handled_alert_ids",
                [],
            )
        )

    print(
        json.dumps(
            {
                "component":
                    "incident-response",
                "status":
                    "started",
                "processed_lines":
                    processed,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    while True:
        alerts = read_jsonl(
            ALERTS_FILE
        )

        if processed > len(alerts):
            processed = len(alerts)

        for alert in alerts[
            processed:
        ]:
            alert_id = str(
                alert.get(
                    "alert_id",
                    "",
                )
            )

            if (
                alert_id
                and alert_id
                not in handled
            ):
                create_incident(
                    alert
                )

                handled.add(
                    alert_id
                )

            processed += 1

        save_state(
            processed,
            handled,
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
