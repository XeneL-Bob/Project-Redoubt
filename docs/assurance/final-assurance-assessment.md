# Project Redoubt — Final Security Assurance Assessment

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
