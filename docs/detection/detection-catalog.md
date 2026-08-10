# Project Redoubt — Detection Catalog

## Purpose

Phase 6 converts Project Redoubt security telemetry into testable detection logic.

Detection engineering follows:

Risk → Attack Behaviour → Telemetry → Detection Rule → Test → Alert → Evidence

## Detection Catalog

| ID | Detection | Severity | Related Risks |
|---|---|---:|---|
| DET-001 | Restricted Finance Resource Access Denied | Medium | R-001, R-005 |
| DET-002 | Finance Access Attempt from Untrusted Device | High | R-001, R-005 |
| DET-003 | Repeated Authorisation Denials | High | R-001, R-003 |
| DET-004 | Finance Application Policy Bypass | Critical | R-004, R-011 |
| DET-005 | Secret Access Without Policy Authorisation | Critical | R-007, R-011 |
| DET-006 | Direct Backend Access Attempt | High | R-003, R-011 |
| DET-007 | Privileged Elevation Denied | High | R-002, R-008 |
| DET-008 | Repeated Privileged Elevation Denials | Critical | R-002, R-008 |
| DET-009 | Direct Management Backend Access Attempt | Critical | R-002, R-008 |
| DET-010 | Privileged Access from Untrusted Device | High | R-002, R-008 |
| DET-011 | Security Control Modification | Medium | R-008 |
| DET-012 | Management Policy Bypass | Critical | R-002, R-008 |
| DET-013 | Supply Chain Artifact Integrity Failure | Critical | R-006 |
| DET-014 | Supply Chain Provenance Signature Failure | Critical | R-006 |
| DET-015 | Untrusted Builder Release Attempt | Critical | R-006 |
| DET-016 | Dirty Source Build Attempt | High | R-006 |
| DET-017 | Unsigned Release Attempt | High | R-006 |
| DET-018 | Release Without Correlated Trusted Build | Critical | R-006 |
| DET-019 | Deployment Approval Denied | Critical | R-006 |
| DET-020 | Deployment Gate Denied | Critical | R-006 |

## DET-001 — Restricted Finance Resource Access Denied

Detects an authenticated subject being denied access to the restricted Finance API.

Example conditions:

- employee attempting Finance access
- developer attempting Finance access
- authenticated identity without required Finance permissions

## DET-002 — Finance Access Attempt from Untrusted Device

Detects Finance access denied because contextual policy identifies the requesting device as untrusted.

This demonstrates contextual Zero Trust authorisation rather than role-only access control.

## DET-003 — Repeated Authorisation Denials

Detects three denied policy decisions for the same subject within sixty seconds.

This demonstrates threshold-based detection and basic temporal correlation.

## DET-004 — Finance Application Policy Bypass

Detects successful Finance application access where no correlated gateway policy ALLOW event exists.

This detection validates the expected control chain:

Gateway → Policy Decision → Finance API

A successful downstream action without that chain is treated as a critical architectural anomaly.

## DET-005 — Secret Access Without Policy Authorisation

Detects Finance Vault secret retrieval without a preceding correlated Finance policy ALLOW decision.

Potential causes include:

- compromised workload
- policy-path bypass
- unexpected workload execution
- broken enforcement architecture

## DET-006 — Direct Backend Access Attempt

Detects attempts to interact directly with protected application workloads using an invalid or missing workload-specific gateway credential.

This provides detection coverage for attempted Policy Enforcement Point bypass.

## Validation Requirement

A detection is not considered implemented merely because a rule exists.

Project Redoubt requires detections to be:

- reproducible
- deliberately triggerable
- validated by automated tests
- linked to documented risks
- supported by observable alert evidence

## Phase 9 — Privileged Management Detections

### DET-007 — Privileged Elevation Denied

Detects rejected JIT privileged-elevation requests.

### DET-008 — Repeated Privileged Elevation Denials

Detects three denied elevation attempts for the same subject within sixty seconds.

### DET-009 — Direct Management Backend Access Attempt

Detects attempted management Policy Enforcement Point bypass.

### DET-010 — Privileged Access from Untrusted Device

Detects management requests denied because administrative device trust is absent.

### DET-011 — Security Control Modification

Records authorised security-control modification activity.

### DET-012 — Management Policy Bypass

Detects successful privileged management activity without a correlated preceding management-gateway ALLOW decision.


## Phase 10 — Software Supply-Chain Detections

### DET-013 — Supply Chain Artifact Integrity Failure

Detects a release artifact whose calculated SHA-256 digest does not match the digest recorded in trusted provenance.

### DET-014 — Supply Chain Provenance Signature Failure

Detects release provenance that fails validation against the trusted release-signing public key.

### DET-015 — Untrusted Builder Release Attempt

Detects a release whose provenance identifies a builder that is not permitted by release policy.

A valid signature alone is therefore insufficient for release approval.

### DET-016 — Dirty Source Build Attempt

Detects a trusted-build request where source state is marked dirty.

### DET-017 — Unsigned Release Attempt

Detects release verification without the required provenance signature.

### DET-018 — Release Without Correlated Trusted Build

Detects an allowed release-verification event where no preceding trusted-builder ALLOW event exists for the same correlation identifier.

Expected control path:

    Trusted Builder ALLOW
            |
            v
    Signed Provenance
            |
            v
    Release Verifier ALLOW

A release-verifier ALLOW event without the trusted-build predecessor is treated as a critical supply-chain control-path anomaly.

## Phase 10 Validation

DET-013 through DET-020 are validated through:

- detection-engine unit tests
- live telemetry tests
- isolated builder and verifier execution
- AP-004 adversary scenarios ADV-010 through ADV-016

The trusted builder and verifier retain network isolation.

Supply-chain telemetry is written to a local spool and forwarded by a separate telemetry relay so the build components do not receive the central telemetry credential.


### DET-019 — Deployment Approval Denied

Detects a release rejected by the independent deployment approval authority.

Examples include:

- trusted-build correlation mismatch
- verification receipt mismatch
- untrusted builder
- release digest mismatch
- invalid release provenance
- prohibited deployment environment

### DET-020 — Deployment Gate Denied

Detects a release rejected at the final deployment admission boundary.

Examples include:

- missing deployment approval
- invalid deployment-approval signature
- expired deployment approval
- environment mismatch
- artifact modification after approval

## Phase 10 Deployment Detection Validation

DET-019 and DET-020 are validated through:

- detection-engine unit tests
- live telemetry relay validation
- independent deployment-gate tests
- AP-004 ADV-015 end-to-end adversary validation

The resulting control chain is:

    Build
      |
      v
    Verify
      |
      v
    Approve
      |
      v
    Deploy

Each major trust transition is independently validated rather than treating successful build verification as sufficient authority to deploy.
