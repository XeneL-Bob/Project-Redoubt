# ResTech — Identity Architecture

## 1. Purpose

Identity is the primary control plane for establishing who or what is requesting access.

Project Redoubt distinguishes:

```text
Human Identity
Workload Identity
Privileged Identity
Device Identity
```

---

## 2. Identity Types

### Standard User

Examples:

```text
alice.employee
bob.developer
carol.finance
```

### Privileged User

Examples:

```text
admin.infrastructure
admin.security
```

### Contractor

Example:

```text
erin.contractor
```

### Workload

Examples:

```text
svc.employee-portal
svc.finance-api
svc.admin-api
svc.cicd-runner
```

---

## 3. Authentication Architecture

```text
User
 │
 ▼
Identity Provider
 │
 ├── Password / Primary Credential
 │
 ├── MFA
 │
 └── Authentication Policy
 │
 ▼
Authenticated Identity
 │
 ▼
Policy Decision
```

Authentication proves identity.

It does not automatically provide resource access.

---

## 4. Privileged Identity Separation

Normal accounts must not be used for privileged administration.

Example:

```text
grace.it
```

for:

```text
Email
Documentation
Normal Corporate Services
```

and:

```text
admin.infrastructure
```

for:

```text
Infrastructure Administration
```

---

## 5. Privileged Access Principle

```text
Standard Identity
       │
       X
       │
       ▼
Administrative Resource
```

Instead:

```text
Dedicated Admin Identity
       +
Strong Authentication
       +
Approved Management Path
       +
Explicit Role
       ↓
Administrative Resource
```

---

## 6. Contractor Identity

Contractor identities must contain:

- explicit owner
- project scope
- start date
- expiry date
- authorised applications
- restricted privileges

Default contractor behaviour:

```text
No project assignment
        =
No access
```

---

## 7. Identity Lifecycle

```text
Create
  ↓
Verify
  ↓
Assign Role
  ↓
Grant Minimum Access
  ↓
Monitor
  ↓
Review
  ↓
Modify / Revoke
  ↓
Disable
```

---

## 8. Identity Telemetry

Important events include:

- successful login
- failed login
- MFA result
- role assignment
- privilege change
- password reset
- identity creation
- identity disablement
- session revocation
- unusual authentication

---

## 9. Related Risks

- R-001 Compromised Employee Identity
- R-002 Compromised Privileged Identity
- R-010 Contractor Over-Privilege
