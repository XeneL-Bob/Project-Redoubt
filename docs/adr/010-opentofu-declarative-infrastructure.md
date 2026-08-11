# ADR-010 — Use OpenTofu for Declarative Infrastructure Modelling

## Status

Accepted

## Context

Project Redoubt requires infrastructure architecture to be reviewable, reproducible and suitable for automated security evaluation.

Manually configured infrastructure would make intended architecture difficult to compare with proposed changes and would reduce the ability to enforce security invariants before deployment.

## Decision

Project Redoubt uses OpenTofu as the declarative Infrastructure as Code model for its reference infrastructure architecture.

Infrastructure configuration is stored in version control and converted into machine-readable plans before deployment eligibility is considered.

The current implementation models an AWS reference architecture.

## Security Drivers

The decision supports:

- version-controlled infrastructure
- reproducible architecture
- machine-readable proposed state
- security review before deployment
- automated negative testing
- infrastructure evidence generation

## Alternatives Considered

### Manual Infrastructure Configuration

Infrastructure is configured directly through cloud consoles or administrative tools.

Reason not selected:

- difficult to review consistently
- changes may bypass version control
- automated policy evaluation becomes harder
- architecture drift becomes less visible

### Provider-Specific Imperative Scripts

Infrastructure is created through custom cloud API scripts.

Reason not selected:

- desired state is harder to reason about
- plan-based security evaluation is less consistent
- custom lifecycle logic increases maintenance burden

## Consequences

### Positive

- architecture changes are represented as code
- infrastructure plans can be inspected before application
- negative security scenarios can be generated reproducibly
- CI can validate proposed architecture
- infrastructure changes can produce auditable evidence

### Negative / Trade-offs

- provider configuration and state require governance
- Infrastructure as Code defects can propagate consistently
- production state management would require additional controls
- declarative configuration does not itself prevent insecure architecture

## Security Traceability

### Risks

- R-003
- R-004
- R-006
- R-009
- R-011

### Security Objectives

- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-010 — Maintain Recoverability
- SO-011 — Make Policy Testable
- SO-012 — Produce Security Evidence

## Implementation

Implemented through Phase 11:

- OpenTofu reference AWS environment
- segmented security zones
- controlled routing
- security-group trust paths
- encrypted evidence storage
- versioning
- KMS key rotation
- VPC flow logging
- provider lockfile

## Validation Evidence

Evidence includes:

- OpenTofu formatting validation
- OpenTofu initialisation
- configuration validation
- successful reference-plan generation
- controlled insecure-plan generation
- real-plan security testing
- GitHub Actions Infrastructure Security workflow

## Residual Risk

The current implementation does not claim:

- production AWS deployment
- production remote-state security
- live cloud-state verification
- continuous configuration-drift detection
- production IAM architecture

## Review Triggers

Reconsider this ADR if:

- a different Infrastructure as Code platform becomes the enterprise standard
- infrastructure moves away from declarative provisioning
- the target cloud architecture changes materially
