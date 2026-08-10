# ResTech — Asset Inventory

## 1. Purpose

This document identifies the major logical, technical and informational assets requiring protection within the ResTech environment.

---

## 2. Asset Categories

```text
Identity
Endpoints
Applications
Infrastructure
Databases
Security Systems
Development Systems
Networks
Cloud Resources
Information Assets
Secrets and Cryptographic Assets
Backup Systems
```

---

## 3. Identity Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| IAM-001 | Central Identity Provider | Critical |
| IAM-002 | MFA Services | Critical |
| IAM-003 | Authorisation Policy Engine | Critical |
| IAM-004 | Privileged Accounts | Critical |
| IAM-005 | Service Identities | High |

---

## 4. Endpoint Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| END-001 | Employee laptops | Medium |
| END-002 | Developer workstations | High |
| END-003 | Administrator workstations | Critical |
| END-004 | Executive laptops | High |
| END-005 | Contractor devices | Medium |
| END-006 | Security analyst workstations | High |

---

## 5. Application Assets

| Asset ID | Asset | Purpose | Criticality |
|---|---|---|---|
| APP-001 | Employee Portal | Employee services | Medium |
| APP-002 | Finance Application | Financial operations | Critical |
| APP-003 | Admin Console | Administration | Critical |
| APP-004 | Customer Portal | Customer services | Critical |
| APP-005 | Research Platform | Research workloads | High |
| APP-006 | Internal API Gateway | Application communication | Critical |

---

## 6. Database Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| DB-001 | Customer Database | Critical |
| DB-002 | Finance Database | Critical |
| DB-003 | HR Database | Critical |
| DB-004 | Research Database | High |
| DB-005 | Application Database | High |
| DB-006 | Security Events Database | High |

---

## 7. Development Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| DEV-001 | Source-code repository | Critical |
| DEV-002 | CI/CD platform | Critical |
| DEV-003 | Development environment | High |
| DEV-004 | Test environment | Medium |
| DEV-005 | Container registry | High |
| DEV-006 | Build agents | High |

---

## 8. Security Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| SEC-001 | SIEM | Critical |
| SEC-002 | Endpoint monitoring platform | High |
| SEC-003 | Network IDS | High |
| SEC-004 | Vulnerability scanner | High |
| SEC-005 | Security dashboards | Medium |
| SEC-006 | Security log storage | Critical |
| SEC-007 | Incident-response platform | High |

---

## 9. Network Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| NET-001 | Edge firewall | Critical |
| NET-002 | Reverse proxy | Critical |
| NET-003 | Corporate network | High |
| NET-004 | Application network | High |
| NET-005 | Database network | Critical |
| NET-006 | Management network | Critical |
| NET-007 | Security network | Critical |
| NET-008 | Development network | High |
| NET-009 | Guest network | Low |
| NET-010 | Attack simulation network | High |

---

## 10. Secrets and Cryptographic Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| CRY-001 | TLS private keys | Critical |
| CRY-002 | API secrets | Critical |
| CRY-003 | Database credentials | Critical |
| CRY-004 | Service credentials | Critical |
| CRY-005 | Signing keys | Critical |
| CRY-006 | Backup encryption keys | Critical |

---

## 11. Backup Assets

| Asset ID | Asset | Criticality |
|---|---|---|
| BAK-001 | Database backups | Critical |
| BAK-002 | Application configuration backups | High |
| BAK-003 | Identity configuration backups | Critical |
| BAK-004 | Infrastructure configuration backups | Critical |
| BAK-005 | Security configuration backups | High |

---

## 12. Information Assets

```text
Customer information
Employee information
Payroll information
Financial information
Research information
Source code
Intellectual property
Authentication information
Security telemetry
Infrastructure configuration
API credentials
Encryption keys
```

---

## 13. Crown Jewels

### CJ-001 — Identity Infrastructure

Compromise could allow attackers to impersonate users, workloads and administrators.

### CJ-002 — Privileged Credentials

Compromise could provide broad administrative control over enterprise systems.

### CJ-003 — Customer Database

Contains sensitive customer information.

### CJ-004 — Finance Database

Contains financial and payroll information.

### CJ-005 — Source-Code Repository

Contains proprietary ResTech software and intellectual property.

### CJ-006 — CI/CD Infrastructure

Compromise could allow malicious modifications to applications or production deployments.

### CJ-007 — Research Repository

Contains commercially valuable research and intellectual property.

### CJ-008 — Secrets Management System

Contains credentials and cryptographic secrets used by enterprise applications.

### CJ-009 — Security Monitoring Platform

Compromise could reduce ResTech's ability to detect, investigate and respond to attacks.

### CJ-010 — Backup Infrastructure

Compromise could prevent effective recovery following destructive attacks.

---

## 14. Asset Management Principles

- Critical assets must have identifiable owners.
- Assets must receive appropriate security classifications.
- Critical systems must produce security telemetry.
- Administrative access must be restricted.
- Unsupported assets must be removed or remediated.
- Asset dependencies must be documented.
- Internet-facing assets must be specifically identified.
- Crown-jewel assets must receive enhanced security controls.
