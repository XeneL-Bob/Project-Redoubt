import argparse
import hashlib
import json
import os
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def get_path(data: dict[str, Any], path: str) -> Any:
    value: Any = data

    for part in path.split("."):
        if not isinstance(value, dict):
            return None

        value = value.get(part)

    return value


def matches(
    event: dict[str, Any],
    conditions: dict[str, Any],
) -> bool:
    for field, expected in conditions.items():
        actual = get_path(event, field)

        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False

    return True


class DetectionEngine:
    def __init__(self, rules: list[dict[str, Any]]):
        self.rules = rules

        self.threshold_state: dict[
            tuple[str, str],
            deque[datetime],
        ] = defaultdict(deque)

        self.history: deque[dict[str, Any]] = deque(
            maxlen=5000
        )

        self.emitted_keys: set[str] = set()

    def _alert_key(
        self,
        rule: dict[str, Any],
        event: dict[str, Any],
    ) -> str:
        raw = json.dumps(
            {
                "rule": rule["id"],
                "event": event,
            },
            sort_keys=True,
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(raw).hexdigest()

    def _create_alert(
        self,
        rule: dict[str, Any],
        event: dict[str, Any],
    ) -> dict[str, Any] | None:
        key = self._alert_key(rule, event)

        if key in self.emitted_keys:
            return None

        self.emitted_keys.add(key)

        return {
            "alert_id": str(uuid.uuid4()),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "detection_id": rule["id"],
            "title": rule["title"],
            "severity": rule["severity"],
            "description": rule["description"],
            "subject": event.get("subject"),
            "resource": event.get("resource"),
            "correlation_id": event.get(
                "correlation_id"
            ),
            "source": event.get("source"),
            "source_event_type": event.get(
                "event_type"
            ),
            "attack_techniques": rule.get(
                "attack_techniques",
                [],
            ),
            "risk_ids": rule.get(
                "risk_ids",
                [],
            ),
            "event_timestamp": event.get(
                "timestamp"
            ),
        }

    def _threshold(
        self,
        rule: dict[str, Any],
        event: dict[str, Any],
    ) -> bool:
        if not matches(event, rule["match"]):
            return False

        group_value = str(
            get_path(
                event,
                rule["group_by"],
            )
            or "unknown"
        )

        timestamp = parse_timestamp(
            event["timestamp"]
        )

        key = (
            rule["id"],
            group_value,
        )

        window = self.threshold_state[key]
        window.append(timestamp)

        cutoff = (
            timestamp.timestamp()
            - int(rule["window_seconds"])
        )

        while (
            window
            and window[0].timestamp() < cutoff
        ):
            window.popleft()

        return len(window) == int(
            rule["threshold"]
        )

    def _missing_prior(
        self,
        rule: dict[str, Any],
        event: dict[str, Any],
    ) -> bool:
        if not matches(event, rule["match"]):
            return False

        field = rule["correlation_field"]
        value = get_path(event, field)

        if not value:
            return True

        event_time = parse_timestamp(
            event["timestamp"]
        )

        max_age = int(
            rule["within_seconds"]
        )

        for prior in reversed(self.history):
            prior_time = parse_timestamp(
                prior["timestamp"]
            )

            age = (
                event_time - prior_time
            ).total_seconds()

            if age < 0:
                continue

            if age > max_age:
                break

            if (
                get_path(prior, field) == value
                and matches(
                    prior,
                    rule["prior_match"],
                )
            ):
                return False

        return True

    def process_event(
        self,
        event: dict[str, Any],
        emit: bool = True,
    ) -> list[dict[str, Any]]:
        alerts = []

        for rule in self.rules:
            kind = rule["kind"]

            if kind == "match":
                triggered = matches(
                    event,
                    rule["match"],
                )

            elif kind == "threshold":
                triggered = self._threshold(
                    rule,
                    event,
                )

            elif kind == "missing_prior":
                triggered = self._missing_prior(
                    rule,
                    event,
                )

            else:
                raise ValueError(
                    f"Unsupported rule kind: {kind}"
                )

            if triggered and emit:
                alert = self._create_alert(
                    rule,
                    event,
                )

                if alert:
                    alerts.append(alert)

        self.history.append(event)

        return alerts


def load_rules(
    path: Path,
) -> list[dict[str, Any]]:
    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    return data["rules"]


def read_events(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    events = []

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        if not line.strip():
            continue

        try:
            events.append(
                json.loads(line)
            )
        except json.JSONDecodeError:
            continue

    return events


def append_alert(
    path: Path,
    alert: dict[str, Any],
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
                alert,
                sort_keys=True,
            )
            + "\n"
        )

    print(
        json.dumps(
            alert,
            sort_keys=True,
        ),
        flush=True,
    )


def load_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        return None


def save_state(
    path: Path,
    processed_lines: int,
    emitted_keys: set[str],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            {
                "processed_lines": processed_lines,
                "emitted_keys": sorted(
                    emitted_keys
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def run_daemon(
    rules_path: Path,
    events_path: Path,
    alerts_path: Path,
    state_path: Path,
) -> None:
    rules = load_rules(rules_path)
    engine = DetectionEngine(rules)

    existing = read_events(events_path)
    state = load_state(state_path)

    if state is None:
        # First Phase 6 startup:
        #
        # Existing telemetry predates the detection engine and
        # may not contain correlation IDs. Establish the current
        # end of the event stream as the baseline instead of
        # retrospectively generating false-positive alerts.
        processed = len(existing)

        save_state(
            state_path,
            processed,
            engine.emitted_keys,
        )

        print(
            json.dumps(
                {
                    "component": "detection-engine",
                    "status": "baseline-established",
                    "rules": len(rules),
                    "historical_events_skipped": processed,
                },
                sort_keys=True,
            ),
            flush=True,
        )

    else:
        processed = int(
            state.get(
                "processed_lines",
                0,
            )
        )

        engine.emitted_keys.update(
            state.get(
                "emitted_keys",
                [],
            )
        )

        if processed > len(existing):
            processed = 0
            engine.emitted_keys.clear()

        # Reconstruct correlation/threshold history without
        # generating duplicate alerts.
        for event in existing[:processed]:
            engine.process_event(
                event,
                emit=False,
            )

    print(
        json.dumps(
            {
                "component": "detection-engine",
                "status": "started",
                "rules": len(rules),
                "processed_lines": processed,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    while True:
        events = read_events(events_path)

        if processed > len(events):
            processed = 0
            engine = DetectionEngine(rules)

        for event in events[processed:]:
            alerts = engine.process_event(
                event
            )

            for alert in alerts:
                append_alert(
                    alerts_path,
                    alert,
                )

            processed += 1

        save_state(
            state_path,
            processed,
            engine.emitted_keys,
        )

        time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mode",
        choices=["daemon"],
    )

    parser.add_argument(
        "--rules",
        default=os.environ.get(
            "RULES_FILE",
            "/app/rules.json",
        ),
    )

    parser.add_argument(
        "--events",
        default=os.environ.get(
            "EVENTS_FILE",
            "/data/security-events.jsonl",
        ),
    )

    parser.add_argument(
        "--alerts",
        default=os.environ.get(
            "ALERTS_FILE",
            "/data/security-alerts.jsonl",
        ),
    )

    parser.add_argument(
        "--state",
        default=os.environ.get(
            "STATE_FILE",
            "/data/detection-state.json",
        ),
    )

    args = parser.parse_args()

    run_daemon(
        Path(args.rules),
        Path(args.events),
        Path(args.alerts),
        Path(args.state),
    )


if __name__ == "__main__":
    main()
