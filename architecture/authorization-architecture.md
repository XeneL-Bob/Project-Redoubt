# ResTech — Authorisation Architecture

## 1. Purpose

This document defines how Project Redoubt determines whether an authenticated subject is permitted to perform an action.

---

## 2. Core Principle

```text
Authentication
      ↓
Who are you?

Authorisation
      ↓
What are you allowed to do?
```

These are separate security decisions.

---

## 3. Authorisation Inputs

A policy decision may consider:

```text
Identity
Role
Group
Resource
Action
Device
Authentication Strength
Time
Session Risk
Data Classification
Workload Identity
```

---

## 4. Example Policy

Request:

```text
Subject:
carol.finance

Role:
finance-approver

Resource:
Finance API

Action:
ApprovePayment

Device:
Compliant

MFA:
Satisfied
```

Decision:

```text
ALLOW
```

---

## 5. Denied Example

```text
Subject:
bob.developer

Resource:
Finance API

Action:
ApprovePayment
```

Decision:

```text
DENY
```

Even if Bob:

- authenticated successfully
- uses a corporate device
- is connected to the corporate network

---

## 6. Policy Model

Project Redoubt uses a combination of:

### RBAC

Role-Based Access Control.

Example:

```text
finance-reader
finance-approver
security-analyst
infrastructure-admin
```

### Contextual / Attribute-Based Policy

Additional context may include:

- device posture
- session risk
- authentication strength
- resource classification
- workload identity

---

## 7. Policy Enforcement

```text
Client Request
      │
      ▼
PEP
      │
      ▼
Policy Decision
      │
      ├── ALLOW
      └── DENY
```

Applications should not independently invent inconsistent access rules where a centrally governed policy model can be used.

---

## 8. Policy as Code

Policies should eventually be stored as version-controlled configuration.

Example conceptual rule:

```text
ALLOW if:

role == finance-approver
AND
resource == finance-api
AND
action == approve-payment
AND
mfa == true
AND
device.trusted == true
```

---

## 9. Negative Security Tests

Project Redoubt must test denied cases.

Examples:

```text
Developer → Finance API = DENY

Contractor → Admin Console = DENY

Employee → Database = DENY

Employee Portal Workload → Finance Secret = DENY
```

Negative tests provide stronger evidence than only testing expected successful access.
