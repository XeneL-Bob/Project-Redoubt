# ResTech — Security Objectives

## 1. Purpose

This document translates the ResTech business requirements, asset inventory and crown-jewel analysis into measurable security architecture objectives.

These objectives describe what Project Redoubt must achieve before individual technologies are selected.

---

## 2. Objective Model

Project Redoubt follows:

```text
Business Requirement
        ↓
Security Requirement
        ↓
Security Objective
        ↓
Architecture Decision
        ↓
Technical Control
        ↓
Validation Evidence
```

This prevents technology selection from driving security requirements.

---

## 3. SO-001 — Protect Enterprise Identity

ResTech must prevent a single compromised user identity from automatically providing access to unrelated sensitive resources.

### Supports

- SR-001 Strong Authentication
- SR-002 Least Privilege
- SR-003 No Implicit Network Trust
- SR-004 Central Identity

### Protects

- CJ-001 Identity Infrastructure
- CJ-002 Privileged Credentials

### Success Criteria

- central authentication is enforced for protected applications
- MFA can be required for sensitive access
- access is explicitly authorised
- identity events are centrally logged

---

## 4. SO-002 — Protect Privileged Access

Privileged access must be separated from normal user activity and receive stronger controls.

### Supports

- SR-002 Least Privilege
- SR-006 Privileged Access Separation
- SR-022 Administrative Audit

### Protects

- CJ-001 Identity Infrastructure
- CJ-002 Privileged Credentials
- CJ-008 Secrets Management System

### Success Criteria

- administrative identities are separate
- privileged sessions are auditable
- privileged access requires stronger authentication
- unnecessary standing administrative access is removed

---

## 5. SO-003 — Limit Lateral Movement

Compromise of one endpoint, workload or account must not automatically provide unrestricted access to other enterprise resources.

### Supports

- SR-003 No Implicit Network Trust
- SR-007 Segmentation
- SR-013 Lateral Movement Protection
- SR-024 Attack Containment

### Success Criteria

- security zones are defined
- unnecessary east-west communication is blocked
- database access is restricted
- sensitive management interfaces are isolated

---

## 6. SO-004 — Protect Sensitive Data

Sensitive ResTech information must only be accessible to explicitly authorised identities and workloads.

### Supports

- SR-002 Least Privilege
- SR-017 Data Classification
- SR-018 Encryption

### Protects

- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-007 Research Repository

### Success Criteria

- data classification influences access controls
- restricted information receives enhanced controls
- sensitive access is auditable
- direct unauthorised database access is prevented

---

## 7. SO-005 — Protect Application and Workload Identity

Applications must not depend on shared static credentials or network location as their primary trust mechanism.

### Supports

- SR-003 No Implicit Network Trust
- SR-009 Workload Authentication
- SR-010 Secrets Protection

### Protects

- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-006 CI/CD Infrastructure
- CJ-008 Secrets Management System

### Success Criteria

- important workloads receive unique identities
- workload permissions are least privilege
- application secrets are not committed to source control
- workload access is auditable

---

## 8. SO-006 — Protect the Software Supply Chain

Software development and deployment processes must resist unauthorised code or artifact modification.

### Supports

- SR-002 Least Privilege
- SR-010 Secrets Protection
- SR-023 Security Testing
- SR-025 Policy as Code

### Protects

- CJ-005 Source-Code Repository
- CJ-006 CI/CD Infrastructure

### Success Criteria

- protected development workflows exist
- source changes are attributable
- secrets are scanned
- deployment permissions are separated
- production changes are auditable

---

## 9. SO-007 — Centralise Security Visibility

Security-relevant events must be centrally observable.

### Supports

- SR-011 Security Logging
- SR-012 Access Logging
- SR-021 Security Monitoring
- SR-022 Administrative Audit

### Protects

- CJ-009 Security Monitoring Platform

### Success Criteria

Telemetry is collected from:

- identity systems
- endpoints
- applications
- policy engines
- network controls
- privileged systems

---

## 10. SO-008 — Detect High-Risk Behaviour

Project Redoubt must detect meaningful attack behaviours rather than merely collect logs.

### Supports

- SR-013 Lateral Movement Protection
- SR-016 High-Risk Sessions
- SR-021 Security Monitoring

### Success Criteria

Detections exist for scenarios including:

- repeated authentication failure
- privileged account misuse
- unauthorised application access
- unusual network movement
- attempted direct database access
- suspicious security-control modification

---

## 11. SO-009 — Contain Compromise

Project Redoubt must reduce the blast radius of successful initial compromise.

### Supports

- SR-007 Segmentation
- SR-014 Default Deny
- SR-024 Attack Containment

### Success Criteria

A compromised:

```text
Employee Account
```

must not automatically compromise:

```text
Finance
Identity
Security
Database
Infrastructure
```

Likewise, a compromised application must not automatically gain access to unrelated services.

---

## 12. SO-010 — Maintain Recoverability

Critical ResTech services must be recoverable following destructive attack or major failure.

### Supports

- BR-008 Business Continuity
- SR-020 Recovery

### Protects

- CJ-001 Identity Infrastructure
- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-010 Backup Infrastructure

### Success Criteria

- critical information is backed up
- recovery priorities are defined
- backup administration is separated where practical
- recovery procedures are tested

---

## 13. SO-011 — Make Security Policy Testable

Important access-control logic should be represented in a form that can be reviewed, version controlled and automatically tested.

### Supports

- SR-005 Central Authorisation
- SR-014 Default Deny
- SR-025 Policy as Code

### Success Criteria

- policies are version controlled
- expected allow/deny behaviour has tests
- unauthorised changes are reviewable
- policy behaviour can be validated in CI

---

## 14. SO-012 — Produce Evidence of Security Effectiveness

Project Redoubt must demonstrate that controls actually influence attacker behaviour.

### Supports

- SR-023 Security Testing
- SR-024 Attack Containment

### Success Criteria

For selected attack scenarios, Project Redoubt records:

- attack action
- expected control
- actual control behaviour
- security telemetry
- detection result
- containment result
- remaining exposure
- architecture improvement

---

## 15. Security Objective Summary

| ID | Objective | Primary Security Theme |
|---|---|---|
| SO-001 | Protect Enterprise Identity | Identity |
| SO-002 | Protect Privileged Access | Privilege |
| SO-003 | Limit Lateral Movement | Network |
| SO-004 | Protect Sensitive Data | Data |
| SO-005 | Protect Workload Identity | Application |
| SO-006 | Protect Software Supply Chain | DevSecOps |
| SO-007 | Centralise Security Visibility | Monitoring |
| SO-008 | Detect High-Risk Behaviour | Detection |
| SO-009 | Contain Compromise | Resilience |
| SO-010 | Maintain Recoverability | Recovery |
| SO-011 | Make Security Policy Testable | Governance |
| SO-012 | Produce Security Evidence | Validation |
