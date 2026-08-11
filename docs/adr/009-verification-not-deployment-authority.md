# ADR-009 — Treat Verification as Distinct from Deployment Authority

## Status

Accepted

## Context

Artifact verification answers whether a release satisfies integrity, provenance and trusted-build requirements.

It does not answer whether the artifact should be deployed at a particular time or into a particular environment.

Allowing a verifier to directly authorise deployment would give one component both assurance and execution authority.

## Decision

Project Redoubt explicitly separates verification from deployment authority.

A successful verification produces evidence that an artifact satisfies release policy.

It does not itself grant permission to deploy.

Deployment requires an additional independently signed approval that is validated again at the deployment boundary.

## Security Drivers

The decision supports:

- least authority
- independent release governance
- defence in depth
- separation of verification and execution
- environment-specific deployment control

## Alternatives Considered

### Verification Receipt Grants Deployment

A successful verifier output directly authorises deployment.

Reason not selected:

- verifier compromise becomes deployment compromise
- environment-specific authority cannot be independently controlled
- verification and execution authority collapse into one trust domain

### CI Success Grants Deployment

Successful CI automatically permits deployment.

Reason not selected:

- passing tests does not establish release approval
- compromised CI could otherwise obtain excessive deployment authority

## Consequences

### Positive

- verifier compromise alone is insufficient for deployment
- deployment requires a second independently verifiable trust decision
- approvals can be short lived and environment specific
- deployment admission can revalidate artifact integrity

### Negative / Trade-offs

- deployment requires additional coordination
- more cryptographic evidence must be handled
- approval expiry can interrupt release operations

## Security Traceability

### Risks

- R-006

### Attack Paths

- AP-004

### Security Objectives

- SO-006 — Protect Software Supply Chain
- SO-009 — Contain Compromise
- SO-011 — Make Policy Testable
- SO-012 — Produce Security Evidence

## Implementation

Implemented through:

- independent release verifier
- verification receipt
- separate release approver
- signed deployment approval
- deployment admission policy
- deployment gate
- artifact digest revalidation

## Validation Evidence

Phase 10 tests demonstrate that:

- verified artifacts without approval are denied deployment
- expired approval is rejected
- approval for the wrong environment is rejected
- mismatched artifacts are rejected
- deployment denial generates telemetry
- ADV-015 results in PREVENTED, DETECTED and CONTAINED

## Residual Risk

The decision does not protect against:

- compromise of both verifier and approver
- malicious authorised approval
- post-admission compromise
- production orchestrator compromise

## Review Triggers

Reconsider this ADR if:

- deployment approval moves to an enterprise change-management system
- Kubernetes or cloud-native admission control becomes the enforcement boundary
- release authority becomes hardware-backed or externally governed
