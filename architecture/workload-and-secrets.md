# ResTech — Workload Identity and Secrets Architecture

## 1. Purpose

Applications and services must have identities independent from human users and host network location.

---

## 2. Workload Identity

Examples:

```text
svc.employee-portal
svc.finance-api
svc.admin-api
svc.logging-agent
svc.backup-service
svc.cicd-runner
```

Each workload identity receives only required permissions.

---

## 3. Example

```text
svc.finance-api
```

Allowed:

```text
Read / write required Finance database objects
Retrieve Finance API secret
Send telemetry
```

Denied:

```text
HR Database
Security Administration
Identity Administration
Research Database
Backup Administration
```

---

## 4. Workload Authentication

Preferred model:

```text
Workload
   │
   ▼
Workload Identity
   │
   ▼
Authenticate
   │
   ▼
Policy
   │
   ▼
Resource
```

Not:

```text
IP Address
   =
Trusted Application
```

---

## 5. Secrets Architecture

Sensitive material includes:

- API tokens
- database credentials
- certificates
- signing keys
- encryption keys
- service credentials

Secrets must not be stored directly in source code.

---

## 6. Secret Retrieval

```text
Application
    │
    ▼
Workload Identity
    │
    ▼
Secrets Policy
    │
    ▼
Secrets Manager
    │
    ▼
Specific Secret
```

---

## 7. Secret Isolation

Example:

```text
svc.employee-portal
```

may retrieve:

```text
employee-portal/database
```

but must be denied:

```text
finance/database
identity/admin
backup/admin
security/signing-key
```

---

## 8. Rotation

Secrets should support rotation without requiring source-code modification.

---

## 9. Audit Events

Log:

- secret requested
- requesting workload
- secret path
- successful retrieval
- denied retrieval
- secret modification
- rotation
- administrative changes

Secret values themselves must not be placed into logs.

---

## 10. Related Risks

- R-006 CI/CD Compromise
- R-007 Secrets Management Compromise
- R-011 Compromised Application Workload
