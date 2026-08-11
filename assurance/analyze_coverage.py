#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GRAPH_PATH = (
    ROOT
    / "assurance"
    / "traceability-graph.json"
)

EVIDENCE_PATH = (
    ROOT
    / "assurance"
    / "evidence-catalog.json"
)

REPORT_JSON = (
    ROOT
    / "assurance"
    / "coverage-report.json"
)

REPORT_MD = (
    ROOT
    / "docs"
    / "assurance"
    / "coverage-and-gaps.md"
)


def fail(message):
    print(
        f"[FAIL] {message}"
    )
    raise SystemExit(1)


def id_range(
    prefix,
    start,
    end,
):
    return {
        f"{prefix}-{n:03d}"
        for n in range(
            start,
            end + 1
        )
    }


def union_field(
    records,
    field,
):
    result = set()

    for record in records:
        result.update(
            record.get(
                field,
                []
            )
        )

    return result


def fmt_ids(values):
    values = sorted(values)

    if not values:
        return "None"

    return ", ".join(values)


def main():

    graph = json.loads(
        GRAPH_PATH.read_text(
            encoding="utf-8"
        )
    )

    evidence = json.loads(
        EVIDENCE_PATH.read_text(
            encoding="utf-8"
        )
    )

    packages = evidence[
        "evidence_packages"
    ]

    all_sr = id_range(
        "SR",
        1,
        25
    )

    all_cj = id_range(
        "CJ",
        1,
        10
    )

    all_risks = id_range(
        "R",
        1,
        12
    )

    all_aps = id_range(
        "AP",
        1,
        8
    )

    all_sos = id_range(
        "SO",
        1,
        12
    )

    objective_sr = union_field(
        graph["objective_mappings"],
        "security_requirements",
    )

    objective_cj = union_field(
        graph["objective_mappings"],
        "crown_jewels",
    )

    adr_objectives = union_field(
        graph["adrs"],
        "objectives",
    )

    control_risks = union_field(
        graph["architecture_controls"],
        "risks",
    )

    detection_risks = union_field(
        graph["detections"],
        "risks",
    )

    evidence_sr = union_field(
        packages,
        "supports_security_requirements",
    )

    evidence_risks = union_field(
        packages,
        "risks",
    )

    evidence_aps = union_field(
        packages,
        "attack_paths",
    )

    evidence_objectives = union_field(
        packages,
        "objectives",
    )

    evidence_controls = union_field(
        packages,
        "controls",
    )

    all_controls = {
        record["id"]
        for record
        in graph[
            "architecture_controls"
        ]
    }

    expected_controls = {
        f"CTRL-{n:03d}"
        for n in range(
            1,
            15
        )
    }

    if all_controls != expected_controls:
        fail(
            "Architecture-control IDs "
            "are not CTRL-001 through CTRL-014"
        )

    known_graph_ids = (
        all_sr
        | all_cj
        | all_risks
        | all_aps
        | all_sos
        | id_range(
            "ADV",
            1,
            16
        )
        | id_range(
            "DET",
            1,
            20
        )
        | id_range(
            "IAC",
            1,
            11
        )
        | all_controls
    )

    package_ids = set()

    for package in packages:

        package_id = package["id"]

        if package_id in package_ids:
            fail(
                f"Duplicate evidence package "
                f"{package_id}"
            )

        package_ids.add(
            package_id
        )

        for field in (
            "supports_security_requirements",
            "risks",
            "attack_paths",
            "objectives",
            "controls",
            "adversary_scenarios",
            "detections",
            "iac_controls",
        ):

            for identifier in package.get(
                field,
                []
            ):

                if identifier not in known_graph_ids:
                    fail(
                        f"{package_id}: unknown "
                        f"identifier {identifier}"
                    )

        for relative_path in (
            package.get(
                "tests",
                []
            )
            + package.get(
                "documentation",
                []
            )
        ):

            candidate = (
                ROOT
                / relative_path
            )

            if not candidate.exists():
                fail(
                    f"{package_id}: referenced "
                    f"path missing: {relative_path}"
                )

    missing_objective_sr = (
        all_sr
        - objective_sr
    )

    missing_objective_cj = (
        all_cj
        - objective_cj
    )

    missing_adr_objectives = (
        all_sos
        - adr_objectives
    )

    risks_without_controls = (
        all_risks
        - control_risks
    )

    risks_without_detection = (
        all_risks
        - detection_risks
    )

    risks_without_evidence = (
        all_risks
        - evidence_risks
    )

    aps_without_evidence = (
        all_aps
        - evidence_aps
    )

    objectives_without_evidence = (
        all_sos
        - evidence_objectives
    )

    controls_without_evidence = (
        all_controls
        - evidence_controls
    )

    evidence_backed_unmapped_sr = (
        missing_objective_sr
        & evidence_sr
    )

    status_counts = Counter(
        record["status"]
        for record
        in graph["attack_paths"]
    )

    gaps = [
        {
            "id": "GAP-001",
            "severity": "MEDIUM",
            "type": "TRACEABILITY",
            "title": (
                "Business requirement to security "
                "requirement relationships are not "
                "machine-readable"
            ),
            "detail": (
                "The assurance model contains BR and SR "
                "identifiers, but does not yet contain an "
                "explicit BR-to-SR relationship layer."
            )
        },
        {
            "id": "GAP-002",
            "severity": "MEDIUM",
            "type": "TRACEABILITY",
            "title": (
                "Security requirements with implementation "
                "evidence are not explicitly mapped to "
                "security objectives"
            ),
            "identifiers": sorted(
                evidence_backed_unmapped_sr
            )
        },
        {
            "id": "GAP-003",
            "severity": "HIGH",
            "type": "ASSURANCE",
            "title": (
                "Research intellectual-property theft "
                "remains outside current technical "
                "validation"
            ),
            "identifiers": [
                "R-012",
                "AP-006"
            ]
        },
        {
            "id": "GAP-004",
            "severity": "MEDIUM",
            "type": "CONTROL_VALIDATION",
            "title": (
                "Architecture controls without direct "
                "validation evidence packages"
            ),
            "identifiers": sorted(
                controls_without_evidence
            )
        },
        {
            "id": "GAP-005",
            "severity": "MEDIUM",
            "type": "DETECTION",
            "title": (
                "Risks without explicit detection mapping"
            ),
            "identifiers": sorted(
                risks_without_detection
            )
        },
        {
            "id": "GAP-006",
            "severity": "MEDIUM",
            "type": "TRACEABILITY",
            "title": (
                "Risk-to-crown-jewel relationships remain "
                "documented in the risk register but are "
                "not yet represented in the machine-readable "
                "assurance graph"
            )
        }
    ]

    summary = {
        "security_requirements_total": len(
            all_sr
        ),
        "security_requirements_mapped_to_objectives": len(
            objective_sr
        ),
        "crown_jewels_total": len(
            all_cj
        ),
        "crown_jewels_mapped_to_objectives": len(
            objective_cj
        ),
        "risks_total": len(
            all_risks
        ),
        "risks_with_architecture_controls": len(
            control_risks
        ),
        "risks_with_detection_mapping": len(
            detection_risks
        ),
        "risks_with_evidence": len(
            evidence_risks
        ),
        "attack_paths_total": len(
            all_aps
        ),
        "attack_paths_with_evidence": len(
            evidence_aps
        ),
        "security_objectives_total": len(
            all_sos
        ),
        "security_objectives_with_adr_mapping": len(
            adr_objectives
        ),
        "security_objectives_with_evidence": len(
            evidence_objectives
        ),
        "architecture_controls_total": len(
            all_controls
        ),
        "architecture_controls_with_evidence": len(
            evidence_controls
        ),
        "evidence_packages": len(
            packages
        ),
        "attack_path_statuses": dict(
            sorted(
                status_counts.items()
            )
        )
    }

    report = {
        "schema": (
            "project-redoubt."
            "assurance-coverage-report/v1"
        ),
        "summary": summary,
        "gaps": gaps,
        "detail": {
            "security_requirements_without_objective_mapping": sorted(
                missing_objective_sr
            ),
            "security_requirements_without_objective_mapping_but_with_evidence": sorted(
                evidence_backed_unmapped_sr
            ),
            "crown_jewels_without_objective_mapping": sorted(
                missing_objective_cj
            ),
            "objectives_without_adr_mapping": sorted(
                missing_adr_objectives
            ),
            "risks_without_architecture_controls": sorted(
                risks_without_controls
            ),
            "risks_without_detection_mapping": sorted(
                risks_without_detection
            ),
            "risks_without_evidence": sorted(
                risks_without_evidence
            ),
            "attack_paths_without_evidence": sorted(
                aps_without_evidence
            ),
            "objectives_without_evidence": sorted(
                objectives_without_evidence
            ),
            "controls_without_evidence": sorted(
                controls_without_evidence
            )
        }
    }

    REPORT_JSON.write_text(
        json.dumps(
            report,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    md = f"""# Project Redoubt — Assurance Coverage and Gap Analysis

## Purpose

This report evaluates the Project Redoubt machine-readable assurance graph against current implementation and validation evidence.

A gap does not automatically mean that an architecture control is defective.

It means that the current assurance package does not establish the corresponding relationship or validation claim strongly enough to treat it as complete.

## Coverage Summary

| Assurance Area | Coverage |
|---|---:|
| Security requirements mapped to objectives | {len(objective_sr)} / {len(all_sr)} |
| Crown jewels mapped to objectives | {len(objective_cj)} / {len(all_cj)} |
| Security objectives mapped to ADRs | {len(adr_objectives)} / {len(all_sos)} |
| Security objectives with evidence | {len(evidence_objectives)} / {len(all_sos)} |
| Risks with architecture controls | {len(control_risks)} / {len(all_risks)} |
| Risks with detection mappings | {len(detection_risks)} / {len(all_risks)} |
| Risks with validation evidence | {len(evidence_risks)} / {len(all_risks)} |
| Attack paths with validation evidence | {len(evidence_aps)} / {len(all_aps)} |
| Architecture controls with validation evidence | {len(evidence_controls)} / {len(all_controls)} |

## Attack-Path Assurance

| Status | Count |
|---|---:|
| Substantially Validated | {status_counts.get("SUBSTANTIALLY_VALIDATED", 0)} |
| Partially Validated | {status_counts.get("PARTIALLY_VALIDATED", 0)} |
| Deferred | {status_counts.get("DEFERRED", 0)} |

No Project Redoubt attack path is currently described as fully validated.

This preserves the distinction between meaningful laboratory assurance and production-grade attack-path assurance.

## Traceability Findings

### Security Requirements Without Explicit Objective Mapping

{fmt_ids(missing_objective_sr)}

The following currently have implementation or validation evidence despite the missing objective relationship:

{fmt_ids(evidence_backed_unmapped_sr)}

This indicates a traceability deficiency rather than necessarily a missing technical control.

### Crown Jewels Without Objective Mapping

{fmt_ids(missing_objective_cj)}

### Security Objectives Without ADR Mapping

{fmt_ids(missing_adr_objectives)}

## Risk Assurance Findings

### Risks Without Architecture-Control Mapping

{fmt_ids(risks_without_controls)}

### Risks Without Detection Mapping

{fmt_ids(risks_without_detection)}

A risk lacking a detection mapping is not automatically uncontrolled.

Preventive, recovery or containment evidence may still exist.

### Risks Without Current Validation Evidence

{fmt_ids(risks_without_evidence)}

## Attack-Path Evidence Gaps

{fmt_ids(aps_without_evidence)}

## Architecture Controls Without Direct Validation Evidence

{fmt_ids(controls_without_evidence)}

These controls should not be described as validated solely because they appear in architecture documentation.

## Material Assurance Gaps

### GAP-001 — BR to SR Traceability

Business requirements and security requirements exist as authoritative identifiers, but their relationships are not yet represented in the machine-readable assurance graph.

### GAP-002 — Objective Traceability

SR-008, SR-015 and SR-019 have implementation or validation evidence but are not explicitly mapped into the security-objective layer.

This is a governance/traceability gap.

### GAP-003 — Research Exfiltration

R-012 and AP-006 remain outside the implemented laboratory.

AP-006 is deliberately DEFERRED.

A research-data service, collection telemetry and external-transfer controls would be required for meaningful validation.

### GAP-004 — Unvalidated Architecture Controls

Current architecture controls without direct validation evidence packages are:

{fmt_ids(controls_without_evidence)}

These correspond to areas such as MFA assurance, tamper-resistant logging and contractor expiry that are not yet fully exercised by the current laboratory.

### GAP-005 — Detection Coverage

Risks without explicit detection mappings are:

{fmt_ids(risks_without_detection)}

R-009 has recovery evidence and R-010 has preventative contractor-access testing, so the lack of a detection mapping should not be interpreted as absence of all control coverage.

### GAP-006 — Risk-to-Crown-Jewel Graph

Risk-to-crown-jewel relationships exist in the human-readable risk register but are not yet represented in the machine-readable assurance graph.

This prevents the current graph from traversing the full intended chain:

    Crown Jewel
        ↓
    Risk
        ↓
    Attack Path

## Interpretation

Project Redoubt currently has strong evidence in:

- application Zero Trust enforcement
- segmentation
- workload identity
- detection engineering
- privileged management
- isolated recovery
- software supply-chain controls
- infrastructure Policy as Code

The largest remaining assurance gaps are concentrated in:

- explicit end-to-end traceability
- phishing-resistant MFA validation
- immutable or tamper-resistant telemetry
- contractor lifecycle expiry
- research exfiltration
- production-grade validation boundaries

These gaps are intentionally retained rather than hidden by unsupported assurance claims.
"""

    REPORT_MD.write_text(
        md,
        encoding="utf-8"
    )

    print(
        "=== Project Redoubt coverage analysis ==="
    )

    print(
        f"[PASS] Security requirements mapped "
        f"to objectives: {len(objective_sr)}/25"
    )

    print(
        f"[PASS] Crown jewels mapped "
        f"to objectives: {len(objective_cj)}/10"
    )

    print(
        f"[PASS] Objectives mapped to ADRs: "
        f"{len(adr_objectives)}/12"
    )

    print(
        f"[PASS] Risks with architecture "
        f"controls: {len(control_risks)}/12"
    )

    print(
        f"[PASS] Risks with evidence: "
        f"{len(evidence_risks)}/12"
    )

    print(
        f"[PASS] Attack paths with evidence: "
        f"{len(evidence_aps)}/8"
    )

    print(
        f"[PASS] Controls with evidence: "
        f"{len(evidence_controls)}/14"
    )

    print()

    print(
        "[INFO] Objective mapping gaps: "
        + fmt_ids(
            missing_objective_sr
        )
    )

    print(
        "[INFO] Risks without control mapping: "
        + fmt_ids(
            risks_without_controls
        )
    )

    print(
        "[INFO] Risks without detection mapping: "
        + fmt_ids(
            risks_without_detection
        )
    )

    print(
        "[INFO] Attack paths without evidence: "
        + fmt_ids(
            aps_without_evidence
        )
    )

    print(
        "[INFO] Controls without evidence: "
        + fmt_ids(
            controls_without_evidence
        )
    )

    print()

    print(
        "[PASS] Coverage and gap reports generated"
    )

    print(
        "PHASE 13C COVERAGE ANALYSIS: PASS"
    )


if __name__ == "__main__":
    main()
