# ADR-001 — Adopt Zero Trust as the Enterprise Security Model

## Status

Accepted

## Context

ResTech contains users, contractors, administrators, applications, workloads, databases, development systems and security infrastructure operating across multiple trust zones.

A security model based primarily on network location would allow compromise of a trusted endpoint or internal workload to provide excessive implicit trust.

Project Redoubt therefore requires an architecture in which successful network access or authentication does not automatically establish trust.

## Decision

Project Redoubt adopts Zero Trust as the primary enterprise security architecture model.

Access decisions must be based on explicit verification, least privilege and contextual policy rather than trusted network location alone.

The architecture assumes that compromise can occur inside an established trust boundary.

## Security Drivers

The decision supports:

- explicit verification
- least privilege
- default-deny access
- containment of compromised identities and workloads
- reduction of lateral movement
- continuous security visibility

## Alternatives Considered

### Perimeter-Centric Trust

Users and systems inside an internal network would receive broad implicit trust.

Reason not selected:

- internal network location is not sufficient evidence of trust
- compromised internal endpoints could inherit excessive access
- lateral movement would become easier after initial compromise

### VPN-Based Trusted Network Extension

Remote users would become trusted after entering the corporate network through a VPN.

Reason not selected:

- network admission alone does not determine resource authorisation
- compromise of a valid remote endpoint would extend internal trust to the attacker

## Consequences

### Positive

- reduces dependence on network location as a security decision
- supports granular authorisation
- creates explicit trust boundaries
- limits blast radius after compromise
- makes access decisions observable and testable

### Negative / Trade-offs

- additional policy infrastructure is required
- identity and workload context must remain available
- enforcement failures can affect availability
- policy design becomes an architectural dependency

## Security Traceability

### Security Objectives

- SO-001 — Protect Enterprise Identity
- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-009 — Contain Compromise

### Related Attack Paths

- AP-001 — Phished Employee to Crown Jewel
- AP-003 — Public Application to Database
- AP-007 — Contractor to Internal Resource

## Implementation

Implemented through:

- Phase 4 Zero Trust architecture
- identity plane
- policy plane
- policy enforcement points
- network segmentation
- workload identity
- Phase 5 Zero Trust laboratory
- later privileged and infrastructure policy enforcement

## Validation Evidence

Project Redoubt validates the decision through:

- denied Finance access by unauthorised users
- trusted-device policy enforcement
- contractor scope restrictions
- workload segmentation
- backend bypass prevention
- adversary simulation
- policy-path detection
- infrastructure Policy as Code

## Residual Risk

Zero Trust reduces implicit trust but does not eliminate:

- stolen valid credentials
- policy-engine compromise
- enforcement-point compromise
- trusted-device compromise
- malicious administrators
- implementation defects

These risks require independent identity, management, telemetry and recovery controls.

## Review Triggers

Reconsider this ADR if:

- the enterprise security model changes materially
- central identity and policy capabilities cannot meet availability requirements
- major workloads cannot participate in explicit identity or policy enforcement
