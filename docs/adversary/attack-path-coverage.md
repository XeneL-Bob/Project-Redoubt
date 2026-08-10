# Project Redoubt — Attack Path Validation Coverage

## Purpose

Not every Phase 3 attack path can be meaningfully validated with the current laboratory.

Project Redoubt does not claim implementation coverage for systems that do not yet exist.

## Current Coverage

| Attack Path | Description | Current Status |
|---|---|---|
| AP-001 | Phished Employee to Crown Jewel | Partially validated |
| AP-002 | Compromised Administrator | Partially validated |
| AP-003 | Public Application to Database | Substantially validated |
| AP-004 | Developer to Software Supply Chain | Substantially validated |
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


## Additional Attack-Path Coverage

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

Phase 10 substantially validates this attack path.

Implemented preventive controls include:

- isolated trusted build execution
- deterministic release artifact construction
- read-only source mounting
- clean-source enforcement
- trusted builder identity enforcement
- SHA-256 artifact integrity verification
- Ed25519 signed release provenance
- builder and signer trust-domain separation
- release signing-key isolation
- independent release verification
- independent deployment approval authority
- separate deployment-approval Ed25519 key
- short-lived environment-bound deployment approval
- deployment approval signature validation
- post-approval artifact digest validation
- network-isolated deployment gate
- denial of deployment without valid approval

Implemented CI/CD controls include:

- GitHub Actions security workflow
- immutable action commit pinning
- explicit least-privilege workflow permissions
- disabled checkout credential persistence
- Gitleaks secret scanning
- CodeQL static analysis
- pull-request dependency review
- SPDX SBOM generation
- GitHub build provenance attestation
- GitHub SBOM attestation
- controlled release-evidence artifact generation

Implemented detective controls include:

- DET-013 — Supply Chain Artifact Integrity Failure
- DET-014 — Supply Chain Provenance Signature Failure
- DET-015 — Untrusted Builder Release Attempt
- DET-016 — Dirty Source Build Attempt
- DET-017 — Unsigned Release Attempt
- DET-018 — Release Without Correlated Trusted Build
- DET-019 — Deployment Approval Denied
- DET-020 — Deployment Gate Denied

Validated adversary scenarios include:

- ADV-010 — dirty-source build attempt
- ADV-011 — post-build artifact tampering
- ADV-012 — forged release provenance
- ADV-013 — signed artifact from an untrusted builder
- ADV-014 — unsigned release attempt
- ADV-015 — trusted-build path bypass against deployment boundary
- ADV-016 — build context attempts signing-key access

ADV-015 validates the complete abnormal path:

    Release Verifier ALLOW
            |
            +--> DET-018
            |
            v
    Independent Release Approver
            |
          DENY
            |
            +--> DET-019
            |
            v
    No Signed Deployment Approval
            |
            v
      Deployment Gate
            |
          DENY
            |
            +--> DET-020

The scenario therefore produces:

    PREVENTED
    DETECTED
    CONTAINED

AP-004 is classified as substantially validated rather than fully validated.

Remaining limitations include:

- GitHub repository branch/ruleset enforcement is not yet validated as an active repository control
- mandatory human pull-request approval is not validated
- GitHub-hosted runner compromise is outside the laboratory scope
- production registry admission control is not implemented
- production deployment infrastructure is simulated
- enterprise release-management integration is not implemented
- third-party dependency compromise is not exercised through a realistic production application dependency chain

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
