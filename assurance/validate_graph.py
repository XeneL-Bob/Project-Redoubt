#!/usr/bin/env python3

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORE_REGISTRY = (
    ROOT
    / "assurance"
    / "source-registry.json"
)

VALIDATION_REGISTRY = (
    ROOT
    / "assurance"
    / "validation-source-registry.json"
)

GRAPH_PATH = (
    ROOT
    / "assurance"
    / "traceability-graph.json"
)


def fail(message):
    print(
        f"[FAIL] {message}"
    )
    raise SystemExit(1)


def identifier_range(
    prefix,
    first_id,
    last_id,
):
    return {
        f"{prefix}-{number:03d}"
        for number in range(
            first_id,
            last_id + 1,
        )
    }


def extract_ids(
    path,
    prefix,
):
    if path.is_dir():

        if prefix != "ADR":
            fail(
                f"Unsupported directory source: "
                f"{path}"
            )

        pattern = re.compile(
            r"^(\d{3})-.*\.md$"
        )

        found = set()

        for candidate in path.iterdir():

            if not candidate.is_file():
                continue

            match = pattern.match(
                candidate.name
            )

            if not match:
                continue

            number = int(
                match.group(1)
            )

            if number == 0:
                continue

            found.add(
                f"ADR-{number:03d}"
            )

        return found

    text = path.read_text(
        encoding="utf-8"
    )

    pattern = re.compile(
        rf"\b{re.escape(prefix)}-"
        rf"(\d{{3}})\b"
    )

    return {
        f"{prefix}-{number}"
        for number in pattern.findall(
            text
        )
    }


def load_registry(
    registry_path,
):
    registry = json.loads(
        registry_path.read_text(
            encoding="utf-8"
        )
    )

    known = set()

    for source in registry["sources"]:

        path = (
            ROOT
            / source["path"]
        )

        if not path.exists():
            fail(
                f"Missing source: {path}"
            )

        expected = identifier_range(
            source["prefix"],
            source["first_id"],
            source["last_id"],
        )

        actual = extract_ids(
            path,
            source["prefix"],
        )

        if actual != expected:

            missing = sorted(
                expected - actual
            )

            unexpected = sorted(
                actual - expected
            )

            if missing:
                print(
                    "[ERROR] Missing: "
                    + ", ".join(missing)
                )

            if unexpected:
                print(
                    "[ERROR] Unexpected: "
                    + ", ".join(unexpected)
                )

            fail(
                f"{source['entity']} "
                f"identifier baseline invalid"
            )

        if len(actual) != source[
            "expected_count"
        ]:
            fail(
                f"{source['entity']} "
                f"count mismatch"
            )

        known.update(actual)

    return known


def require_known(
    identifiers,
    known,
    context,
):
    for identifier in identifiers:

        if identifier not in known:
            fail(
                f"{context}: unknown identifier "
                f"{identifier}"
            )


def exact_id_set(
    records,
    expected,
    context,
):
    actual = {
        record["id"]
        for record in records
    }

    if actual != expected:

        missing = sorted(
            expected - actual
        )

        unexpected = sorted(
            actual - expected
        )

        if missing:
            print(
                "[ERROR] Missing: "
                + ", ".join(missing)
            )

        if unexpected:
            print(
                "[ERROR] Unexpected: "
                + ", ".join(unexpected)
            )

        fail(
            f"{context}: identifier set mismatch"
        )


def main():

    if not GRAPH_PATH.exists():
        fail(
            "Traceability graph missing"
        )

    core_ids = load_registry(
        CORE_REGISTRY
    )

    validation_ids = load_registry(
        VALIDATION_REGISTRY
    )

    known = (
        core_ids
        | validation_ids
    )

    graph = json.loads(
        GRAPH_PATH.read_text(
            encoding="utf-8"
        )
    )

    if graph.get("schema") != (
        "project-redoubt."
        "assurance-graph/v1"
    ):
        fail(
            "Unsupported graph schema"
        )

    objectives = graph[
        "objective_mappings"
    ]

    exact_id_set(
        objectives,
        identifier_range(
            "SO",
            1,
            12
        ),
        "Security objectives",
    )

    for record in objectives:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        require_known(
            record[
                "security_requirements"
            ],
            known,
            record["id"],
        )

        require_known(
            record[
                "business_requirements"
            ],
            known,
            record["id"],
        )

        require_known(
            record[
                "crown_jewels"
            ],
            known,
            record["id"],
        )

    attack_paths = graph[
        "attack_paths"
    ]

    exact_id_set(
        attack_paths,
        identifier_range(
            "AP",
            1,
            8
        ),
        "Attack paths",
    )

    valid_statuses = {
        "PARTIALLY_VALIDATED",
        "SUBSTANTIALLY_VALIDATED",
        "DEFERRED",
        "VALIDATED",
        "NOT_VALIDATED",
    }

    for record in attack_paths:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        require_known(
            record["risks"],
            known,
            record["id"],
        )

        if not record["risks"]:
            fail(
                f"{record['id']} has no risks"
            )

        if record["status"] not in (
            valid_statuses
        ):
            fail(
                f"{record['id']} has invalid "
                f"status {record['status']}"
            )

    adrs = graph["adrs"]

    exact_id_set(
        adrs,
        identifier_range(
            "ADR",
            1,
            12
        ),
        "Architecture decisions",
    )

    for record in adrs:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        require_known(
            record["objectives"],
            known,
            record["id"],
        )

        if not record["objectives"]:
            fail(
                f"{record['id']} has no "
                f"objective mapping"
            )

    controls = graph[
        "architecture_controls"
    ]

    control_ids = set()

    for record in controls:

        control_id = record["id"]

        if control_id in control_ids:
            fail(
                f"Duplicate control "
                f"{control_id}"
            )

        control_ids.add(control_id)

        require_known(
            record["risks"],
            known,
            control_id,
        )

        require_known(
            record["attack_paths"],
            known,
            control_id,
        )

    scenarios = graph[
        "adversary_scenarios"
    ]

    exact_id_set(
        scenarios,
        identifier_range(
            "ADV",
            1,
            16
        ),
        "Adversary scenarios",
    )

    for record in scenarios:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        require_known(
            record["attack_paths"],
            known,
            record["id"],
        )

        require_known(
            record["risks"],
            known,
            record["id"],
        )

        require_known(
            record["detections"],
            known,
            record["id"],
        )

        if not record["attack_paths"]:
            fail(
                f"{record['id']} has no "
                f"attack-path mapping"
            )

    detections = graph[
        "detections"
    ]

    exact_id_set(
        detections,
        identifier_range(
            "DET",
            1,
            20
        ),
        "Detections",
    )

    for record in detections:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        require_known(
            record["risks"],
            known,
            record["id"],
        )

        if not record["risks"]:
            fail(
                f"{record['id']} has no "
                f"risk mapping"
            )

    iac_controls = graph[
        "iac_controls"
    ]

    exact_id_set(
        iac_controls,
        identifier_range(
            "IAC",
            1,
            11
        ),
        "IaC controls",
    )

    for record in iac_controls:

        require_known(
            [record["id"]],
            known,
            record["id"],
        )

        if record["result"] != "PASS":
            fail(
                f"{record['id']} result "
                f"is not PASS"
            )

    require_known(
        graph[
            "iac_objective_scope"
        ],
        known,
        "IaC objective scope",
    )

    graph_records = sum(
        [
            len(objectives),
            len(attack_paths),
            len(adrs),
            len(controls),
            len(scenarios),
            len(detections),
            len(iac_controls),
        ]
    )

    print(
        "=== Project Redoubt assurance graph ==="
    )

    print(
        f"[PASS] Core identifiers: "
        f"{len(core_ids)}"
    )

    print(
        f"[PASS] Validation identifiers: "
        f"{len(validation_ids)}"
    )

    print(
        f"[PASS] Security objectives: "
        f"{len(objectives)}"
    )

    print(
        f"[PASS] Attack paths: "
        f"{len(attack_paths)}"
    )

    print(
        f"[PASS] Architecture decisions: "
        f"{len(adrs)}"
    )

    print(
        f"[PASS] Architecture controls: "
        f"{len(controls)}"
    )

    print(
        f"[PASS] Adversary scenarios: "
        f"{len(scenarios)}"
    )

    print(
        f"[PASS] Detections: "
        f"{len(detections)}"
    )

    print(
        f"[PASS] IaC controls: "
        f"{len(iac_controls)}"
    )

    print()

    print(
        f"[PASS] Validated "
        f"{graph_records} assurance records "
        f"against {len(known)} known identifiers"
    )

    print(
        "PHASE 13B TRACEABILITY GRAPH: PASS"
    )


if __name__ == "__main__":
    main()
