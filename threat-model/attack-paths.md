# ResTech — Attack Paths

## 1. Purpose

Attack paths model sequences of attacker actions leading from an initial foothold toward a ResTech crown jewel.

Security architecture will later be designed to interrupt these paths at multiple points.

---

# AP-001 — Phished Employee to Crown Jewel

```text
External Attacker
        │
        ▼
Phishing
        │
        ▼
Employee Credentials
        │
        ▼
Valid Employee Session
        │
        ▼
Internal Resource Discovery
        │
        ▼
Attempted Privilege Expansion
        │
        ▼
Lateral Movement
        │
        ▼
Crown Jewel
```

## Relevant Risks

- R-001
- R-003

## Desired Interruption Points

```text
Phishing
   ↓
[MFA / authentication controls]
   ↓
Employee Session
   ↓
[least privilege]
   ↓
Discovery
   ↓
[segmentation]
   ↓
Privilege Attempt
   ↓
[detection + denial]
```

---

# AP-002 — Compromised Administrator

```text
Credential Theft
      │
      ▼
Privileged Identity
      │
      ▼
Management Access
      │
      ├──> Identity
      ├──> Infrastructure
      ├──> Security Systems
      └──> Backup Systems
```

## Relevant Risks

- R-002
- R-008
- R-009

## Architectural Goal

Compromise of one privileged identity must not equal unrestricted enterprise control.

---

# AP-003 — Public Application to Database

```text
Internet
   │
   ▼
Public Application
   │
   ▼
Application Exploitation
   │
   ▼
Workload Execution
   │
   ▼
Credential / Secret Discovery
   │
   ▼
Database Access
   │
   ▼
Customer Data
```

## Relevant Risks

- R-004
- R-007
- R-011

## Required Breakpoints

- application hardening
- workload identity
- secret isolation
- database segmentation
- least-privilege database permissions
- application telemetry

---

# AP-004 — Developer to Software Supply Chain

```text
Developer Identity
       │
       ▼
Source Repository
       │
       ▼
Malicious / Compromised Change
       │
       ▼
CI/CD
       │
       ▼
Build Artifact
       │
       ▼
Production Deployment
```

## Relevant Risk

- R-006

## Required Breakpoints

- strong developer authentication
- protected branches
- mandatory review
- pipeline policy
- secret scanning
- artifact validation
- deployment approval

---

# AP-005 — Ransomware to Recovery Infrastructure

```text
Initial Access
     │
     ▼
Endpoint Compromise
     │
     ▼
Credential Theft
     │
     ▼
Privilege Escalation
     │
     ▼
Lateral Movement
     │
     ▼
Production Control
     │
     ├──> Encrypt Production
     │
     └──> Attack Backups
```

## Relevant Risks

- R-002
- R-003
- R-009

## Architectural Objective

The attacker should encounter independent controls before reaching backup deletion or recovery administration.

---

# AP-006 — Insider Research Exfiltration

```text
Valid Researcher
      │
      ▼
Research Repository
      │
      ▼
Large / Unusual Collection
      │
      ▼
External Transfer
```

## Relevant Risk

- R-012

## Security Requirement

Because the identity may be legitimate, controls require:

- least privilege
- data-access telemetry
- unusual behaviour detection
- controlled sharing

---

# AP-007 — Contractor to Internal Resource

```text
Contractor Identity
      │
      ▼
Approved Project Resource
      │
      ▼
Attempt Access Beyond Scope
      │
      ▼
Sensitive Internal Resource
```

## Relevant Risk

- R-010

## Required Breakpoints

- project-specific roles
- explicit authorisation
- segmentation
- account expiry
- monitoring

---

# AP-008 — Security Platform Compromise

```text
Privileged Foothold
       │
       ▼
Security Platform
       │
       ├──> Disable Detection
       ├──> Modify Rules
       └──> Delete Evidence
```

## Relevant Risk

- R-008

## Architectural Requirement

Security administration must itself be treated as privileged and monitored activity.

---

## Attack-Path Design Principle

Project Redoubt should avoid reliance on a single preventative control.

Preferred design:

```text
Prevent
   │
   ▼
Constrain
   │
   ▼
Detect
   │
   ▼
Contain
   │
   ▼
Recover
```

A successful initial compromise should therefore not imply successful completion of the attack path.
