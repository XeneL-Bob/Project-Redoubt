#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assurance" / "source-registry.json"


def fail(message):
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def expected_ids(prefix, first_id, last_id):
    return {
        f"{prefix}-{number:03d}"
        for number in range(first_id, last_id + 1)
    }


def extract_document_ids(path, prefix):
    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        rf"\b{re.escape(prefix)}-(\d{{3}})\b"
    )

    return {
        f"{prefix}-{match}"
        for match in pattern.findall(text)
    }


def extract_adr_ids(directory):
    ids = set()

    pattern = re.compile(
        r"^(\d{3})-.*\.md$"
    )

    for path in directory.iterdir():
        if not path.is_file():
            continue

        match = pattern.match(path.name)

        if not match:
            continue

        number = int(match.group(1))

        if number == 0:
            continue

        ids.add(
            f"ADR-{number:03d}"
        )

    return ids


def main():
    if not REGISTRY.exists():
        fail("source registry missing")

    registry = json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )

    sources = registry.get("sources")

    if not isinstance(sources, list):
        fail("sources must be a list")

    total = 0

    print("=== Project Redoubt assurance baseline ===")

    for source in sources:
        entity = source["entity"]
        prefix = source["prefix"]
        relative = Path(source["path"])

        path = ROOT / relative

        if not path.exists():
            fail(
                f"{entity}: source does not exist: "
                f"{relative}"
            )

        expected = expected_ids(
            prefix,
            source["first_id"],
            source["last_id"],
        )

        if path.is_dir():
            if prefix != "ADR":
                fail(
                    f"{entity}: unsupported directory source"
                )

            actual = extract_adr_ids(path)

        else:
            actual = extract_document_ids(
                path,
                prefix,
            )

        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)

        if missing:
            fail(
                f"{entity}: missing identifiers: "
                f"{', '.join(missing)}"
            )

        if unexpected:
            fail(
                f"{entity}: unexpected identifiers: "
                f"{', '.join(unexpected)}"
            )

        if len(actual) != source["expected_count"]:
            fail(
                f"{entity}: expected "
                f"{source['expected_count']} unique IDs, "
                f"found {len(actual)}"
            )

        total += len(actual)

        print(
            f"[PASS] {entity}: "
            f"{len(actual)} identifiers"
        )

    print()
    print(
        f"[PASS] Assurance baseline contains "
        f"{total} authoritative identifiers"
    )

    print(
        "PHASE 13A ASSURANCE BASELINE: PASS"
    )


if __name__ == "__main__":
    main()
