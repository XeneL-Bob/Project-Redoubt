# Project Redoubt — Security Architecture Assurance Model

## Purpose

Project Redoubt uses security assurance to determine whether documented architecture decisions are supported by identifiable implementation and validation evidence.

Traceability alone does not prove effectiveness.

The assurance model therefore distinguishes:

- requirements
- risks
- attack paths
- security objectives
- architecture decisions
- architecture controls
- implementations
- tests
- detections
- evidence
- known limitations

## Assurance Chain

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
    Test / Adversary Scenario
            ↓
    Detection
            ↓
    Evidence
            ↓
    Assurance Assessment

The chain may contain legitimate gaps where a relationship is not explicitly established.

Project Redoubt must not invent links merely to make the matrix appear complete.

## Assurance Status

### DOCUMENTED

The requirement, architecture decision or control exists in Project Redoubt documentation.

This status does not imply implementation.

### IMPLEMENTED

A corresponding technical control or configuration exists in the laboratory or reference architecture.

Implementation alone does not prove effectiveness.

### VALIDATED

The implemented control has been exercised through a relevant repeatable test and produced the expected result.

### PARTIALLY_VALIDATED

Meaningful portions of the architecture or attack path have been tested, but important stages remain outside the current implementation or test scope.

### DEFERRED

The control or attack-path validation cannot currently be exercised because the necessary system or realistic test environment does not exist.

### NOT_VALIDATED

The architecture relationship exists but no adequate validation evidence has been produced.

## Adversary Result Semantics

Project Redoubt uses the following terms consistently:

- PREVENTED — the tested attacker action was blocked
- DETECTED — the expected detection fired
- CONTAINED — the attacker could not progress beyond the tested boundary
- MISSED — the expected control or detection did not operate as intended

These terms describe the tested scenario only.

They do not establish universal effectiveness.

## Evidence Types

Project Redoubt recognises evidence including:

- DOCUMENTATION
- CONFIGURATION
- UNIT_TEST
- INTEGRATION_TEST
- ADVERSARY_TEST
- DETECTION
- INCIDENT_RESPONSE_TEST
- RECOVERY_TEST
- CI_GATE
- POLICY_DECISION
- MACHINE_READABLE_EVIDENCE

Evidence types are not treated as a simple maturity hierarchy.

Different controls require different forms of evidence.

## Assurance Strength

An assurance assessment considers:

1. whether the architecture relationship is explicit
2. whether an implementation exists
3. whether the implementation is testable
4. whether a negative case has been exercised
5. whether telemetry is produced
6. whether expected detections fire
7. whether attacker progression is constrained
8. whether the result is repeatable
9. whether machine-readable evidence is retained
10. what important limitations remain

## Production Boundary

Project Redoubt is a reference architecture and security engineering laboratory.

Unless explicitly stated otherwise, assurance results do not represent:

- production certification
- independent penetration-test certification
- regulatory certification
- live enterprise control effectiveness
- production cloud configuration assurance
- complete attacker coverage

## Core Principle

A missing or deferred validation result is preferable to fabricated assurance.

Project Redoubt only claims validation when a corresponding control exists and can actually be exercised.
