# Project Redoubt — Attack Path Validation Coverage

## Purpose

Not every Phase 3 attack path can be meaningfully validated with the current laboratory.

Project Redoubt does not claim implementation coverage for systems that do not yet exist.

## Current Coverage

| Attack Path | Description | Phase 7 Status |
|---|---|---|
| AP-001 | Phished Employee to Crown Jewel | Partially validated |
| AP-002 | Compromised Administrator | Deferred |
| AP-003 | Public Application to Database | Substantially validated |
| AP-004 | Developer to Software Supply Chain | Deferred |
| AP-005 | Ransomware to Recovery Infrastructure | Deferred |
| AP-006 | Insider Research Exfiltration | Deferred |
| AP-007 | Contractor to Internal Resource | Partially validated |
| AP-008 | Security Platform Compromise | Deferred |

## AP-001 Coverage

Validated controls include:

- least privilege
- restricted Finance access
- repeated unauthorised-access detection
- application segmentation
- contextual device trust

Not yet validated:

- phishing resistance
- MFA strength
- endpoint compromise
- privilege escalation mechanisms


## AP-003 Coverage

Validated controls include:

- application segmentation
- gateway-to-data isolation
- workload-specific credentials
- Vault-mediated secret access
- policy-path correlation
- direct-backend bypass detection
- secret-access anomaly detection

Not yet validated:

- application exploit resistance
- runtime exploit mitigation
- database privilege minimisation beyond the current application account


## AP-007 Coverage

Validated controls include:

- contractor role restriction
- explicit authorisation
- denial of access beyond approved scope

Not yet validated:

- contractor account expiry
- project-specific resource provisioning


## Deferred Attack Paths

### AP-002 — Compromised Administrator

Requires implementation of:

- privileged management plane
- administrative identities
- privileged-access workflows

### AP-004 — Developer to Software Supply Chain

Requires:

- source repository controls
- CI/CD pipeline
- artifact validation
- deployment approval controls

### AP-005 — Ransomware to Recovery Infrastructure

Requires:

- protected backup infrastructure
- recovery credentials
- recovery-network isolation
- restore workflow

### AP-006 — Insider Research Exfiltration

Requires:

- research data service
- download and collection telemetry
- external-transfer control

### AP-008 — Security Platform Compromise

Requires:

- detection administration interface
- rule-management control plane
- immutable or protected evidence storage

## Architectural Principle

A deferred test is preferable to a fabricated validation result.

Project Redoubt only marks an attack path as validated when the corresponding technical control exists and can be exercised.
