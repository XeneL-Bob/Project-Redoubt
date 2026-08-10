# ResTech — Regulatory and Governance Requirements

## 1. Purpose

This document defines the regulatory, governance and cybersecurity frameworks considered during the design of the fictional ResTech security architecture.

Project Redoubt is an educational security architecture laboratory.

The project does not claim that ResTech is formally certified against any framework or regulatory standard.

---

## 2. Australian Privacy Considerations

Because the fictional ResTech organisation operates within Australia and handles personal information, the architecture considers Australian privacy and information-protection requirements.

Security capabilities should support:

- protection of personal information
- controlled access to personal information
- secure information storage
- monitoring of sensitive access
- incident investigation
- data-breach response
- appropriate retention and destruction

Formal applicability and compliance requirements would require legal and regulatory assessment in a real organisation.

---

## 3. Internal Privacy Principles

```text
Collect only required personal information.
Limit access to authorised personnel.
Protect stored personal information.
Protect information during transmission.
Maintain security logs.
Review access to sensitive systems.
Remove unnecessary data.
Respond to suspected data breaches.
```

---

## 4. NIST Cybersecurity Framework

ResTech uses the NIST Cybersecurity Framework as a high-level cybersecurity governance reference.

The architecture considers:

```text
GOVERN
IDENTIFY
PROTECT
DETECT
RESPOND
RECOVER
```

| Function | ResTech Capability |
|---|---|
| Govern | Policies, architecture decisions and risk management |
| Identify | Asset inventory and threat modelling |
| Protect | MFA, segmentation, encryption and access control |
| Detect | SIEM, endpoint telemetry and network detection |
| Respond | Incident-response procedures |
| Recover | Backups and recovery architecture |

---

## 5. Zero Trust Architecture

ResTech's security architecture is based on Zero Trust principles.

Core principles include:

```text
Do not automatically trust internal networks.
Authenticate identities.
Authorise resource requests.
Apply least privilege.
Evaluate context.
Protect individual resources.
Continuously monitor activity.
Assume compromise can occur.
```

---

## 6. Zero Trust Security Areas

The project separates Zero Trust architecture into:

```text
Identity
Devices
Networks and Environments
Applications and Workloads
Data
```

Cross-cutting capabilities include:

```text
Visibility
Analytics
Automation
Governance
```

---

## 7. MITRE ATT&CK

ResTech uses MITRE ATT&CK as a threat-informed security reference for modelling realistic attacker behaviour.

Attack scenarios may be mapped to:

```text
Reconnaissance
Resource Development
Initial Access
Execution
Persistence
Privilege Escalation
Defense Evasion
Credential Access
Discovery
Lateral Movement
Collection
Command and Control
Exfiltration
Impact
```

The architecture should identify controls capable of:

```text
Preventing
Detecting
Containing
Responding
Recovering
```

from relevant attacker behaviours.

---

## 8. Secure Development

ResTech applications should follow secure software-development principles.

Development requirements include:

- source-code review
- dependency management
- secret scanning
- vulnerability scanning
- controlled CI/CD access
- separation between development and production
- application security testing
- secure configuration management

---

## 9. Least Privilege Governance

Access must follow:

```text
Need to know
Need to use
Minimum required privilege
Minimum required duration
```

Administrative privileges must not be assigned solely because a user belongs to the IT or Cybersecurity department.

---

## 10. Separation of Duties

Examples:

```text
Developer
≠
Production Administrator
```

```text
Security Analyst
≠
Finance Administrator
```

```text
Infrastructure Administrator
≠
Security Log Administrator
```

The objective is to limit unnecessary concentration of privilege.

---

## 11. Logging Requirements

Security logs should support investigation of:

- successful authentication
- failed authentication
- MFA events
- privileged access
- policy decisions
- account changes
- sensitive data access
- application errors
- firewall activity
- endpoint alerts
- security configuration changes

Security logs should themselves be treated as sensitive information.

---

## 12. Security Incident Governance

```text
Detection
    ↓
Validation
    ↓
Containment
    ↓
Investigation
    ↓
Eradication
    ↓
Recovery
    ↓
Lessons Learned
```

---

## 13. Risk Management Principle

ResTech recognises that cybersecurity controls cannot eliminate all risk.

The security architecture therefore aims to:

```text
Reduce likelihood
Reduce impact
Reduce attacker freedom
Increase detection capability
Increase response speed
Improve recovery capability
```

Residual risks should be explicitly documented rather than assumed to have been eliminated.

---

## 14. Governance Principles

The ResTech architecture should maintain:

- documented security requirements
- traceable architecture decisions
- defined ownership of critical assets
- documented residual risk
- repeatable control validation
- periodic access reviews
- defined incident-response responsibilities
- documented recovery requirements
