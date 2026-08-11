# ADR-002 — Centralise Policy Decisions and Distribute Enforcement

## Status

Accepted

## Context

Project Redoubt contains multiple applications, APIs, workloads and administrative interfaces.

Embedding independent authorisation logic into every service would create inconsistent policy implementations and make enterprise access-control behaviour difficult to review, test and govern.

At the same time, a single central gateway cannot enforce every security boundary.

## Decision

Project Redoubt separates policy decision from policy enforcement.

Policy decisions are evaluated by centralised policy engines.

Enforcement occurs at distributed Policy Enforcement Points positioned at relevant application, workload and management boundaries.

The architectural model is:

    Request
       ↓
    Enforcement Point
       ↓
    Policy Decision
       ↓
    ALLOW / DENY
       ↓
    Enforcement Point
       ↓
    Protected Resource

The policy engine decides.

The enforcement point enforces.

## Security Drivers

The decision supports:

- consistent enterprise policy
- explicit authorisation
- central policy review
- testable policy behaviour
- distributed protection of resources
- observable security decisions

## Alternatives Considered

### Application-Local Authorisation

Each application would independently implement access-control logic.

Reason not selected:

- policy behaviour could diverge between services
- security rules would be harder to audit
- duplicated implementation increases configuration risk

### Single Central Security Gateway

All enforcement would occur at one gateway.

Reason not selected:

- backend and management interfaces require independent enforcement
- a gateway cannot reliably represent every workload trust boundary
- gateway compromise could otherwise bypass all authorisation

## Consequences

### Positive

- policy logic can be version controlled
- access decisions become consistent and testable
- enforcement can exist at several trust boundaries
- policy updates do not require rewriting every application
- security decisions generate central telemetry

### Negative / Trade-offs

- policy engines become security-critical infrastructure
- availability of policy decisions must be considered
- request context must be transported correctly
- disagreement between policy and enforcement implementations can create defects

## Security Traceability

### Risks

- R-001
- R-003
- R-004
- R-010
- R-011

### Attack Paths

- AP-001
- AP-003
- AP-007

### Security Objectives

- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-009 — Contain Compromise
- SO-011 — Make Policy Testable

## Implementation

Implemented through:

- OPA policy engines
- API gateway Policy Enforcement Point
- management Policy Enforcement Point
- workload credentials
- contextual access decisions
- dedicated management policy
- OpenTofu infrastructure policy evaluation

## Validation Evidence

Evidence includes:

- OPA policy tests
- Zero Trust smoke tests
- unauthorised Finance access denial
- contractor scope denial
- backend bypass testing
- management-plane bypass testing
- infrastructure negative-policy tests

## Residual Risk

The design does not eliminate:

- incorrect policy logic
- policy-engine compromise
- forged decision context
- enforcement-point compromise
- policy availability failures

Independent detection and segmentation controls remain required.

## Review Triggers

Reconsider this ADR if:

- authorisation requirements cannot be represented consistently
- policy-engine availability becomes unacceptable
- a new architecture requires autonomous disconnected policy decisions
