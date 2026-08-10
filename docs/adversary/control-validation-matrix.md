# Project Redoubt — Adversary Control Validation Matrix

## Purpose

Phase 7 validates whether Project Redoubt controls behave as designed when exercised under controlled adversarial scenarios.

Each scenario records four possible security outcomes:

- PREVENTED — the attempted action was blocked
- DETECTED — the activity generated the expected security alert
- CONTAINED — the attacker could not progress beyond the tested boundary
- MISSED — the expected control or detection failed

A scenario may produce more than one successful outcome.

## Validation Matrix

| Scenario | Attack Path | Risks | Preventive Control | Detection | Expected Outcome |
|---|---|---|---|---|---|
| ADV-001 | AP-001 | R-001, R-003 | OPA least privilege | DET-001 | Prevented + Detected + Contained |
| ADV-002 | AP-001 | R-001, R-005 | Device trust policy | DET-002 | Prevented + Detected + Contained |
| ADV-003 | AP-001 | R-001, R-003 | Default-deny authorisation | DET-003 | Prevented + Detected + Contained |
| ADV-004 | AP-007 | R-010 | Contractor least privilege | — | Prevented + Contained |
| ADV-005 | AP-001 / AP-003 | R-003, R-011 | Application segmentation | — | Prevented + Contained |
| ADV-006 | AP-003 | R-004, R-011 | Data-tier segmentation | — | Prevented + Contained |
| ADV-007 | AP-003 | R-003, R-011 | Workload gateway credential | DET-006 | Prevented + Detected + Contained |
| ADV-008 | AP-003 | R-004, R-011 | Policy-path monitoring | DET-004 | Detected |
| ADV-009 | AP-003 | R-007, R-011 | Secret-access correlation | DET-005 | Detected |
| ADV-010 | AP-004 | R-006 | Clean-source build policy | DET-016 | Prevented + Detected + Contained |
| ADV-011 | AP-004 | R-006 | Artifact digest verification | DET-013 | Prevented + Detected + Contained |
| ADV-012 | AP-004 | R-006 | Signed provenance | DET-014 | Prevented + Detected + Contained |
| ADV-013 | AP-004 | R-006 | Trusted-builder policy | DET-015 | Prevented + Detected + Contained |
| ADV-014 | AP-004 | R-006 | Mandatory signed provenance | DET-017 | Prevented + Detected + Contained |
| ADV-015 | AP-004 | R-006 | Trusted-build correlation + independent deployment approval gate | DET-018, DET-019, DET-020 | Prevented + Detected + Contained |
| ADV-016 | AP-004 | R-006 | Builder/signer key separation | — | Prevented + Contained |

## Security Interpretation

Phase 7 distinguishes preventive and detective controls.

For example:

    ADV-007
        |
        v
    Attempt direct Finance API access
        |
        +--> Workload credential rejects request
        |       PREVENTED
        |
        +--> Finance API emits bypass telemetry
                |
                v
              DET-006
                |
             DETECTED

This provides stronger assurance than testing either prevention or detection independently.

## Control Validation Principle

Project Redoubt follows:

    Prevent
       |
       v
    Constrain
       |
       v
    Detect
       |
       v
    Contain
       |
       v
    Recover

Phase 7 currently validates Prevent, Constrain, Detect and Contain across the implemented Zero Trust laboratory.

Recovery validation remains a later phase because recovery infrastructure has not yet been implemented.
