# ADR-008 — Separate Release Signing from Deployment Approval

## Status

Accepted

## Context

A software artifact can be authentic and correctly built without necessarily being authorised for deployment into a particular environment.

If the same authority both signs a release and approves its deployment, compromise of that authority could collapse two independent trust decisions into one.

Project Redoubt therefore requires release integrity and deployment authorisation to remain separate security functions.

## Decision

Project Redoubt separates release signing from deployment approval.

The release-signing authority establishes artifact provenance and integrity.

A separate deployment-approval authority determines whether that verified artifact is authorised for deployment into a specific environment.

Separate Ed25519 key pairs are used for these functions.

## Security Drivers

The decision supports:

- separation of duties
- independent trust decisions
- reduced signing-key blast radius
- controlled deployment authority
- auditable release promotion

## Alternatives Considered

### Single Release Authority

One authority signs an artifact and authorises deployment.

Reason not selected:

- compromise creates excessive authority
- artifact authenticity and deployment approval become indistinguishable
- separation of duties is lost

### Deployment Based Only on Artifact Signature

Any correctly signed release is automatically deployable.

Reason not selected:

- authenticity does not establish environment-specific approval
- a valid but unintended artifact could be deployed

## Consequences

### Positive

- compromise of the release signer does not automatically grant deployment authority
- deployment approval can be independently revoked or constrained
- environment and expiry constraints can be applied separately
- release decisions become independently auditable

### Negative / Trade-offs

- additional key management is required
- release workflows contain an additional trust step
- availability of the approval authority affects deployment

## Security Traceability

### Risks

- R-006 — CI/CD Supply-Chain Compromise

### Attack Paths

- AP-004 — Developer to Software Supply Chain

### Security Objectives

- SO-006 — Protect Software Supply Chain
- SO-009 — Contain Compromise
- SO-012 — Produce Security Evidence

## Implementation

Implemented through Phase 10:

- trusted builder
- release provenance signer
- independent verifier
- independent release approver
- separate Ed25519 signing and approval key pairs
- short-lived deployment approval
- environment-bound approval claims

## Validation Evidence

Evidence includes:

- trusted build tests
- signed provenance validation
- independent release-verification receipts
- deployment-approval tests
- deployment-gate negative tests
- ADV-010 through ADV-016
- DET-013 through DET-020

## Residual Risk

The design does not eliminate:

- simultaneous compromise of both authorities
- malicious human approval
- compromised hosted build infrastructure
- production registry compromise
- compromise after successful deployment admission

## Review Triggers

Reconsider this ADR if:

- hardware-backed signing is introduced
- enterprise release-management infrastructure replaces the laboratory authority
- production deployment uses an external admission-control platform
