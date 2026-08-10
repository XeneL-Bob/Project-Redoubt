# ResTech — Cybersecurity Risk Register

## 1. Purpose

This document records the primary cybersecurity risks identified during Phase 2 of Project Redoubt.

Scores represent architecture-planning estimates for the fictional ResTech environment.

Residual scores are **targets** and must not be interpreted as validated effectiveness until the relevant controls have been implemented and tested.

---

## 2. Risk Rating Reference

```text
Risk Score = Likelihood × Impact
```

| Score | Rating |
|---:|---|
| 1–4 | Low |
| 5–9 | Moderate |
| 10–16 | High |
| 17–25 | Critical |

---

## 3. Risk Summary

| ID | Risk | L | I | Inherent | Target Residual |
|---|---|---:|---:|---|---|
| R-001 | Compromised employee identity | 5 | 4 | 20 Critical | 8 Moderate |
| R-002 | Compromised privileged identity | 4 | 5 | 20 Critical | 8 Moderate |
| R-003 | Lateral movement from compromised endpoint | 4 | 5 | 20 Critical | 8 Moderate |
| R-004 | Customer data exfiltration | 4 | 5 | 20 Critical | 8 Moderate |
| R-005 | Finance-system misuse or fraud | 3 | 5 | 15 High | 6 Moderate |
| R-006 | CI/CD supply-chain compromise | 4 | 5 | 20 Critical | 8 Moderate |
| R-007 | Secrets-management compromise | 3 | 5 | 15 High | 6 Moderate |
| R-008 | Security telemetry tampering | 3 | 5 | 15 High | 6 Moderate |
| R-009 | Backup destruction during ransomware | 4 | 5 | 20 Critical | 8 Moderate |
| R-010 | Contractor over-privilege | 4 | 4 | 16 High | 6 Moderate |
| R-011 | Compromised application workload | 4 | 5 | 20 Critical | 8 Moderate |
| R-012 | Research intellectual-property theft | 3 | 5 | 15 High | 6 Moderate |

---

## 4. R-001 — Compromised Employee Identity

### Risk Statement

There is a risk that an attacker could use stolen employee credentials to access ResTech resources because user identities are a primary enterprise access mechanism, resulting in unauthorised access and potential expansion into higher-value systems.

### Affected Assets

- CJ-001 Identity Infrastructure
- CJ-003 Customer Database
- internal applications

### Threat Sources

- phishing
- credential theft
- password reuse
- token theft

### Inherent Risk

```text
Likelihood: 5
Impact:     4
Score:      20
Rating:     Critical
```

### Planned Controls

- MFA
- central authentication
- contextual authorisation
- least privilege
- session logging
- segmentation
- high-risk access controls

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

### Validation

Simulate use of a compromised standard employee identity and attempt access to unrelated sensitive applications.

---

## 5. R-002 — Compromised Privileged Identity

### Risk Statement

There is a risk that stolen or abused administrator credentials could provide broad control over ResTech systems, resulting in widespread compromise, security-control bypass or destructive action.

### Affected Assets

- CJ-001 Identity Infrastructure
- CJ-002 Privileged Credentials
- CJ-008 Secrets Management System
- CJ-009 Security Monitoring Platform
- CJ-010 Backup Infrastructure

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- separate admin identities
- MFA
- hardened administration paths
- least privilege
- privileged-access auditing
- credential rotation
- management-network isolation

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 6. R-003 — Lateral Movement from Compromised Endpoint

### Risk Statement

There is a risk that an attacker controlling an employee endpoint could discover and access unrelated enterprise systems because of excessive network reachability, resulting in expansion of the initial compromise.

### Affected Assets

- CJ-001 Identity Infrastructure
- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-009 Security Monitoring Platform

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- microsegmentation
- default-deny firewall policy
- protected management network
- endpoint telemetry
- network IDS
- workload-specific access paths

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 7. R-004 — Customer Data Exfiltration

### Risk Statement

There is a risk that an attacker or malicious insider could extract customer information from ResTech systems, resulting in privacy harm, business loss and reputational damage.

### Affected Assets

- CJ-003 Customer Database

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- strict application access
- database segmentation
- workload identities
- encryption
- detailed data-access logging
- least privilege
- exfiltration monitoring

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 8. R-005 — Finance-System Misuse or Fraud

### Risk Statement

There is a risk that compromised or malicious authorised users could manipulate finance information or transactions, resulting in financial loss or fraudulent activity.

### Affected Assets

- CJ-004 Finance Database

### Inherent Risk

```text
Likelihood: 3
Impact:     5
Score:      15
Rating:     High
```

### Planned Controls

- separation of duties
- finance-specific roles
- MFA
- transaction logging
- restricted administrative access
- anomaly detection

### Target Residual Risk

```text
Likelihood: 2
Impact:     3
Score:      6
Rating:     Moderate
```

---

## 9. R-006 — CI/CD Supply-Chain Compromise

### Risk Statement

There is a risk that an attacker could compromise source-control or CI/CD infrastructure and introduce malicious code into trusted software artifacts, resulting in production compromise.

### Affected Assets

- CJ-005 Source-Code Repository
- CJ-006 CI/CD Infrastructure

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- protected branches
- code review
- pipeline isolation
- dedicated workload identity
- secret scanning
- artifact validation
- controlled production deployment

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 10. R-007 — Secrets-Management Compromise

### Risk Statement

There is a risk that compromise of the secrets-management system could expose credentials used by multiple workloads, resulting in cascading compromise.

### Affected Assets

- CJ-008 Secrets Management System
- application and database services

### Inherent Risk

```text
Likelihood: 3
Impact:     5
Score:      15
Rating:     High
```

### Planned Controls

- strict administrative access
- workload-specific policies
- secret rotation
- audit logging
- protected recovery procedures
- high availability

### Target Residual Risk

```text
Likelihood: 2
Impact:     3
Score:      6
Rating:     Moderate
```

---

## 11. R-008 — Security Telemetry Tampering

### Risk Statement

There is a risk that an attacker with access to monitoring infrastructure could modify or suppress telemetry, reducing ResTech's ability to detect and investigate malicious activity.

### Affected Assets

- CJ-009 Security Monitoring Platform

### Inherent Risk

```text
Likelihood: 3
Impact:     5
Score:      15
Rating:     High
```

### Planned Controls

- restricted monitoring administration
- central log forwarding
- tamper-resistant storage
- security-platform auditing
- independent telemetry sources

### Target Residual Risk

```text
Likelihood: 2
Impact:     3
Score:      6
Rating:     Moderate
```

---

## 12. R-009 — Backup Destruction During Ransomware

### Risk Statement

There is a risk that an attacker gaining privileged control could delete or encrypt both production data and accessible backups, resulting in prolonged or irreversible business disruption.

### Affected Assets

- CJ-010 Backup Infrastructure
- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-001 Identity Infrastructure

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- isolated backup administration
- immutable backup copies
- encryption
- restricted deletion permissions
- offline or logically isolated recovery copies
- recovery testing

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 13. R-010 — Contractor Over-Privilege

### Risk Statement

There is a risk that contractor identities could retain excessive or unnecessary access because of weak lifecycle controls, resulting in unauthorised access to internal systems.

### Affected Assets

- internal applications
- research information
- customer information

### Inherent Risk

```text
Likelihood: 4
Impact:     4
Score:      16
Rating:     High
```

### Planned Controls

- time-limited identities
- explicit project access
- reduced default permissions
- automatic expiry
- access reviews
- enhanced contractor monitoring

### Target Residual Risk

```text
Likelihood: 2
Impact:     3
Score:      6
Rating:     Moderate
```

---

## 14. R-011 — Compromised Application Workload

### Risk Statement

There is a risk that exploitation of an internet-facing or internal application could provide access to unrelated back-end resources because of excessive workload permissions or network reachability.

### Affected Assets

- CJ-003 Customer Database
- CJ-004 Finance Database
- CJ-008 Secrets Management System

### Inherent Risk

```text
Likelihood: 4
Impact:     5
Score:      20
Rating:     Critical
```

### Planned Controls

- unique workload identities
- policy-based authorisation
- network segmentation
- least-privilege database access
- application security testing
- workload telemetry

### Target Residual Risk

```text
Likelihood: 2
Impact:     4
Score:      8
Rating:     Moderate
```

---

## 15. R-012 — Research Intellectual-Property Theft

### Risk Statement

There is a risk that compromised or malicious users could obtain proprietary research outside their authorised responsibilities, resulting in loss of commercially valuable intellectual property.

### Affected Assets

- CJ-007 Research Repository

### Inherent Risk

```text
Likelihood: 3
Impact:     5
Score:      15
Rating:     High
```

### Planned Controls

- restricted research groups
- MFA
- encryption
- data-access auditing
- controlled sharing
- anomaly detection

### Target Residual Risk

```text
Likelihood: 2
Impact:     3
Score:      6
Rating:     Moderate
```

---

## 16. Risk Register Interpretation

The highest inherent risks currently concern:

1. identity compromise
2. privileged compromise
3. lateral movement
4. customer-data exfiltration
5. software supply-chain compromise
6. backup destruction
7. application compromise

These risks will directly influence the order in which the Project Redoubt architecture is designed and implemented.
