# ResTech — Data Classification Standard

## 1. Purpose

ResTech classifies information according to the potential business impact resulting from unauthorised disclosure, modification or destruction.

Four classifications are used:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

---

## 2. PUBLIC

### Definition

Information approved for public distribution.

Unauthorised disclosure would cause little or no damage to ResTech.

### Examples

- Public website information
- Published research
- Public job advertisements
- Public product information
- Press releases
- Marketing content

### Protection Requirements

```text
Authentication:
Generally not required

Encryption in transit:
Expected for web services

Access logging:
Normal application logging

Storage restrictions:
Minimal
```

---

## 3. INTERNAL

### Definition

Information intended for ResTech employees and authorised contractors but not intended for public distribution.

### Examples

- Internal procedures
- Employee directory
- Internal project information
- Internal technical documentation
- Internal meeting records
- Non-sensitive system documentation

### Protection Requirements

```text
Authentication:
Required

Access:
Employees and authorised contractors

Encryption in transit:
Required

External sharing:
Requires approval

Logging:
Standard
```

---

## 4. CONFIDENTIAL

### Definition

Sensitive business information where unauthorised disclosure could cause significant operational, commercial or reputational harm.

### Examples

- Source code
- Internal research
- System architecture
- Security documentation
- Contracts
- Customer project information
- Internal financial reports
- Security telemetry

### Protection Requirements

```text
Authentication:
Required

Authorisation:
Role-based or policy-based

Encryption in transit:
Required

Encryption at rest:
Required where appropriate

Logging:
Required

External sharing:
Restricted

Access reviews:
Required
```

---

## 5. RESTRICTED

### Definition

ResTech's highest sensitivity classification.

Unauthorised access could result in severe financial, legal, security or operational consequences.

### Examples

- Customer personally identifiable information
- Employee personal information
- Payroll information
- Authentication secrets
- Private cryptographic keys
- API secrets
- Database passwords
- Privileged credentials
- Highly sensitive research
- Incident investigation evidence

### Protection Requirements

```text
Authentication:
Strong authentication required

MFA:
Required where applicable

Authorisation:
Strict least privilege

Access:
Explicitly authorised identities only

Encryption in transit:
Required

Encryption at rest:
Required

Logging:
Detailed auditing required

Monitoring:
Enhanced monitoring

External sharing:
Prohibited unless specifically authorised

Access review:
Regularly required
```

---

## 6. Classification Matrix

| Information | Classification |
|---|---|
| Marketing website | Public |
| Employee directory | Internal |
| Internal documentation | Internal |
| Source code | Confidential |
| Architecture diagrams | Confidential |
| Security logs | Confidential |
| Research data | Confidential |
| Customer PII | Restricted |
| HR records | Restricted |
| Payroll | Restricted |
| Database credentials | Restricted |
| Private keys | Restricted |
| Administrator passwords | Restricted |

---

## 7. Data Handling Principles

- Only collect information required for legitimate business purposes.
- Provide access only to authorised identities.
- Encrypt sensitive information where appropriate.
- Maintain audit records for sensitive access.
- Remove access when no longer required.
- Do not place Restricted information within public repositories.
- Do not commit secrets to source control.
- Use approved methods for transferring sensitive information.
- Destroy information securely when retention is no longer required.

---

## 8. Access Based on Classification

```text
PUBLIC
   │
   └── Open access

INTERNAL
   │
   └── Authenticated ResTech user

CONFIDENTIAL
   │
   └── Authenticated
       + authorised role

RESTRICTED
   │
   └── Authenticated
       + authorised
       + appropriate device
       + appropriate security context
       + enhanced monitoring
```

---

## 9. Classification Responsibilities

Data owners are responsible for determining appropriate information classifications.

System owners must implement security controls appropriate to the highest classification of information processed by their systems.

Users are responsible for handling information according to its assigned classification.
