# Project Redoubt — Phase 12 Acceptance

## Phase

Phase 12 — Architecture Decision Records

## Objective

The objective of Phase 12 is to make significant Project Redoubt security architecture decisions explicit, reviewable, traceable and defensible.

The phase documents why major architectural choices were made rather than leaving those decisions implicit within implementation code.

## Implemented Capabilities

Phase 12 provides:

- a formal ADR lifecycle
- a reusable ADR template
- twelve accepted architecture decisions
- documented alternatives considered
- security drivers
- consequences and architectural trade-offs
- security-objective traceability
- implementation references
- validation-evidence references
- explicit residual-risk statements
- review triggers
- an architecture decision map
- integration with the overall Project Redoubt architecture model

## Accepted Architecture Decisions

- ADR-001 — Adopt Zero Trust as the Enterprise Security Model
- ADR-002 — Centralise Policy Decisions and Distribute Enforcement
- ADR-003 — Separate Authentication from Authorisation
- ADR-004 — Use Dedicated Workload Identities Instead of Shared Service Credentials
- ADR-005 — Separate Privileged Administration into a Dedicated Management Plane
- ADR-006 — Centralise Security Telemetry and Detection
- ADR-007 — Isolate Recovery Infrastructure from Production
- ADR-008 — Separate Release Signing from Deployment Approval
- ADR-009 — Treat Verification as Distinct from Deployment Authority
- ADR-010 — Use OpenTofu for Declarative Infrastructure Modelling
- ADR-011 — Use OPA for Infrastructure Policy as Code
- ADR-012 — Evaluate Infrastructure Plans Before Deployment Authority

## Architecture Decision Domains

The ADRs cover four major architecture domains:

1. Zero Trust and identity
2. Privileged operations, telemetry and recovery
3. Software supply-chain trust
4. Infrastructure governance and Policy as Code

## Acceptance Criteria

Phase 12 is accepted when:

- ADR-001 through ADR-012 exist
- all twelve ADRs are marked Accepted
- every ADR records Context
- every ADR records a Decision
- every ADR records Security Drivers
- every ADR records Alternatives Considered
- every ADR records Consequences
- every ADR records Security Traceability
- every ADR records Implementation
- every ADR records Validation Evidence
- every ADR records Residual Risk
- every ADR records Review Triggers
- the ADR catalogue lists all accepted decisions
- the architecture decision map covers all twelve ADRs
- the primary architecture documentation references ADR governance
- Git content validation succeeds

## Validation Approach

Phase 12 does not introduce a new runtime security control.

Its assurance purpose is architecture governance.

Technical evidence referenced by the ADRs is inherited from the validated Project Redoubt phases in which those controls were implemented.

Examples include:

- Zero Trust policy tests
- network segmentation tests
- adversary simulations
- detection validation
- incident-response validation
- recovery tests
- privileged-access tests
- supply-chain adversary tests
- deployment-gate tests
- OpenTofu negative-plan testing
- OPA infrastructure policy tests
- GitHub Actions security gates

## Architecture Governance Principle

A significant architecture decision should be explainable independently of its implementation.

The required chain is:

    Security Problem
        ↓
    Architecture Decision
        ↓
    Rationale
        ↓
    Alternatives
        ↓
    Trade-offs
        ↓
    Control Implementation
        ↓
    Validation Evidence

This prevents implementation choices from becoming undocumented architecture by accident.

## Assurance Limitations

Phase 12 records Project Redoubt architecture decisions but does not represent:

- independent external architecture certification
- production deployment approval
- formal regulatory certification
- independent penetration-test assurance
- production cloud architecture validation
- complete validation of every attack path
- proof that future implementations will preserve the documented architecture

ADRs must be reviewed when material architectural assumptions change.

## Acceptance Decision

Phase 12 satisfies the Project Redoubt requirement for formal architecture decision governance.

The project now contains explicit and traceable records explaining the rationale, alternatives, consequences, implementation relationships, validation evidence and residual risks for its major security architecture decisions.

Phase 12 status: COMPLETE.
