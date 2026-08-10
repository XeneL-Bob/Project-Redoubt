# ResTech — Security Architecture Priorities

## 1. Purpose

This document converts the Phase 2 crown-jewel and risk analysis into an ordered security architecture programme.

Project Redoubt will not attempt to implement all security capabilities simultaneously.

Controls are prioritised according to their ability to reduce multiple high or critical risks.

---

## 2. Prioritisation Principles

Higher priority is assigned to controls that:

- protect multiple crown jewels
- reduce critical risks
- constrain attacker privilege
- reduce lateral movement
- establish dependencies for later controls
- increase visibility
- improve recovery capability
- can be objectively tested

---

## 3. Priority Levels

| Level | Meaning |
|---|---|
| P0 | Foundational — must exist before dependent security capabilities |
| P1 | Critical risk reduction |
| P2 | Important strengthening and resilience |
| P3 | Optimisation and maturity |

---

# 4. P0 — Security Foundations

## P0-01 — Central Identity

Establish a central identity provider for users and applications.

### Why First

Nearly every later Zero Trust control depends on reliable identity information.

### Risks Addressed

- R-001
- R-002
- R-010

---

## P0-02 — Authentication and MFA

Implement strong authentication and MFA capabilities.

### Risks Addressed

- R-001
- R-002
- R-005
- R-012

---

## P0-03 — Role and Privilege Model

Implement explicit roles and separate privileged identities.

### Risks Addressed

- R-002
- R-005
- R-010

---

## P0-04 — Network Security Zones

Establish architectural network zones before deploying production-like workloads.

Initial zones should include:

```text
Edge / DMZ
User
Application
Database
Development
Management
Security
Attack Lab
```

### Risks Addressed

- R-003
- R-004
- R-011

---

## P0-05 — Central Security Logging

Establish a logging architecture before attack simulation begins.

### Reason

Testing without telemetry would prove whether an attack succeeded but not whether ResTech could detect it.

### Risks Addressed

- R-001
- R-002
- R-003
- R-008
- R-011

---

# 5. P1 — Critical Risk Reduction

## P1-01 — Central Policy Enforcement

Introduce externalised or centralised authorisation decisions.

Potential implementation:

```text
Application Request
        ↓
Policy Enforcement Point
        ↓
Policy Decision Point
        ↓
ALLOW / DENY
```

### Risks Addressed

- R-001
- R-004
- R-005
- R-010
- R-011

---

## P1-02 — Microsegmentation

Implement default-deny connectivity between security zones.

### Required Principle

```text
Network reachability
≠
Authorisation
```

### Risks Addressed

- R-003
- R-004
- R-011

---

## P1-03 — Workload Identity

Applications and services receive unique identities.

### Risks Addressed

- R-004
- R-006
- R-007
- R-011

---

## P1-04 — Secrets Management

Move sensitive application credentials into a dedicated secrets-management system.

### Risks Addressed

- R-006
- R-007
- R-011

---

## P1-05 — Database Isolation

Prevent normal users and unrelated workloads from directly accessing protected databases.

### Target Architecture

```text
User
  ↓
Authorised Application
  ↓
Authorised Workload Identity
  ↓
Database
```

Instead of:

```text
User ───────────────> Database
```

### Risks Addressed

- R-003
- R-004
- R-005
- R-011

---

## P1-06 — Software Supply-Chain Controls

Implement controls around source code and deployment.

### Capabilities

- protected branches
- code review
- secret scanning
- CI security testing
- controlled production deployment
- dedicated pipeline identities

### Risks Addressed

- R-006

---

# 6. P2 — Detection and Resilience

## P2-01 — Endpoint Telemetry

Collect security-relevant endpoint activity.

### Risks Addressed

- R-001
- R-002
- R-003

---

## P2-02 — Network Detection

Add network-level security telemetry.

Potential capability:

- IDS
- firewall logs
- connection metadata
- unusual east-west communication detection

### Risks Addressed

- R-003
- R-011

---

## P2-03 — Identity Detection

Detect:

- repeated authentication failure
- unusual privileged access
- abnormal authentication context
- role changes
- disabled security controls

### Risks Addressed

- R-001
- R-002

---

## P2-04 — Data Access Monitoring

Monitor sensitive data access and unusual retrieval patterns.

### Risks Addressed

- R-004
- R-005
- R-012

---

## P2-05 — Protected Backup Architecture

Implement backup separation and recovery controls.

### Risks Addressed

- R-009

---

## P2-06 — Incident Response Procedures

Create playbooks for:

- compromised user
- compromised administrator
- compromised workload
- ransomware
- data exfiltration
- CI/CD compromise

---

# 7. P3 — Validation and Security Maturity

## P3-01 — Adversary Simulation

Validate the architecture using controlled attack scenarios.

Potential tools may later include:

- Atomic Red Team
- MITRE CALDERA
- custom attack simulation

---

## P3-02 — Automated Policy Testing

Test authorisation policies automatically.

Examples:

```text
Finance User
+ Approved Device
+ Finance API
= ALLOW
```

```text
Developer
+ Approved Device
+ Finance API
= DENY
```

---

## P3-03 — Resilience Testing

Validate:

- backup restoration
- credential revocation
- session termination
- endpoint isolation
- service recovery

---

## P3-04 — Architecture Decision Records

Document important architectural decisions and trade-offs.

Examples:

- identity-provider selection
- policy-engine selection
- segmentation model
- secrets-management model
- logging architecture
- recovery architecture

---

# 8. Implementation Sequence

The resulting Project Redoubt implementation order is:

```text
1. Central Identity
        ↓
2. MFA
        ↓
3. Roles & Privileged Access
        ↓
4. Security Zones
        ↓
5. Central Logging
        ↓
6. Policy Enforcement
        ↓
7. Microsegmentation
        ↓
8. Workload Identity
        ↓
9. Secrets Management
        ↓
10. Database Isolation
        ↓
11. CI/CD Security
        ↓
12. Endpoint / Network Detection
        ↓
13. Backup Resilience
        ↓
14. Incident Response
        ↓
15. Adversary Simulation
        ↓
16. Residual Risk Validation
```

---

## 9. Phase 2 Outcome

Phase 2 establishes why the future Project Redoubt architecture exists.

The architecture will therefore be derived from:

```text
Business Requirements
        ↓
Crown Jewels
        ↓
Risks
        ↓
Security Objectives
        ↓
Security Priorities
        ↓
Architecture
```

rather than:

```text
Interesting Security Tool
        ↓
Install It
        ↓
Try To Justify It Later
```

This distinction is central to the Security Architect focus of Project Redoubt.
