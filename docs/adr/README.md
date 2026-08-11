# Project Redoubt — Architecture Decision Records

## Purpose

Architecture Decision Records document significant architectural decisions made throughout Project Redoubt.

Each ADR records:

- the architectural problem or context
- the decision taken
- security drivers
- alternatives considered
- consequences and trade-offs
- links to risks, attack paths and security objectives
- implementation and validation evidence
- conditions that could cause the decision to be revisited

The ADR set provides evidence that Project Redoubt architecture decisions are deliberate, traceable and reviewable rather than incidental implementation choices.

## Decision Lifecycle

ADR status values are:

- Proposed — decision is under consideration
- Accepted — decision has been adopted
- Superseded — replaced by another ADR
- Deprecated — retained for history but no longer recommended
- Rejected — evaluated but not selected

Accepted ADRs may still contain residual risks or limitations.

## ADR Catalogue

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Adopt Zero Trust as the enterprise security model | Accepted |
| ADR-002 | Centralise policy decisions and distribute enforcement | Accepted |
| ADR-003 | Separate authentication from authorisation | Accepted |
| ADR-004 | Use dedicated workload identities instead of shared service credentials | Accepted |
| ADR-005 | Separate privileged administration into a management plane | Accepted |
| ADR-006 | Centralise security telemetry and detection | Accepted |
| ADR-007 | Isolate recovery infrastructure from production | Accepted |
| ADR-008 | Separate release signing from deployment approval | Accepted |
| ADR-009 | Treat verification as distinct from deployment authority | Accepted |
| ADR-010 | Use OpenTofu for declarative infrastructure modelling | Accepted |
| ADR-011 | Use OPA for infrastructure Policy as Code | Accepted |
| ADR-012 | Evaluate infrastructure plans before deployment authority | Accepted |

## Architecture Decision Chain

    Business Requirement
            ↓
    Security Requirement
            ↓
    Risk / Threat
            ↓
    Security Objective
            ↓
    Architecture Decision
            ↓
    Architecture Control
            ↓
    Implementation
            ↓
    Validation
            ↓
    Evidence

ADRs sit between security objectives and technical architecture controls.

They explain why a control architecture exists before describing how it is implemented.

## Scope

These ADRs document the Project Redoubt reference architecture for the fictional ResTech enterprise.

They are architecture records, not claims that the design has been deployed in a production enterprise environment.

## Supporting Governance Documents

- `decision-map.md` — maps architecture decisions to security objectives and implementation evidence.
- `phase-12-acceptance.md` — records Phase 12 completion criteria, assurance scope and limitations.

