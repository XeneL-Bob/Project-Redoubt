import json
import os
import time
from pathlib import Path

import httpx


TELEMETRY_URL = os.environ[
    "TELEMETRY_URL"
].rstrip("/")

TELEMETRY_INGEST_TOKEN = os.environ[
    "TELEMETRY_INGEST_TOKEN"
]

SPOOL_FILE = Path(
    os.environ.get(
        "SPOOL_FILE",
        "/spool/security-events.jsonl",
    )
)

STATE_FILE = Path(
    os.environ.get(
        "STATE_FILE",
        "/spool/relay-state.json",
    )
)


def load_state() -> int:
    if not STATE_FILE.exists():
        return 0

    try:
        data = json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )

        return int(
            data.get(
                "processed_lines",
                0,
            )
        )
    except Exception:
        return 0


def save_state(
    processed_lines: int,
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
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def read_lines() -> list[str]:
    if not SPOOL_FILE.exists():
        return []

    return SPOOL_FILE.read_text(
        encoding="utf-8"
    ).splitlines()


processed = load_state()

print(
    json.dumps(
        {
            "component":
                "supply-chain-telemetry-relay",
            "status":
                "started",
            "processed_lines":
                processed,
        },
        sort_keys=True,
    ),
    flush=True,
)

with httpx.Client(
    timeout=5.0,
) as client:

    while True:
        lines = read_lines()

        if processed > len(lines):
            processed = 0
            save_state(processed)

        while processed < len(lines):
            line = lines[processed]

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                processed += 1
                save_state(processed)
                continue

            try:
                response = client.post(
                    f"{TELEMETRY_URL}/event",
                    headers={
                        "X-Redoubt-Telemetry-Token":
                            TELEMETRY_INGEST_TOKEN,
                    },
                    json=event,
                )

                response.raise_for_status()

            except Exception as exc:
                print(
                    json.dumps(
                        {
                            "component":
                                "supply-chain-telemetry-relay",
                            "status":
                                "forward-failed",
                            "error":
                                str(exc),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

                break

            processed += 1
            save_state(processed)

            print(
                json.dumps(
                    {
                        "component":
                            "supply-chain-telemetry-relay",
                        "status":
                            "forwarded",
                        "processed_lines":
                            processed,
                        "correlation_id":
                            event.get(
                                "correlation_id"
                            ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

        time.sleep(0.5)
