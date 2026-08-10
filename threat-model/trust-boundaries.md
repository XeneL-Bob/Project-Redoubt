# ResTech — Trust Boundaries

## 1. Purpose

A trust boundary exists where identity, privilege, ownership, security posture or data sensitivity changes.

Project Redoubt does not treat network location alone as evidence of trust.

---

## 2. TB-001 — Internet to ResTech

```text
Internet
   │
   │ TB-001
   ▼
Edge / DMZ
```

Anything crossing this boundary is considered untrusted until authenticated, authorised and validated.

---

## 3. TB-002 — User Device to Enterprise Service

```text
User
  │
Device
  │
  │ TB-002
  ▼
Enterprise Application
```

Evaluation should include:

- identity
- authentication strength
- authorisation
- device context
- requested resource
- requested action

---

## 4. TB-003 — Standard User to Privileged Administration

```text
Normal User Context
        │
        │ TB-003
        ▼
Privileged Context
```

Crossing this boundary must require explicit privileged authorisation.

Normal productivity identity must not automatically become administrative identity.

---

## 5. TB-004 — Application to Database

```text
Application
     │
     │ TB-004
     ▼
Database
```

Required concepts:

- workload authentication
- least privilege
- explicit database permissions
- encrypted transport
- access logging

---

## 6. TB-005 — Workload to Secrets

```text
Application Workload
        │
        │ TB-005
        ▼
Secrets Management
```

A workload must only retrieve secrets required for its function.

---

## 7. TB-006 — Development to Production

```text
Developer
   │
Source
   │
CI/CD
   │
   │ TB-006
   ▼
Production
```

Developer access must not imply direct production administrative access.

The deployment process itself is a security boundary.

---

## 8. TB-007 — Corporate Network to Management Network

```text
Corporate User Zone
        │
        │ TB-007
        ▼
Management Zone
```

Management interfaces should not be broadly reachable from standard endpoints.

---

## 9. TB-008 — Production to Security Monitoring

```text
Production Systems
        │
        │ telemetry
        ▼
Security Monitoring
```

Production systems may send telemetry, but must not automatically receive administrative control over the monitoring platform.

---

## 10. TB-009 — Production to Backup Infrastructure

```text
Production
    │
    │ TB-009
    ▼
Backup Environment
```

The boundary should prevent compromise of production administration from automatically providing destructive control over all recovery copies.

---

## 11. TB-010 — Contractor to ResTech

```text
External Contractor
        │
        │ TB-010
        ▼
Approved ResTech Resource
```

Contractor trust must be:

- explicit
- limited
- monitored
- project-specific
- time-bounded

---

## 12. Boundary Principle

Every significant boundary should eventually have:

```text
Identity Verification
        +
Authorisation
        +
Network Control
        +
Telemetry
        +
Failure Behaviour
```

The preferred failure behaviour is **deny**.
