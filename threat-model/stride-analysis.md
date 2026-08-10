# ResTech — STRIDE Threat Analysis

## 1. Purpose

STRIDE is used to systematically examine threats affecting major Project Redoubt components and trust boundaries.

STRIDE categories are:

```text
S — Spoofing
T — Tampering
R — Repudiation
I — Information Disclosure
D — Denial of Service
E — Elevation of Privilege
```

---

## 2. Identity Provider

### Spoofing

- stolen user credentials
- stolen session token
- impersonated workload

### Tampering

- unauthorised role modification
- MFA-policy modification

### Repudiation

- administrative action without sufficient audit evidence

### Information Disclosure

- credential or token exposure
- identity metadata disclosure

### Denial of Service

- authentication service disruption

### Elevation of Privilege

- user becomes administrator
- manipulated group membership

---

## 3. Customer Portal

### Spoofing

- stolen customer or employee session

### Tampering

- modified request
- malicious input
- unauthorised transaction modification

### Repudiation

- sensitive actions without attributable logging

### Information Disclosure

- customer data exposure

### Denial of Service

- application resource exhaustion

### Elevation of Privilege

- broken authorisation
- application exploit

---

## 4. Finance Application

Primary STRIDE concerns:

| Category | Example |
|---|---|
| Spoofing | Compromised Finance identity |
| Tampering | Financial record modification |
| Repudiation | Transaction cannot be attributed |
| Information Disclosure | Payroll exposure |
| DoS | Finance service unavailable |
| Elevation | Reader becomes approver/admin |

---

## 5. CI/CD

| Category | Example |
|---|---|
| Spoofing | Stolen pipeline identity |
| Tampering | Build or source modification |
| Repudiation | Unattributed deployment |
| Information Disclosure | Deployment-secret exposure |
| DoS | Pipeline disruption |
| Elevation | Build process gains excessive production rights |

---

## 6. Secrets Management

| Category | Example |
|---|---|
| Spoofing | Fake workload identity |
| Tampering | Secret replacement |
| Repudiation | Secret retrieval not logged |
| Information Disclosure | Secret extraction |
| DoS | Secret service unavailable |
| Elevation | Workload retrieves unrelated secrets |

---

## 7. Security Monitoring

| Category | Example |
|---|---|
| Spoofing | Fake telemetry source |
| Tampering | Alert or log modification |
| Repudiation | Admin changes unrecorded |
| Information Disclosure | Incident evidence exposed |
| DoS | Telemetry ingestion disabled |
| Elevation | Analyst gains security-admin capability |

---

## 8. Backup Infrastructure

| Category | Example |
|---|---|
| Spoofing | Stolen backup admin identity |
| Tampering | Backup corruption |
| Repudiation | Deletion without attribution |
| Information Disclosure | Sensitive backup exposure |
| DoS | Recovery service unavailable |
| Elevation | Production admin obtains backup-admin privilege |

---

## 9. STRIDE Across Trust Boundaries

Highest-priority boundaries for STRIDE analysis are:

1. Internet → public application
2. user → enterprise application
3. standard identity → privileged context
4. application → database
5. workload → secrets
6. development → production
7. corporate network → management network
8. production → security monitoring
9. production → backup infrastructure

---

## 10. Architectural Use

STRIDE findings do not directly prescribe products.

They identify security properties the architecture must provide:

```text
Spoofing
→ Authentication

Tampering
→ Integrity

Repudiation
→ Auditability

Information Disclosure
→ Confidentiality

Denial of Service
→ Availability

Elevation of Privilege
→ Authorisation / Least Privilege
```
