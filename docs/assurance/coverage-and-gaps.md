# Project Redoubt — Assurance Coverage and Gap Analysis

## Purpose

This report evaluates the Project Redoubt machine-readable assurance graph against current implementation and validation evidence.

A gap does not automatically mean that an architecture control is defective.

It means that the current assurance package does not establish the corresponding relationship or validation claim strongly enough to treat it as complete.

## Coverage Summary

| Assurance Area | Coverage |
|---|---:|
| Security requirements mapped to objectives | 25 / 25 |
| Crown jewels mapped to objectives | 10 / 10 |
| Security objectives mapped to ADRs | 12 / 12 |
| Security objectives with evidence | 12 / 12 |
| Risks with architecture controls | 11 / 12 |
| Risks with detection mappings | 9 / 12 |
| Risks with validation evidence | 11 / 12 |
| Attack paths with validation evidence | 7 / 8 |
| Architecture controls with validation evidence | 11 / 14 |

## Attack-Path Assurance

| Status | Count |
|---|---:|
| Substantially Validated | 2 |
| Partially Validated | 5 |
| Deferred | 1 |

No Project Redoubt attack path is currently described as fully validated.

This preserves the distinction between meaningful laboratory assurance and production-grade attack-path assurance.

## Traceability Findings

### Security Requirements Without Explicit Objective Mapping

None

The following currently have implementation or validation evidence despite the missing objective relationship:

None

This indicates a traceability deficiency rather than necessarily a missing technical control.

### Crown Jewels Without Objective Mapping

None

### Security Objectives Without ADR Mapping

None

## Risk Assurance Findings

### Risks Without Architecture-Control Mapping

R-012

### Risks Without Detection Mapping

R-009, R-010, R-012

A risk lacking a detection mapping is not automatically uncontrolled.

Preventive, recovery or containment evidence may still exist.

### Risks Without Current Validation Evidence

R-012

## Attack-Path Evidence Gaps

AP-006

## Architecture Controls Without Direct Validation Evidence

CTRL-001, CTRL-011, CTRL-013

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

CTRL-001, CTRL-011, CTRL-013

These correspond to areas such as MFA assurance, tamper-resistant logging and contractor expiry that are not yet fully exercised by the current laboratory.

### GAP-005 — Detection Coverage

Risks without explicit detection mappings are:

R-009, R-010, R-012

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
