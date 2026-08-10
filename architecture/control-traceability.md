# ResTech — Architecture Control Traceability

## 1. Purpose

This document connects risks and attack paths to architectural controls.

This prevents controls from being introduced without a documented reason.

---

## 2. Traceability Matrix

| Control | Risks | Attack Paths | Architecture Domain |
|---|---|---|---|
| MFA | R-001, R-002 | AP-001, AP-002 | Identity |
| Privileged identity separation | R-002 | AP-002, AP-005 | Identity / Management |
| Central policy engine | R-001, R-004, R-010, R-011 | AP-001, AP-003, AP-007 | Authorisation |
| Policy enforcement points | R-001, R-003, R-011 | AP-001, AP-003 | Zero Trust |
| Network segmentation | R-003, R-004, R-011 | AP-001, AP-003, AP-005 | Network |
| Database isolation | R-003, R-004, R-005 | AP-003 | Data |
| Workload identity | R-004, R-007, R-011 | AP-003 | Workload |
| Secrets manager | R-006, R-007, R-011 | AP-003, AP-004 | Secrets |
| Protected CI/CD | R-006 | AP-004 | Development |
| Central telemetry | R-001, R-002, R-003, R-008 | Multiple | Security |
| Tamper-resistant logs | R-008 | AP-008 | Security |
| Isolated backups | R-009 | AP-005 | Recovery |
| Contractor expiry | R-010 | AP-007 | Identity |

---

## 3. Security Objective Mapping

### SO-001 Protect Enterprise Identity

Architecture:

- Identity Plane
- MFA
- Policy Plane

### SO-002 Protect Privileged Access

Architecture:

- dedicated admin identities
- management network
- administrative separation

### SO-003 Limit Lateral Movement

Architecture:

- security zones
- default deny
- PEPs
- workload isolation

### SO-004 Protect Sensitive Data

Architecture:

- database isolation
- workload identity
- explicit authorisation

### SO-005 Protect Workload Identity

Architecture:

- service identities
- secrets policy
- workload authentication

### SO-006 Protect Software Supply Chain

Architecture:

- CI/CD trust boundary
- pipeline identities
- deployment controls

### SO-007 Centralise Security Visibility

Architecture:

- telemetry plane
- central event collection

### SO-008 Detect High-Risk Behaviour

Architecture:

- SIEM
- correlation
- detection rules

### SO-009 Contain Compromise

Architecture:

- segmentation
- policy enforcement
- least privilege

### SO-010 Maintain Recoverability

Architecture:

- protected backup plane
- recovery procedures

### SO-011 Make Policy Testable

Architecture:

- policy as code
- version control
- automated negative tests

### SO-012 Produce Security Evidence

Architecture:

- attack lab
- telemetry
- test results
- evidence repository

---

## 4. Architecture Chain

```text
Business Requirement
        ↓
Security Requirement
        ↓
Crown Jewel
        ↓
Risk
        ↓
Threat / Attack Path
        ↓
Security Objective
        ↓
Architecture Control
        ↓
Implementation
        ↓
Test
        ↓
Evidence
```

This traceability chain is a core Project Redoubt deliverable.
