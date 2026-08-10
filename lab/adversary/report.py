#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

RESULTS = (
    ROOT
    / "evidence"
    / "runtime"
    / "adversary-results.jsonl"
)


def main():
    if not RESULTS.exists():
        raise SystemExit(
            "No adversary-results.jsonl found. "
            "Run the Phase 7 adversary test first."
        )

    rows = [
        json.loads(line)
        for line in RESULTS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    print(
        "============================================================"
    )
    print(
        " PROJECT REDOUBT — ADVERSARY VALIDATION SUMMARY"
    )
    print(
        "============================================================"
    )

    for row in rows:
        print(
            "{:<8} {:<8} {:<30} {}".format(
                row["scenario_id"],
                row["validation"],
                row["verdict"],
                row["title"],
            )
        )

    totals = Counter()

    for row in rows:
        if row.get("prevented"):
            totals["PREVENTED"] += 1

        if row.get("detected"):
            totals["DETECTED"] += 1

        if row.get("contained"):
            totals["CONTAINED"] += 1

        if row.get("verdict") == "MISSED":
            totals["MISSED"] += 1

    failed = [
        row
        for row in rows
        if row.get("validation") != "PASS"
    ]

    print()
    print(f"Scenarios:            {len(rows)}")
    print(f"Prevented:            {totals['PREVENTED']}")
    print(f"Detected:             {totals['DETECTED']}")
    print(f"Contained:            {totals['CONTAINED']}")
    print(f"Missed:               {totals['MISSED']}")
    print(f"Validation failures:  {len(failed)}")

    if failed:
        print()
        print("Failed scenarios:")

        for row in failed:
            print(
                f"- {row['scenario_id']}: "
                f"{row['title']}"
            )

        raise SystemExit(1)

    print()
    print(
        "PHASE 7 ADVERSARY REPORT: PASS"
    )


if __name__ == "__main__":
    main()
