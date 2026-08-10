# ResTech — Business and Security Requirements

## 1. Purpose

This document defines the high-level business and security requirements driving the ResTech enterprise security architecture.

Every major security control implemented within Aegis-Fabric should ultimately be traceable to a business, security or risk requirement.

---

## 2. Business Requirements

### BR-001 — Secure Remote Work

ResTech employees must be able to securely access authorised company resources from corporate offices and approved remote locations.

### BR-002 — Cloud Adoption

ResTech must support applications and infrastructure hosted within public cloud environments.

### BR-003 — Application Availability

Critical customer and internal applications must remain available during normal business operations and recoverable infrastructure failures.

### BR-004 — Protect Research

Research information and intellectual property must be protected against unauthorised disclosure, modification and destruction.

### BR-005 — Protect Customer Information

Customer information must only be accessible to authorised personnel and approved applications.

### BR-006 — Support Software Development

Developers must have access to development environments and source-code systems without automatically receiving access to production infrastructure.

### BR-007 — Contractor Access

External contractors must be able to access specifically authorised resources without receiving the same privileges as permanent employees.

### BR-008 — Business Continuity

Critical business services must be recoverable following infrastructure failure, cyberattack or data corruption.

### BR-009 — Auditability

ResTech must maintain sufficient security logging to investigate security incidents and sensitive administrative actions.

### BR-010 — Scalability

The architecture must support growth in users, workloads, applications and cloud services without requiring fundamental redesign.

---

## 3. Security Requirements

### SR-001 — Strong Authentication

Access to sensitive ResTech resources must require authenticated identities.

Privileged and high-risk access must support multi-factor authentication.

### SR-002 — Least Privilege

Users and workloads must receive only the permissions necessary to perform authorised functions.

### SR-003 — No Implicit Network Trust

Access must not be granted solely because a user, device or workload exists on an internal network.

### SR-004 — Central Identity

Where practical, enterprise applications should use centrally managed identity and authentication services.

### SR-005 — Central Authorisation

Sensitive application access should be evaluated using centrally defined authorisation policies.

### SR-006 — Privileged Access Separation

Administrative privileges must be separated from normal user identities.

Example:

```text
Normal account:
alex.employee

Administrative account:
alex.admin
```

### SR-007 — Segmentation

User, application, database, management and security environments must be logically separated.

### SR-008 — Direct Database Access

Normal employee endpoints must not directly access production databases.

Access should occur through authorised applications or specifically approved administrative paths.

### SR-009 — Workload Authentication

Applications and services should authenticate using unique workload identities rather than shared credentials.

### SR-010 — Secrets Protection

Passwords, API keys, certificates and other secrets must not be stored directly within application source code.

### SR-011 — Security Logging

Security-relevant events must be forwarded to central monitoring infrastructure.

### SR-012 — Access Logging

Sensitive resource access must produce sufficient logs to determine:

- who accessed the resource
- what resource was accessed
- what action was performed
- whether access succeeded
- when access occurred

### SR-013 — Lateral Movement Protection

Security controls should detect or prevent unauthorised movement between network and application environments.

### SR-014 — Default Deny

Access should be denied unless explicitly authorised.

### SR-015 — Device Context

Sensitive systems should support access decisions partly based on device security posture.

### SR-016 — High-Risk Sessions

High-risk authentication sessions should support:

- denial
- additional verification
- session termination
- security alert generation

### SR-017 — Data Classification

Information must be classified according to business sensitivity.

### SR-018 — Encryption

Sensitive information must be protected using appropriate encryption during transmission and, where required, while stored.

### SR-019 — Incident Response

ResTech must maintain defined procedures for responding to security incidents.

### SR-020 — Recovery

Critical systems and information must have documented recovery mechanisms.

### SR-021 — Security Monitoring

Authentication, endpoints, networks, applications and infrastructure must produce security telemetry.

### SR-022 — Administrative Audit

Privileged administrative activities must be logged.

### SR-023 — Security Testing

Security architecture and controls must be periodically validated through authorised security testing.

### SR-024 — Attack Containment

The compromise of a single workstation, user identity or application should not automatically compromise unrelated enterprise resources.

### SR-025 — Policy as Code

Where practical, security and authorisation policies should be version controlled and testable.

---

## 4. Architectural Principles

```text
Verify explicitly
Use least privilege
Assume compromise
Default deny
Minimise trust boundaries
Segment critical services
Centralise security telemetry
Protect identities
Protect data at its source
Automate repeatable controls
Design for recovery
```
