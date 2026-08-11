# ADR-005 — Separate Privileged Administration into a Dedicated Management Plane

## Status

Accepted

## Context

Administrative operations have substantially greater impact than normal user or workload activity.

Allowing privileged management through the same identities, interfaces and network paths used for normal business activity would increase the probability that compromise of a standard account or workload could progress directly into administrative control.

Project Redoubt therefore requires privileged administration to exist behind additional trust boundaries.

## Decision

Project Redoubt separates privileged administration into a dedicated management plane.

Management operations require:

- dedicated administrative identity
- explicit privileged role
- trusted administrative context
- short-lived elevation authority
- dedicated management Policy Enforcement Point
- independent administrative policy evaluation
- management-specific workload credentials
- management-plane telemetry

Normal application identities and normal application access paths are not sufficient to enter the management plane.

## Security Drivers

The decision supports:

- separation of privilege
- least privilege
- just-in-time administration
- reduced administrative attack surface
- containment of compromised standard identities
- explicit privileged-operation visibility

## Alternatives Considered

### Shared User and Administrator Identity

Users would perform administrative actions with their normal identities.

Reason not selected:

- compromise of a normal account could directly expose privileged authority
- normal and privileged activity would be harder to distinguish
- privilege separation would be weakened

### Shared Application and Management Network

Administrative APIs would be reachable through normal application paths.

Reason not selected:

- application compromise could provide a direct path toward management infrastructure
- administrative trust boundaries would depend excessively on application controls

### Permanent Administrative Privilege

Administrative accounts would retain persistent elevated permissions.

Reason not selected:

- increases the useful lifetime of compromised administrator credentials
- conflicts with least privilege and just-in-time access

## Consequences

### Positive

- administrative authority is separated from standard identity
- privileged operations cross additional enforcement boundaries
- elevation can be short lived
- management activity becomes independently observable
- compromise of an application identity does not automatically grant management access

### Negative / Trade-offs

- management infrastructure becomes an additional architecture domain
- privileged-access workflows become more complex
- elevation services must remain available
- administrative context and role lifecycle require governance

## Security Traceability

### Risks

- R-002
- R-011

### Attack Paths

- AP-002 — Compromised Administrator
- AP-008 — Security Platform Compromise

### Security Objectives

- SO-002 — Protect Privileged Access
- SO-009 — Contain Compromise

## Implementation

Implemented through Phase 9:

- dedicated administrator identities
- privileged OIDC client
- privilege broker
- short-lived signed elevation grants
- trusted-device context
- management Policy Enforcement Point
- independent administrative OPA policy
- isolated management networks
- dedicated management backend
- management-specific workload credential

## Validation Evidence

Evidence includes:

- standard users cannot obtain privileged elevation
- normal-client tokens cannot enter the management plane
- untrusted administrative devices are denied
- incorrect administrative roles are denied
- expired elevation grants are rejected
- direct management-backend bypass is blocked
- security-control modifications generate telemetry
- DET-007 through DET-012

## Residual Risk

The management plane does not eliminate:

- compromise of a legitimately elevated administrator
- compromise of the privilege broker
- compromise of administrative policy
- theft of valid short-lived elevation authority
- compromise of trusted administrative devices

Phishing-resistant MFA, stronger device attestation and enterprise PAM remain outside the current laboratory implementation.

## Review Triggers

Reconsider this ADR if:

- enterprise PAM replaces the current privilege broker
- privileged access moves to hardware-backed administrator workstations
- management infrastructure requires additional independent trust domains
