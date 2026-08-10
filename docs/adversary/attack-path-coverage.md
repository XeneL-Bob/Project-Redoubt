# Project Redoubt — Attack Path Validation Coverage

## Purpose

Not every Phase 3 attack path can be meaningfully validated with the current laboratory.

Project Redoubt does not claim implementation coverage for systems that do not yet exist.

## Current Coverage

| Attack Path | Description | Phase 7 Status |
|---|---|---|
| AP-001 | Phished Employee to Crown Jewel | Partially validated |
| AP-002 | Compromised Administrator | Partially validated |
| AP-003 | Public Application to Database | Substantially validated |
| AP-004 | Developer to Software Supply Chain | Deferred |
| AP-005 | Ransomware to Recovery Infrastructure | Partially validated |
| AP-006 | Insider Research Exfiltration | Deferred |
| AP-007 | Contractor to Internal Resource | Partially validated |
| AP-008 | Security Platform Compromise | Partially validated |

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

Phase 9 partially validates this attack path.

Validated controls include:

- dedicated privileged identities
- separate privileged OIDC client
- isolated management networks
- JIT privileged elevation
- short-lived elevation grants
- role-specific administrative domains
- trusted administrative device context
- management Policy Enforcement Point
- independent Admin OPA decisions
- management-backend workload credential
- privileged elevation detection
- repeated elevation-denial detection
- direct management-backend bypass detection
- management policy-bypass detection

Validated negative cases include:

- standard employee requests elevation
- privileged identity uses normal client
- privileged identity has no elevation
- administrator uses untrusted device
- administrator requests wrong privileged domain
- elevation grant crosses management domains
- elevation grant expires
- direct backend bypass is attempted

Not yet validated:

- phishing-resistant MFA
- real privileged workstation attestation
- real credential theft
- session revocation
- enterprise PAM integration
- production infrastructure administration
- administrator endpoint compromise

### AP-004 — Developer to Software Supply Chain

Requires:

- source repository controls
- CI/CD pipeline
- artifact validation
- deployment approval controls

### AP-005 — Ransomware to Recovery Infrastructure

Phase 8 now partially validates this attack path.

Validated controls include:

- dedicated recovery network
- production-to-recovery segmentation
- controlled Finance backup
- recovery-store integrity verification
- simulated production corruption
- isolated database restoration
- restored-data verification

Not yet validated:

- immutable or offline backup infrastructure
- backup-administrator compromise
- enterprise-wide ransomware propagation
- identity and infrastructure reconstruction

### AP-006 — Insider Research Exfiltration

Requires:

- research data service
- download and collection telemetry
- external-transfer control

### AP-008 — Security Platform Compromise

Phase 9 partially validates this attack path.

Validated controls include:

- separate security-admin identity
- JIT security-management elevation
- security-management role separation
- controlled security-control modification operation
- telemetry for privileged security operations
- DET-011 security-control modification detection
- DET-012 management policy-bypass detection
- management-backend bypass protection

The laboratory can identify expected security-control changes and detect privileged operations that occur outside the expected policy path.

Not yet validated:

- actual detection-rule replacement
- malicious deletion of detection rules
- suppression or deletion of existing alerts
- compromise of the detection-engine host
- immutable security telemetry
- independently administered evidence storage
- cryptographically protected audit logs


## Architectural Principle

A deferred test is preferable to a fabricated validation result.

Project Redoubt only marks an attack path as validated when the corresponding technical control exists and can be exercised.
