# Project Redoubt — Threat Model

## Phase 3 — Enterprise Threat Modelling

This directory contains the threat model for the fictional ResTech enterprise.

Phase 3 translates the risks identified during Phase 2 into concrete attacker behaviours, trust-boundary violations and attack paths.

The objective is to answer:

> How could a realistic attacker move from an initial foothold to a ResTech crown jewel, and where must the architecture break that path?

---

## Threat-Modelling Flow

```text
Enterprise Definition
        ↓
Crown Jewels
        ↓
Risk Register
        ↓
Threat Actors
        ↓
Attack Surface
        ↓
Trust Boundaries
        ↓
Abuse Cases
        ↓
Attack Paths
        ↓
STRIDE Analysis
        ↓
MITRE ATT&CK Mapping
        ↓
Security Architecture
```

---

## Documents

| Document | Purpose |
|---|---|
| `threat-actors.md` | Defines relevant attacker types and capabilities |
| `attack-surface.md` | Identifies exposed enterprise entry points |
| `trust-boundaries.md` | Defines where trust context changes |
| `abuse-cases.md` | Describes misuse and hostile scenarios |
| `attack-paths.md` | Models paths from foothold to crown jewel |
| `stride-analysis.md` | Applies STRIDE to major system components |
| `mitre-attack-mapping.md` | Maps scenarios to MITRE ATT&CK |
| `security-control-opportunities.md` | Identifies where architecture must interrupt attacks |

---

## Modelling Principles

Project Redoubt assumes:

- internal networks are not trusted by default
- authenticated users may still be malicious or compromised
- endpoints may become compromised
- workloads may be exploited
- credentials and sessions may be stolen
- administrators may make mistakes
- privileged accounts may be compromised
- security tooling may itself become a target

The threat model therefore focuses on **attack paths**, not just isolated vulnerabilities.

---

## Scope

Included:

- identity
- users
- privileged administration
- endpoints
- applications
- workloads
- APIs
- databases
- CI/CD
- source control
- secrets
- security monitoring
- backup infrastructure
- cloud resources
- internal networks

Excluded from Phase 3:

- physical building security
- detailed vendor-specific vulnerabilities
- production penetration testing
- destructive testing against real systems

All attack activity described by Project Redoubt is intended only for the authorised fictional laboratory.
