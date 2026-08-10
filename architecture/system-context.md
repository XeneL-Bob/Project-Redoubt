# ResTech — Enterprise System Context

## 1. Purpose

This document defines the high-level system context for the Project Redoubt security architecture.

---

## 2. External Actors

ResTech interacts with:

- employees
- administrators
- developers
- researchers
- finance users
- security analysts
- executives
- contractors
- customers
- external identity providers where applicable
- software and package repositories
- cloud platforms

---

## 3. Core Enterprise Systems

### Identity

- Central Identity Provider
- MFA service
- privileged identity functions
- service identity infrastructure

### Applications

- Employee Portal
- Customer Portal
- Finance Application
- Research Platform
- Admin Console
- internal APIs

### Development

- source-code repository
- CI/CD
- build agents
- container registry
- test environment

### Data

- Customer Database
- Finance Database
- HR Database
- Research Database
- Security Events Database

### Security

- SIEM
- endpoint telemetry
- network detection
- vulnerability scanning
- policy engine
- secrets management

### Recovery

- protected backup infrastructure
- configuration backup
- identity recovery data

---

## 4. Enterprise Context

```text
                         INTERNET
                            │
                            ▼
                    ┌───────────────┐
                    │ EDGE / DMZ    │
                    │ WAF / Proxy   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ APPLICATIONS  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ DATABASES     │
                    └───────────────┘


 Employees / Contractors
          │
          ▼
   Identity Provider
          │
          ▼
     Policy Plane
          │
          ▼
 Enforcement Points
          │
          ▼
 Approved Resources
```

---

## 5. Security Context

Security controls must consider:

```text
Subject Identity
      +
Authentication Strength
      +
Device Context
      +
Requested Resource
      +
Requested Action
      +
Role
      +
Session Risk
      +
Resource Sensitivity
```

---

## 6. Architecture Assumption

No network zone is inherently trusted.

Segmentation limits reachability, but authorisation determines whether an identity or workload should access a resource.

Therefore:

```text
Network Reachability
≠
Permission
```
