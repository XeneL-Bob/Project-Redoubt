# Project Redoubt — IaC Control Validation Matrix

| ID | Security Requirement | Enforcement | Negative Validation | Result |
|---|---|---|---|---|
| IAC-001 | Internet ingress must be HTTPS only | OPA plan policy | Public TCP/80 plan | PASS |
| IAC-002 | SSH must not be Internet exposed | OPA plan policy | Public TCP/22 plan | PASS |
| IAC-003 | Private zones must not auto-assign public IPs | OPA plan policy | Management public-IP plan | PASS |
| IAC-004 | Internet default routes belong only in the edge zone | OPA plan policy | Private default-route plan | PASS |
| IAC-005 | Security evidence must block public access | OPA plan policy | Public-access protection disabled | PASS |
| IAC-006 | Security evidence must use KMS encryption | OPA plan policy | Encryption downgraded to AES256 | PASS |
| IAC-007 | Evidence versioning must remain enabled | OPA plan policy | Versioning suspended | PASS |
| IAC-008 | KMS rotation must remain enabled | OPA plan policy | Key rotation disabled | PASS |
| IAC-009 | Network telemetry must capture all traffic | OPA plan policy | Flow logs reduced to ACCEPT | PASS |
| IAC-010 | Security-sensitive resources require metadata | OPA plan policy | DataClassification removed | PASS |
| IAC-011 | Unrestricted Internet egress is prohibited | OPA plan policy | 0.0.0.0/0 unrestricted egress | PASS |

## Enforcement Layers

The controls are validated through:

    Architecture Requirement
            ↓
    OpenTofu Configuration
            ↓
    OpenTofu Plan
            ↓
    OPA Policy
            ↓
    Automated Negative Test
            ↓
    CI Security Gate
            ↓
    Evidence

## Architectural Objectives

The Phase 11 controls primarily support:

- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-007 — Centralise Security Visibility
- SO-010 — Maintain Recoverability
- SO-011 — Make Policy Testable
- SO-012 — Produce Security Evidence

The policy gate also strengthens the controls supporting software delivery and privileged infrastructure administration by preventing insecure infrastructure changes from becoming deployable configurations.
