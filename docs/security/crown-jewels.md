# ResTech — Crown Jewel Analysis

## 1. Purpose

This document identifies and prioritises the information systems, identities, services and data whose compromise would cause the greatest harm to ResTech.

The crown-jewel analysis provides the security architecture with a business-driven basis for prioritising controls.

The objective is not to protect every asset equally.

Instead, Project Redoubt prioritises security according to:

- business impact
- confidentiality requirements
- integrity requirements
- availability requirements
- privilege concentration
- dependency relationships
- threat exposure
- recovery importance

---

## 2. Assessment Scale

Each crown jewel receives a Confidentiality, Integrity and Availability rating.

| Score | Rating | Description |
|---:|---|---|
| 1 | Very Low | Minimal organisational impact |
| 2 | Low | Limited operational impact |
| 3 | Moderate | Material but manageable impact |
| 4 | High | Major business or security impact |
| 5 | Critical | Severe enterprise-wide impact |

The CIA values do not represent mathematical risk by themselves.

They indicate which security properties are most important for each asset and support later risk analysis.

---

## 3. Crown Jewel Summary

| ID | Crown Jewel | C | I | A | Overall Criticality |
|---|---|---:|---:|---:|---|
| CJ-001 | Identity Infrastructure | 5 | 5 | 5 | Critical |
| CJ-002 | Privileged Credentials | 5 | 5 | 4 | Critical |
| CJ-003 | Customer Database | 5 | 5 | 4 | Critical |
| CJ-004 | Finance Database | 5 | 5 | 4 | Critical |
| CJ-005 | Source-Code Repository | 4 | 5 | 4 | Critical |
| CJ-006 | CI/CD Infrastructure | 4 | 5 | 4 | Critical |
| CJ-007 | Research Repository | 5 | 5 | 3 | Critical |
| CJ-008 | Secrets Management System | 5 | 5 | 5 | Critical |
| CJ-009 | Security Monitoring Platform | 4 | 5 | 4 | Critical |
| CJ-010 | Backup Infrastructure | 4 | 5 | 5 | Critical |

---

## 4. CJ-001 — Identity Infrastructure

### Business Function

Provides authentication and identity services for ResTech users, administrators, applications and services.

### Security Importance

Identity infrastructure represents a central trust dependency across the enterprise.

Compromise may allow an attacker to:

- impersonate legitimate users
- impersonate administrators
- create unauthorised identities
- modify authentication policies
- disable authentication controls
- manipulate group membership
- obtain access to multiple downstream services

### CIA Assessment

**Confidentiality: 5 — Critical**

Authentication information and identity attributes require strong protection.

**Integrity: 5 — Critical**

Unauthorised modification could allow attackers to create identities or grant privileges.

**Availability: 5 — Critical**

Identity outages could prevent access to a large proportion of ResTech services.

### Key Dependencies

- MFA services
- application authentication
- privileged access
- workload authentication
- policy enforcement
- logging and monitoring

### Primary Security Concerns

- credential theft
- account takeover
- privilege escalation
- identity-provider compromise
- authentication bypass
- malicious administrative changes
- session or token theft

### Required Architectural Direction

Identity infrastructure must receive:

- strong administrative separation
- MFA
- least privilege
- detailed audit logging
- hardened administration paths
- resilient deployment
- secure recovery mechanisms
- centralised monitoring

---

## 5. CJ-002 — Privileged Credentials

### Business Function

Privileged identities provide administrative access to infrastructure, security systems, cloud services and critical applications.

### Security Importance

Compromise of privileged credentials can convert a limited compromise into an enterprise-wide incident.

### CIA Assessment

**Confidentiality: 5 — Critical**

Privileged credentials must not be exposed.

**Integrity: 5 — Critical**

Credential or privilege manipulation could provide unauthorised administrative control.

**Availability: 4 — High**

Loss of privileged access could significantly impair administration and incident response.

### Primary Security Concerns

- credential dumping
- password reuse
- session theft
- phishing
- privilege escalation
- misuse by authorised administrators
- excessive standing privilege

### Required Architectural Direction

Project Redoubt should implement:

- separate administrative identities
- MFA
- privileged access restrictions
- short-lived privilege where practical
- privileged-session logging
- credential rotation
- hardened administrator workstations

---

## 6. CJ-003 — Customer Database

### Business Function

Stores customer information used by ResTech customer-facing services.

### CIA Assessment

**Confidentiality: 5 — Critical**

Unauthorised disclosure may expose sensitive customer information.

**Integrity: 5 — Critical**

Unauthorised modification may damage customer records and business processes.

**Availability: 4 — High**

Extended outages may disrupt customer-facing operations.

### Primary Security Concerns

- unauthorised database access
- application compromise
- SQL injection
- credential theft
- data exfiltration
- malicious modification
- destructive attack

### Required Architectural Direction

The customer database should:

- reject direct normal-user access
- accept traffic only from authorised workloads
- encrypt sensitive data
- maintain detailed auditing
- use dedicated service identities
- use protected credentials
- maintain recoverable backups

---

## 7. CJ-004 — Finance Database

### Business Function

Stores financial, invoicing, payroll and related information.

### CIA Assessment

**Confidentiality: 5 — Critical**

Contains highly sensitive financial and payroll information.

**Integrity: 5 — Critical**

Manipulation could result in fraud or incorrect financial processing.

**Availability: 4 — High**

Extended unavailability could interrupt financial operations.

### Primary Security Concerns

- financial fraud
- insider abuse
- compromised finance accounts
- privileged misuse
- data exfiltration
- unauthorised modification

### Required Architectural Direction

Finance data requires:

- strict role-based access
- separation of duties
- enhanced auditing
- MFA for sensitive access
- segmentation
- application-mediated database access
- data-exfiltration monitoring

---

## 8. CJ-005 — Source-Code Repository

### Business Function

Stores ResTech proprietary application source code and development history.

### CIA Assessment

**Confidentiality: 4 — High**

Source code represents intellectual property and may expose implementation details.

**Integrity: 5 — Critical**

Malicious modification may introduce vulnerabilities or backdoors.

**Availability: 4 — High**

Developers depend on repository availability for normal engineering activities.

### Primary Security Concerns

- stolen developer credentials
- malicious commits
- repository token compromise
- source-code theft
- secret exposure
- branch-protection bypass

### Required Architectural Direction

Controls should include:

- strong developer authentication
- protected branches
- code review
- secret scanning
- signed or attributable changes
- least-privilege repository access
- CI security controls

---

## 9. CJ-006 — CI/CD Infrastructure

### Business Function

Builds, tests and deploys ResTech applications.

### CIA Assessment

**Confidentiality: 4 — High**

CI/CD systems may access source code, deployment secrets and infrastructure information.

**Integrity: 5 — Critical**

Compromise could allow malicious code to enter production.

**Availability: 4 — High**

Outages could prevent software deployment and recovery operations.

### Primary Security Concerns

- pipeline compromise
- poisoned build artifacts
- malicious dependencies
- stolen deployment credentials
- build-agent compromise
- unauthorised production deployment

### Required Architectural Direction

CI/CD security should include:

- dedicated workload identities
- isolated build agents
- protected secrets
- controlled deployment permissions
- artifact integrity validation
- pipeline audit logging
- approval controls for production

---

## 10. CJ-007 — Research Repository

### Business Function

Stores proprietary ResTech research and intellectual property.

### CIA Assessment

**Confidentiality: 5 — Critical**

Research may represent substantial commercial value.

**Integrity: 5 — Critical**

Unauthorised modification could invalidate research findings.

**Availability: 3 — Moderate**

Temporary unavailability would disrupt research operations but may not immediately halt the enterprise.

### Primary Security Concerns

- intellectual-property theft
- insider threat
- compromised researcher identity
- unauthorised sharing
- destructive modification

### Required Architectural Direction

Controls should include:

- restrictive access groups
- strong authentication
- data access logging
- encryption
- controlled external sharing
- backup and version history

---

## 11. CJ-008 — Secrets Management System

### Business Function

Stores credentials, API secrets, cryptographic material and application secrets.

### CIA Assessment

**Confidentiality: 5 — Critical**

Exposure could compromise many dependent systems.

**Integrity: 5 — Critical**

Secret modification could redirect, impersonate or disrupt trusted services.

**Availability: 5 — Critical**

Applications depending on dynamic secret retrieval may fail if the service becomes unavailable.

### Primary Security Concerns

- administrator compromise
- secret extraction
- excessive service permissions
- unauthorised secret modification
- service-token compromise

### Required Architectural Direction

The system should implement:

- strict authentication
- detailed access policies
- workload-specific access
- audit logging
- credential rotation
- high availability
- protected recovery procedures

---

## 12. CJ-009 — Security Monitoring Platform

### Business Function

Collects and analyses enterprise security telemetry.

### CIA Assessment

**Confidentiality: 4 — High**

Security logs may expose infrastructure, identities and incident information.

**Integrity: 5 — Critical**

Attackers modifying telemetry could hide malicious activity.

**Availability: 4 — High**

Loss of visibility would materially weaken detection and response capability.

### Primary Security Concerns

- log deletion
- alert suppression
- monitoring administrator compromise
- telemetry manipulation
- denial of service

### Required Architectural Direction

Controls should include:

- restricted administrative access
- centralised logging
- tamper-resistant storage
- monitoring of security-platform changes
- independent telemetry sources
- resilient log collection

---

## 13. CJ-010 — Backup Infrastructure

### Business Function

Provides recoverable copies of critical ResTech information and system configuration.

### CIA Assessment

**Confidentiality: 4 — High**

Backups may contain sensitive production information.

**Integrity: 5 — Critical**

Corrupted or attacker-modified backups may make recovery impossible.

**Availability: 5 — Critical**

Backup availability is essential during destructive incidents.

### Primary Security Concerns

- ransomware
- backup deletion
- administrator compromise
- destructive insider activity
- credential theft
- recovery failure

### Required Architectural Direction

Backup architecture should include:

- separation from production administration
- encryption
- immutable or protected copies
- restricted deletion permissions
- recovery testing
- offline or logically isolated recovery capability

---

## 14. Crown Jewel Dependency Model

The crown jewels are not independent.

A simplified dependency relationship is:

```text
Identity Infrastructure
        │
        ├──> Privileged Access
        │
        ├──> Applications
        │
        ├──> Source Control
        │
        └──> Security Platforms

Secrets Management
        │
        ├──> Applications
        ├──> Databases
        └──> CI/CD

Source Repository
        │
        ▼
     CI/CD
        │
        ▼
 Production Applications
        │
        ▼
    Databases

Security Monitoring
        │
        ▼
 Detection & Response

Backup Infrastructure
        │
        ▼
 Enterprise Recovery
```

This dependency model means compromise of certain assets can create cascading risk.

Identity infrastructure and secrets management therefore receive especially high architectural priority.

---

## 15. Phase 2 Conclusion

The highest-priority ResTech crown jewels are those that either:

1. contain highly sensitive information, or
2. provide control over other critical systems.

This analysis will be used by the Project Redoubt risk register and security-prioritisation process.
