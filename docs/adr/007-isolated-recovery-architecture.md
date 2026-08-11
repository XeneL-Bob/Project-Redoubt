# ADR-007 — Isolate Recovery Infrastructure from Production

## Status

Accepted

## Context

Backups that remain fully accessible from normal production workloads can be damaged or destroyed during ransomware, destructive administrator activity or production compromise.

Recovery capability must therefore survive compromise of the environment it is intended to restore.

## Decision

Project Redoubt separates recovery infrastructure from normal production workloads.

Recovery data and restore operations exist behind a distinct recovery boundary.

Normal production services do not receive direct membership in the recovery network.

Restoration requires integrity verification before data is admitted into the recovery environment.

## Security Drivers

The decision supports:

- ransomware resilience
- recovery-plane isolation
- preservation of known-good data
- integrity-gated restoration
- reduced production blast radius
- recovery from compromised production state

## Alternatives Considered

### Production-Accessible Backup Storage

Backups remain directly reachable from production workloads.

Reason not selected:

- production compromise could extend directly into backup infrastructure
- ransomware could affect both production and recoverability

### Recovery from Production Replicas Only

Production replicas are treated as sufficient recovery copies.

Reason not selected:

- destructive changes may replicate
- replicas primarily support availability, not independent trusted recovery

## Consequences

### Positive

- production compromise does not automatically provide recovery access
- backup data can remain independent from modified production state
- restoration can be integrity checked
- recovery behaviour can be tested separately from production

### Negative / Trade-offs

- separate recovery infrastructure must be maintained
- backup and restore procedures become more controlled
- recovery testing requires dedicated resources
- isolation alone does not provide immutability

## Security Traceability

### Risks

- R-009

### Attack Paths

- AP-005 — Ransomware to Recovery Infrastructure

### Security Objectives

- SO-009 — Contain Compromise
- SO-010 — Maintain Recoverability
- SO-012 — Produce Security Evidence

## Implementation

Implemented through Phase 8:

- dedicated recovery network
- isolated recovery database
- controlled Finance backup workflow
- protected recovery storage
- SHA-256 backup integrity verification
- integrity-gated restoration
- independent recovery-data validation

## Validation Evidence

Project Redoubt demonstrated:

- known-good Finance data backup
- recorded backup SHA-256
- deliberate modification of production data after backup
- recovery data remaining independent from production state
- integrity validation before restoration
- successful restore into isolated recovery database
- restored data matching known-good state
- production workload inability to resolve the recovery database

## Residual Risk

The current architecture does not provide:

- physically offline backups
- immutable storage
- backup-administrator compromise testing
- complete enterprise reconstruction
- independent cloud-account recovery isolation

AP-005 therefore remains only partially validated.

## Review Triggers

Reconsider this ADR if:

- immutable backup technology is introduced
- recovery moves into a separate cloud account or subscription
- regulatory recovery objectives change
- full enterprise rebuild capability becomes required
