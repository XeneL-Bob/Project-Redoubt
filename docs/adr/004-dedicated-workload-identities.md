# ADR-004 — Use Dedicated Workload Identities Instead of Shared Service Credentials

## Status

Accepted

## Context

Project Redoubt services communicate across application, policy, secrets and data boundaries.

Shared credentials would make it difficult to determine which workload performed an action and could allow compromise of one service to impersonate another service using the same credential.

Static secrets also increase exposure when credentials must be distributed to multiple workloads.

## Decision

Project Redoubt assigns distinct identities and credentials to security-sensitive workloads.

Workload access is authorised according to the identity of the calling workload rather than only its network location.

Credentials should be scoped to the service and purpose for which they are issued.

Shared enterprise-wide service credentials are not an accepted architecture pattern.

## Security Drivers

The decision supports:

- service-to-service authentication
- least privilege
- workload accountability
- reduced credential reuse
- workload segmentation
- stronger secret-access policy
- containment following workload compromise

## Alternatives Considered

### Shared Service Credentials

Multiple workloads use the same credential.

Reason not selected:

- individual workload actions become difficult to attribute
- compromise of one service compromises the shared identity
- credential rotation affects multiple unrelated services

### Network-Only Workload Trust

Services trust requests based primarily on network membership.

Reason not selected:

- network access does not prove workload identity
- lateral movement inside a permitted network becomes easier
- backend bypass cannot be distinguished reliably

## Consequences

### Positive

- workloads can be independently authorised
- compromise can be constrained to a service identity
- credential use becomes attributable
- secret access can be linked to workload policy
- backend services can reject unauthorised callers

### Negative / Trade-offs

- identity lifecycle management is required
- credentials or tokens require rotation
- secret-management availability becomes important
- additional configuration is required for each workload

## Security Traceability

### Risks

- R-004
- R-007
- R-011

### Attack Paths

- AP-003 — Public Application to Database

### Security Objectives

- SO-004 — Protect Sensitive Data
- SO-005 — Protect Workload Identity
- SO-009 — Contain Compromise

## Implementation

Implemented through:

- dedicated service credentials
- Vault workload secrets
- gateway workload identity
- Finance backend workload credentials
- management-backend credentials
- explicit workload authorisation
- network segmentation

## Validation Evidence

Evidence includes:

- invalid workload credential rejection
- direct backend bypass denial
- workload lateral-movement tests
- secret-access correlation
- DET-005 secret-access anomaly detection
- DET-006 direct backend access detection
- DET-009 direct management backend detection

## Residual Risk

Dedicated identities do not eliminate:

- workload credential theft
- compromised workloads acting within their authorised scope
- secrets-manager compromise
- excessive identity permissions
- credential lifecycle failure

Short-lived credentials, segmentation and telemetry remain required.

## Review Triggers

Reconsider this ADR if:

- workload identity moves to a different trust mechanism
- certificate-based or platform-native workload identity replaces current credentials
- workloads require a federated service-identity architecture
