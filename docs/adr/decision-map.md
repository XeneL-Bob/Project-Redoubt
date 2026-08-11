# Project Redoubt — Architecture Decision Map

## Purpose

This document shows how the major Project Redoubt architecture decisions relate to security objectives and implemented security capabilities.

The ADR set records why the architecture exists.

The control-traceability model records how those decisions are implemented and validated.

## Decision Domains

### Zero Trust and Identity

    ADR-001 Zero Trust
        ↓
    ADR-002 Central Policy / Distributed Enforcement
        ↓
    ADR-003 Authentication != Authorisation
        ↓
    ADR-004 Dedicated Workload Identity

These decisions establish the core access-control model.

### Privileged Operations and Resilience

    ADR-005 Dedicated Management Plane

    ADR-006 Central Security Telemetry

    ADR-007 Isolated Recovery Architecture

These decisions protect administrative authority, security visibility and recoverability.

### Software Supply Chain

    ADR-008 Separate Release Signing and Deployment Approval
        ↓
    ADR-009 Verification != Deployment Authority

These decisions create independent trust domains between artifact assurance and release execution.

### Infrastructure Governance

    ADR-010 Declarative Infrastructure with OpenTofu
        ↓
    ADR-011 Infrastructure Policy as Code with OPA
        ↓
    ADR-012 Pre-Deployment Infrastructure Policy Gate

These decisions convert selected architecture requirements into machine-enforceable infrastructure controls.

## Decision-to-Objective Matrix

| ADR | Architecture Decision | Security Objectives |
|---|---|---|
| ADR-001 | Zero Trust security model | SO-001, SO-003, SO-004, SO-009 |
| ADR-002 | Central policy with distributed enforcement | SO-003, SO-004, SO-009, SO-011 |
| ADR-003 | Authentication separated from authorisation | SO-001, SO-002, SO-004, SO-009 |
| ADR-004 | Dedicated workload identities | SO-004, SO-005, SO-009 |
| ADR-005 | Dedicated management plane | SO-002, SO-009 |
| ADR-006 | Central security telemetry | SO-007, SO-008, SO-012 |
| ADR-007 | Isolated recovery architecture | SO-009, SO-010, SO-012 |
| ADR-008 | Separate release signing and deployment approval | SO-006, SO-009, SO-012 |
| ADR-009 | Verification distinct from deployment authority | SO-006, SO-009, SO-011, SO-012 |
| ADR-010 | OpenTofu declarative infrastructure | SO-003, SO-004, SO-010, SO-011, SO-012 |
| ADR-011 | OPA infrastructure Policy as Code | SO-003, SO-004, SO-007, SO-010, SO-011, SO-012 |
| ADR-012 | Pre-deployment infrastructure policy gate | SO-003, SO-004, SO-007, SO-010, SO-011, SO-012 |

## Decision-to-Implementation Map

| ADR | Principal Implementation Evidence |
|---|---|
| ADR-001 | Phase 4 architecture, Phase 5 Zero Trust lab, Phase 7 adversary validation |
| ADR-002 | OPA policy engines, application PEP, management PEP |
| ADR-003 | Keycloak authentication separated from OPA authorisation |
| ADR-004 | Vault-backed workload credentials and backend enforcement |
| ADR-005 | Phase 9 JIT privileged access and isolated management plane |
| ADR-006 | Phase 6 detection engine and DET-001 through DET-020 |
| ADR-007 | Phase 8 isolated backup and recovery validation |
| ADR-008 | Phase 10 independent signer and release approver |
| ADR-009 | Phase 10 verification receipt, approval authority and deployment gate |
| ADR-010 | Phase 11 OpenTofu AWS reference architecture |
| ADR-011 | Phase 11 IAC-001 through IAC-011 |
| ADR-012 | Phase 11 real-plan testing and CI infrastructure security gate |

## Architecture Reasoning Chain

Project Redoubt uses the following reasoning model:

    Business Requirement
            ↓
    Security Requirement
            ↓
    Crown Jewel
            ↓
    Risk
            ↓
    Threat / Attack Path
            ↓
    Security Objective
            ↓
    Architecture Decision
            ↓
    Architecture Control
            ↓
    Implementation
            ↓
    Test
            ↓
    Evidence

An ADR does not prove that a control works.

The ADR records why the architecture decision was selected.

Implementation tests, adversary scenarios, detections, CI validation and evidence provide the corresponding assurance.

## Assurance Boundary

Some ADRs support controls relevant to multiple attack paths.

This does not mean that every referenced attack path has been fully validated.

Attack-path validation remains governed by the Project Redoubt adversary coverage model and documented validation evidence.
