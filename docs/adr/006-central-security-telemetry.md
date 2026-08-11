# ADR-006 — Centralise Security Telemetry and Detection

## Status

Accepted

## Context

Project Redoubt security decisions occur across identity, policy, application, workload, secrets, management, deployment and recovery components.

If each component retained security events independently, correlation between attack stages would be difficult and compromise could progress without producing an enterprise-level security view.

## Decision

Project Redoubt centralises security-relevant telemetry and evaluates it through a dedicated detection capability.

Security events should retain sufficient structured context to correlate activity across trust boundaries.

Where possible, events use correlation identifiers to connect related actions.

Detection processing remains logically separated from protected application workloads.

## Security Drivers

The decision supports:

- central security visibility
- correlation across security boundaries
- attack-path detection
- incident reconstruction
- policy-bypass detection
- evidence generation
- incident-response initiation

## Alternatives Considered

### Application-Local Logging Only

Each service retains its own operational logs.

Reason not selected:

- cross-service attacks become difficult to reconstruct
- individual application compromise may hide local evidence
- enterprise detection rules cannot correlate activity easily

### Network Telemetry Only

Security monitoring relies primarily on network traffic.

Reason not selected:

- authorisation decisions and identity context may not be visible
- encrypted application traffic limits semantic visibility
- management and policy decisions require application-level events

## Consequences

### Positive

- security events can be correlated across systems
- policy decisions can be linked to downstream actions
- detections can identify missing expected security events
- central evidence supports incident response
- attack simulations can validate observable behaviour

### Negative / Trade-offs

- telemetry infrastructure becomes security-sensitive
- event schemas must remain consistent
- high event volume can increase processing requirements
- central visibility may be reduced if telemetry delivery fails

## Security Traceability

### Risks

- R-001
- R-002
- R-003
- R-008

### Attack Paths

- Multiple attack paths

### Security Objectives

- SO-007 — Centralise Security Visibility
- SO-008 — Detect High-Risk Behaviour
- SO-012 — Produce Security Evidence

## Implementation

Implemented through:

- structured JSON security events
- central telemetry collection
- correlation identifiers
- dedicated detection engine
- threshold rules
- missing-prior-event detection
- incident-response processing
- supply-chain telemetry
- management telemetry
- infrastructure policy evidence

## Validation Evidence

Project Redoubt has validated:

- DET-001 through DET-020
- threshold-based detections
- policy-path bypass detection
- secret-access anomaly detection
- direct backend access detection
- management-plane detection
- supply-chain detection
- deployment-gate detection
- incident creation from critical alerts

## Residual Risk

Central telemetry does not guarantee evidence immutability.

The current laboratory architecture does not claim:

- production SIEM durability
- cryptographically append-only event storage
- independent long-term log archival
- protection from complete telemetry-platform compromise

These remain residual production architecture concerns.

## Review Triggers

Reconsider this ADR if:

- telemetry volume requires distributed processing
- independent security domains require separate collectors
- immutable event infrastructure is introduced
- enterprise SIEM integration replaces the laboratory detection pipeline
