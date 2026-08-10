# ResTech — Zero Trust Core Architecture

## 1. Purpose

This document defines the central Zero Trust decision architecture used by Project Redoubt.

---

## 2. Logical Components

### Policy Engine — PE

The Policy Engine determines whether a requested action should be permitted.

Inputs may include:

- user identity
- workload identity
- role
- device security posture
- resource classification
- session risk
- time
- authentication method
- requested action

Output:

```text
ALLOW
DENY
STEP-UP
TERMINATE
```

---

## 3. Policy Administrator — PA

The Policy Administrator executes decisions made by the Policy Engine.

Responsibilities may include:

- issuing session-specific access information
- establishing authorised communication
- terminating sessions
- propagating access decisions to enforcement points

---

## 4. Policy Enforcement Point — PEP

The Policy Enforcement Point protects a resource and enforces policy decisions.

Potential PEP implementations later in Project Redoubt may include:

- reverse proxy
- API gateway
- service proxy
- network firewall
- application middleware
- database access gateway

---

## 5. Policy Decision Flow

```text
Subject
   │
   ▼
Authentication
   │
   ▼
Request Resource
   │
   ▼
Policy Enforcement Point
   │
   ▼
Policy Engine
   │
   ├── Identity
   ├── Device Context
   ├── Role
   ├── Risk
   └── Resource Policy
   │
   ▼
Policy Decision
   │
   ├── ALLOW
   ├── DENY
   ├── STEP-UP
   └── TERMINATE
   │
   ▼
Policy Administrator
   │
   ▼
Policy Enforcement Point
   │
   ▼
Resource
```

---

## 6. Policy Information Sources

The Policy Engine may consume information from:

- identity directory
- MFA system
- device posture
- asset inventory
- data classification
- role definitions
- threat intelligence
- security telemetry
- vulnerability information
- session-risk analytics

---

## 7. Default Behaviour

The default policy outcome is:

```text
DENY
```

Access is allowed only when policy conditions are satisfied.

---

## 8. Continuous Evaluation

A session that was previously allowed may later become unsafe.

Examples:

- device becomes non-compliant
- user privilege changes
- suspicious authentication detected
- impossible access pattern detected
- identity is disabled

The architecture should therefore support:

```text
ALLOW
  ↓
Monitor
  ↓
Re-evaluate
  ↓
Continue / Step-Up / Terminate
```

---

## 9. Attack Paths Addressed

This architecture directly interrupts:

- AP-001 Phished Employee
- AP-002 Compromised Administrator
- AP-003 Public Application to Database
- AP-007 Contractor Access Expansion
