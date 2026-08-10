# ResTech — Threat Actors

## 1. Purpose

This document identifies attacker profiles relevant to the ResTech threat model.

Threat actors are defined by capability, intent and potential access rather than by specific real-world organisations.

---

## 2. TA-001 — Opportunistic External Attacker

### Access

No legitimate ResTech access.

### Objectives

- exploit exposed services
- obtain credentials
- gain initial access
- steal information
- deploy commodity malware

### Likely Entry Points

- phishing
- public applications
- exposed APIs
- reused credentials
- vulnerable internet-facing services

### Capability

Moderate.

### Primary Risks

- R-001
- R-003
- R-004
- R-011

---

## 3. TA-002 — Targeted External Attacker

### Access

No initial legitimate access.

### Objectives

- steal intellectual property
- obtain persistent access
- compromise identity infrastructure
- access customer information
- compromise development systems

### Likely Behaviour

```text
Reconnaissance
    ↓
Initial Access
    ↓
Credential Access
    ↓
Discovery
    ↓
Privilege Escalation
    ↓
Lateral Movement
    ↓
Collection
    ↓
Exfiltration
```

### Capability

High.

### Primary Risks

- R-001
- R-002
- R-003
- R-004
- R-006
- R-007
- R-012

---

## 4. TA-003 — Ransomware Operator

### Objectives

- gain broad access
- obtain privileged credentials
- disable security controls
- compromise backup systems
- encrypt or destroy business information

### Primary Targets

- privileged identities
- endpoints
- identity systems
- databases
- backup infrastructure

### Primary Risks

- R-002
- R-003
- R-009

---

## 5. TA-004 — Malicious Insider

### Initial Access

Valid ResTech identity and legitimate internal access.

### Objectives

May include:

- data theft
- fraud
- intellectual-property theft
- sabotage
- unauthorised disclosure

### Security Concern

The insider may not need to bypass authentication.

The architecture must therefore distinguish:

```text
Authenticated
```

from:

```text
Authorised
```

### Primary Risks

- R-004
- R-005
- R-010
- R-012

---

## 6. TA-005 — Compromised Employee

This actor represents an attacker operating through a legitimate employee identity or endpoint.

### Possible Causes

- phishing
- malware
- stolen credentials
- session theft
- compromised personal device

### Primary Risks

- R-001
- R-003
- R-004

---

## 7. TA-006 — Compromised Administrator

A privileged identity has been obtained by an attacker.

### Security Significance

This is one of the highest-impact scenarios in Project Redoubt.

A privileged identity may potentially affect:

- identity
- infrastructure
- cloud services
- logging
- applications
- secrets
- backups

### Primary Risks

- R-002
- R-007
- R-008
- R-009

---

## 8. TA-007 — Compromised Contractor

### Initial Access

Valid but externally managed or temporary identity.

### Security Concerns

- excessive access
- poor lifecycle management
- unmanaged endpoint
- retained credentials
- project access extending beyond need

### Primary Risk

- R-010

---

## 9. TA-008 — Compromised Application

An attacker gains execution or control within an application workload.

### Objectives

- obtain workload credentials
- query databases
- access secrets
- call internal APIs
- pivot to additional services

### Primary Risks

- R-004
- R-007
- R-011

---

## 10. TA-009 — Software Supply-Chain Attacker

### Targets

- source repositories
- dependencies
- build systems
- CI/CD
- deployment credentials
- container artifacts

### Objective

Introduce malicious functionality into software that is subsequently treated as trusted.

### Primary Risk

- R-006

---

## 11. Threat Actor Summary

| ID | Actor | Initial Trust |
|---|---|---|
| TA-001 | Opportunistic External Attacker | None |
| TA-002 | Targeted External Attacker | None |
| TA-003 | Ransomware Operator | None |
| TA-004 | Malicious Insider | User |
| TA-005 | Compromised Employee | User |
| TA-006 | Compromised Administrator | Privileged |
| TA-007 | Compromised Contractor | Limited |
| TA-008 | Compromised Application | Workload |
| TA-009 | Supply-Chain Attacker | Development path |

The architecture must remain resilient even when the attacker begins **inside an existing trust context**.
