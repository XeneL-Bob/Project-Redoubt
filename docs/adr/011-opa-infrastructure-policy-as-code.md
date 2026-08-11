# ADR-011 — Use OPA for Infrastructure Policy as Code

## Status

Accepted

## Context

Declarative infrastructure improves reviewability but does not guarantee that proposed infrastructure satisfies Project Redoubt security architecture.

Security requirements must therefore be converted into machine-enforceable rules capable of evaluating proposed infrastructure consistently.

## Decision

Project Redoubt uses Open Policy Agent and Rego to implement infrastructure Policy as Code.

OPA evaluates OpenTofu plan JSON against explicit infrastructure security invariants.

Policy decisions return structured ALLOW or DENY outcomes and identified violations.

## Security Drivers

The decision supports:

- machine-enforceable architecture rules
- consistent policy decisions
- automated negative testing
- pre-deployment security validation
- version-controlled security requirements
- machine-readable evidence

## Alternatives Considered

### Manual Architecture Review Only

Security architects manually inspect infrastructure changes.

Reason not selected:

- repetitive controls may be missed
- enforcement depends on reviewer consistency
- automated CI prevention is unavailable

### Custom Validation Scripts Only

Security requirements are implemented as bespoke procedural scripts.

Reason not selected:

- policy semantics become tightly coupled to implementation logic
- policy review and reuse become harder
- a dedicated policy language provides clearer separation of policy from execution

## Consequences

### Positive

- infrastructure rules are explicit and reviewable
- policies can be unit tested
- real OpenTofu plans can be evaluated
- insecure changes can fail CI
- policy results can be incorporated into evidence

### Negative / Trade-offs

- Rego expertise is required
- policy defects can create false allows or false denials
- policy coverage must evolve with the architecture
- OPA becomes part of the infrastructure security toolchain

## Security Traceability

### Risks

- R-003
- R-004
- R-006
- R-008
- R-009
- R-011

### Security Objectives

- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-007 — Centralise Security Visibility
- SO-010 — Maintain Recoverability
- SO-011 — Make Policy Testable
- SO-012 — Produce Security Evidence

## Implementation

Phase 11 implements IAC-001 through IAC-011 covering:

- permitted public ingress
- public SSH prohibition
- public IP restrictions
- default-route restrictions
- evidence-storage public-access controls
- KMS encryption
- storage versioning
- KMS rotation
- complete VPC flow logging
- required security metadata
- unrestricted egress prohibition

## Validation Evidence

Each IAC control is validated through:

- policy unit tests
- synthetic negative inputs
- real OpenTofu negative plans
- CI enforcement
- machine-readable policy evidence

## Residual Risk

OPA enforcement only covers rules that have been explicitly encoded.

The architecture remains exposed to:

- missing policies
- incorrect Rego logic
- unsupported infrastructure types
- policy bypass outside the enforced CI path
- live cloud drift after deployment

## Review Triggers

Reconsider this ADR if:

- enterprise policy tooling changes
- policy evaluation moves into a cloud-native admission platform
- infrastructure schemas require a different policy model
