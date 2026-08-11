# ADR-003 — Separate Authentication from Authorisation

## Status

Accepted

## Context

Successful authentication proves that an identity has satisfied an authentication process.

It does not prove that the identity should be permitted to perform every action or access every resource.

Treating authentication as sufficient authorisation would allow any compromised valid account to inherit excessive enterprise access.

## Decision

Project Redoubt treats authentication and authorisation as separate security decisions.

Authentication establishes identity.

Authorisation evaluates whether that identity, operating within the supplied context, may perform the requested action against the requested resource.

The architecture therefore follows:

    Identity Authentication
            ↓
    Authenticated Identity
            ↓
    Context + Resource + Action
            ↓
    Authorisation Policy
            ↓
       ALLOW / DENY

An authenticated identity can still receive a DENY decision.

## Security Drivers

The decision supports:

- least privilege
- role and scope restrictions
- contextual access control
- trusted-device requirements
- privileged-access separation
- contractor restrictions
- resource-specific policy

## Alternatives Considered

### Authentication Grants General Access

A successfully authenticated identity receives broad access.

Reason not selected:

- compromised accounts would receive excessive privilege
- resource sensitivity would not influence decisions
- contextual security conditions could not be enforced

### Network Membership Determines Authorisation

Access is determined primarily by whether the user or workload is inside a trusted network.

Reason not selected:

- network location does not prove business authorisation
- compromised internal systems could abuse inherited trust

## Consequences

### Positive

- valid credentials do not automatically provide crown-jewel access
- access can be restricted by role, resource, device and context
- privileged operations can require additional authority
- denied access remains observable even for valid users

### Negative / Trade-offs

- authorisation policy must be maintained separately
- additional request context is required
- policy mistakes may incorrectly allow or deny access

## Security Traceability

### Security Objectives

- SO-001 — Protect Enterprise Identity
- SO-002 — Protect Privileged Access
- SO-004 — Protect Sensitive Data
- SO-009 — Contain Compromise

### Related Attack Paths

- AP-001 — Phished Employee to Crown Jewel
- AP-002 — Compromised Administrator
- AP-007 — Contractor to Internal Resource

## Implementation

Implemented through:

- Keycloak authentication
- OIDC access tokens
- OPA authorisation
- Finance policy controls
- trusted-device context
- role and scope evaluation
- management-plane JIT elevation
- dedicated administrative policy

## Validation Evidence

Validated through:

- authenticated employee denied Finance access
- Finance identity denied from an untrusted device
- contractor scope escape denied
- normal identities denied privileged elevation
- incorrect administrative roles denied
- expired elevation grants denied

## Residual Risk

The decision depends on:

- integrity of identity claims
- correct authorisation policy
- correct context propagation
- trusted enforcement points

Authentication or authorisation infrastructure compromise can still undermine the security model.

## Review Triggers

Reconsider this ADR if:

- identity architecture changes substantially
- applications require disconnected authorisation
- new trust models replace current identity claims
