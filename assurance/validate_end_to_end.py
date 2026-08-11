#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH = ROOT / "assurance" / "traceability-graph.json"
EVIDENCE = ROOT / "assurance" / "evidence-catalog.json"

REPORT_JSON = (
    ROOT
    / "assurance"
    / "final-assessment.json"
)

REPORT_MD = (
    ROOT
    / "docs"
    / "assurance"
    / "final-assurance-assessment.md"
)


def fail(message):
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ids(prefix, start, end):
    return {
        f"{prefix}-{number:03d}"
        for number in range(start, end + 1)
    }


def union(records, field):
    result = set()

    for record in records:
        result.update(
            record.get(field, [])
        )

    return result


def main():
    graph = json.loads(
        GRAPH.read_text(encoding="utf-8")
    )

    evidence = json.loads(
        EVIDENCE.read_text(encoding="utf-8")
    )

    brs = ids("BR", 1, 10)
    srs = ids("SR", 1, 25)
    cjs = ids("CJ", 1, 10)
    risks = ids("R", 1, 12)
    aps = ids("AP", 1, 8)
    sos = ids("SO", 1, 12)
    adrs = ids("ADR", 1, 12)

    controls = {
        f"CTRL-{n:03d}"
        for n in range(1, 15)
    }

    br_records = graph.get(
        "business_requirement_mappings",
        []
    )

    if {
        record["id"]
        for record in br_records
    } != brs:
        fail("BR -> SR mapping is incomplete")

    for record in br_records:
        mapped = set(
            record["security_requirements"]
        )

        if not mapped:
            fail(
                f"{record['id']} has no SR mapping"
            )

        if not mapped <= srs:
            fail(
                f"{record['id']} references unknown SR"
            )

    risk_cj = graph.get(
        "risk_crown_jewel_mappings",
        []
    )

    if {
        record["id"]
        for record in risk_cj
    } != risks:
        fail("Risk -> CJ mapping is incomplete")

    for record in risk_cj:
        mapped = set(
            record["crown_jewels"]
        )

        if not mapped:
            fail(
                f"{record['id']} has no crown jewel"
            )

        if not mapped <= cjs:
            fail(
                f"{record['id']} references unknown CJ"
            )

    objective_sr = union(
        graph["objective_mappings"],
        "security_requirements",
    )

    if objective_sr != srs:
        fail(
            "Not every SR maps to a security objective"
        )

    adr_objectives = union(
        graph["adrs"],
        "objectives",
    )

    if adr_objectives != sos:
        fail(
            "Not every security objective maps to an ADR"
        )

    control_records = graph[
        "architecture_controls"
    ]

    control_ids = {
        record["id"]
        for record in control_records
    }

    if control_ids != controls:
        fail(
            "Architecture control set incomplete"
        )

    controls_without_adr = set()

    for record in control_records:
        refs = set(
            record.get("adrs", [])
        )

        if not refs:
            controls_without_adr.add(
                record["id"]
            )

        if not refs <= adrs:
            fail(
                f"{record['id']} references unknown ADR"
            )

    expected_without_adr = {
        "CTRL-013"
    }

    if controls_without_adr != expected_without_adr:
        fail(
            "Unexpected ADR/control traceability gap: "
            + ", ".join(
                sorted(controls_without_adr)
            )
        )

    packages = evidence[
        "evidence_packages"
    ]

    evidence_risks = union(
        packages,
        "risks",
    )

    evidence_aps = union(
        packages,
        "attack_paths",
    )

    evidence_controls = union(
        packages,
        "controls",
    )

    detection_risks = union(
        graph["detections"],
        "risks",
    )

    risks_without_evidence = (
        risks - evidence_risks
    )

    aps_without_evidence = (
        aps - evidence_aps
    )

    controls_without_evidence = (
        controls - evidence_controls
    )

    risks_without_detection = (
        risks - detection_risks
    )

    expected_risk_gap = {
        "R-012"
    }

    expected_ap_gap = {
        "AP-006"
    }

    expected_control_gaps = {
        "CTRL-001",
        "CTRL-011",
        "CTRL-013",
    }

    expected_detection_gaps = {
        "R-009",
        "R-010",
        "R-012",
    }

    if risks_without_evidence != expected_risk_gap:
        fail(
            "Unexpected risk evidence gaps"
        )

    if aps_without_evidence != expected_ap_gap:
        fail(
            "Unexpected attack-path evidence gaps"
        )

    if controls_without_evidence != expected_control_gaps:
        fail(
            "Unexpected control evidence gaps"
        )

    if risks_without_detection != expected_detection_gaps:
        fail(
            "Unexpected detection coverage gaps"
        )

    status_counts = Counter(
        record["status"]
        for record in graph["attack_paths"]
    )

    expected_statuses = {
        "PARTIALLY_VALIDATED": 5,
        "SUBSTANTIALLY_VALIDATED": 2,
        "DEFERRED": 1,
    }

    if dict(status_counts) != expected_statuses:
        fail(
            "Attack-path assurance statuses changed "
            "unexpectedly"
        )

    assessment = {
        "schema": (
            "project-redoubt."
            "final-assurance-assessment/v1"
        ),

        "traceability": {
            "business_requirements_mapped": "10/10",
            "security_requirements_mapped": "25/25",
            "risks_mapped_to_crown_jewels": "12/12",
            "security_objectives_mapped_to_adrs": "12/12",
            "architecture_controls_mapped_to_adrs": "13/14"
        },

        "technical_assurance": {
            "risks_with_validation_evidence": "11/12",
            "attack_paths_with_validation_evidence": "7/8",
            "architecture_controls_with_validation_evidence": "11/14",
            "attack_path_statuses": dict(status_counts)
        },

        "accepted_residual_gaps": {
            "risk_without_validation_evidence": [
                "R-012"
            ],

            "attack_path_without_validation_evidence": [
                "AP-006"
            ],

            "controls_without_direct_validation_evidence": [
                "CTRL-001",
                "CTRL-011",
                "CTRL-013"
            ],

            "control_without_adr": [
                "CTRL-013"
            ],

            "risks_without_explicit_detection_mapping": [
                "R-009",
                "R-010",
                "R-012"
            ]
        },

        "assurance_conclusion": (
            "Traceability defects identified during "
            "Phase 13C were repaired where supported by "
            "existing architecture. Remaining gaps are "
            "retained as explicit technical or assurance "
            "limitations rather than being represented "
            "as validated."
        )
    }

    REPORT_JSON.write_text(
        json.dumps(
            assessment,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    markdown = """# Project Redoubt — Final Security Assurance Assessment

## Purpose

This assessment records the final Phase 13 security architecture assurance position after traceability remediation.

Phase 13 distinguishes between:

- traceability that can be repaired through architecture governance
- technical controls that have been implemented and validated
- controls that exist only as architectural intent
- attack paths that remain partially validated
- validation that must remain deferred

## End-to-End Traceability

| Relationship | Coverage |
|---|---:|
| Business Requirements → Security Requirements | 10 / 10 |
| Security Requirements → Security Objectives | 25 / 25 |
| Risks → Crown Jewels | 12 / 12 |
| Security Objectives → ADRs | 12 / 12 |
| Architecture Controls → ADRs | 13 / 14 |

The remaining ADR/control gap is CTRL-013 — Contractor Expiry.

Project Redoubt does not create an artificial ADR relationship for this lifecycle control.

## Technical Assurance

| Assurance Area | Coverage |
|---|---:|
| Risks with validation evidence | 11 / 12 |
| Attack paths with validation evidence | 7 / 8 |
| Architecture controls with direct validation evidence | 11 / 14 |

## Attack-Path Status

| Status | Count |
|---|---:|
| Substantially Validated | 2 |
| Partially Validated | 5 |
| Deferred | 1 |
| Fully Validated | 0 |

No attack path is represented as fully validated.

This is intentional.

The laboratory demonstrates meaningful control effectiveness without claiming production-grade adversary assurance.

## Accepted Residual Assurance Gaps

### R-012 / AP-006 — Research Exfiltration

Research intellectual-property exfiltration remains outside the implemented laboratory.

Meaningful validation requires:

- a research-data service
- collection/download telemetry
- external-transfer controls
- realistic insider-exfiltration scenarios

AP-006 remains DEFERRED.

### CTRL-001 — MFA

MFA is part of the architecture but phishing-resistant MFA strength has not been directly validated.

### CTRL-011 — Tamper-Resistant Logs

Central telemetry and detection are implemented.

Cryptographically protected, append-only or independently administered immutable logging is not.

### CTRL-013 — Contractor Expiry

Contractor authorisation restrictions are tested.

Automatic contractor account expiry and lifecycle enforcement are not currently exercised.

### Detection Coverage

R-009, R-010 and R-012 do not currently have explicit detection-rule mappings.

R-009 has recovery assurance.

R-010 has preventative contractor-access assurance.

R-012 remains outside the implemented laboratory.

## Assurance Interpretation

Project Redoubt has strong laboratory assurance for:

- Zero Trust authorisation
- application and network segmentation
- workload identity
- security telemetry
- detection engineering
- privileged management
- recovery isolation
- software supply-chain integrity
- deployment approval separation
- Infrastructure as Code security policy

The project retains explicit limitations for controls and scenarios that have not been meaningfully exercised.

## Final Assurance Principle

Documentation is not evidence.

Implementation is not automatically validation.

Validation is not automatically production assurance.

Project Redoubt only raises an assurance claim to the level supported by its actual implementation, test and evidence.
"""

    REPORT_MD.write_text(
        markdown,
        encoding="utf-8"
    )

    print(
        "=== Project Redoubt end-to-end assurance ==="
    )

    print(
        "[PASS] BR -> SR traceability: 10/10"
    )

    print(
        "[PASS] SR -> SO traceability: 25/25"
    )

    print(
        "[PASS] Risk -> Crown Jewel traceability: 12/12"
    )

    print(
        "[PASS] SO -> ADR traceability: 12/12"
    )

    print(
        "[PASS] ADR -> Control traceability: 13/14"
    )

    print(
        "[PASS] Known residual gaps remain explicit"
    )

    print()
    print(
        "PHASE 13D END-TO-END ASSURANCE: PASS"
    )


if __name__ == "__main__":
    main()
