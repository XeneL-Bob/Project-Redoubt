# Project Redoubt — Security Architecture Assurance

## Purpose

Phase 13 converts Project Redoubt's architecture documentation, implementation tests and security evidence into a structured assurance model.

The goal is to establish defensible traceability between:

    Requirements
        ↓
    Crown Jewels
        ↓
    Risks
        ↓
    Attack Paths
        ↓
    Security Objectives
        ↓
    Architecture Decisions
        ↓
    Controls
        ↓
    Implementations
        ↓
    Tests and Detections
        ↓
    Evidence
        ↓
    Assurance Status

## Phase Structure

### Phase 13A — Assurance Foundation

Establish:

- assurance terminology
- authoritative source registry
- identifier integrity validation
- machine-checkable baseline

### Phase 13B — Traceability Graph

Create machine-readable relationships between security objectives, risks, attack paths, ADRs, controls, implementations and evidence.

### Phase 13C — Coverage and Gap Analysis

Measure:

- validated areas
- partially validated areas
- deferred areas
- missing traceability
- evidence coverage
- residual assurance gaps

### Phase 13D — Assurance Gate and Acceptance

Add:

- automated traceability validation
- architecture documentation integration
- CI assurance gate
- Phase 13 acceptance record

## Assurance Principle

Project Redoubt distinguishes between:

- documented architecture
- implemented controls
- validated controls
- partially validated attack paths
- deferred validation

A relationship existing in documentation does not by itself constitute evidence of control effectiveness.

See:

- `assurance-model.md`

## Machine-Readable Traceability Graph

Phase 13B introduces:

- `assurance/traceability-graph.json`
- `assurance/validation-source-registry.json`
- `assurance/validate_graph.py`

The graph represents relationships already established by Project Redoubt source documentation.

It includes:

- security objective to requirement mappings
- security objective to crown-jewel mappings
- attack path to risk mappings
- attack-path assurance status
- ADR to security-objective mappings
- architecture control to risk mappings
- architecture control to attack-path mappings
- adversary scenario relationships
- detection-to-risk relationships
- IaC security-control validation

The graph deliberately does not manufacture relationships solely to make the traceability chain appear complete.

Missing relationships are treated as assurance gaps and are analysed separately during Phase 13C.


## Phase 13D — Final Assurance

Phase 13D adds:

- complete BR-to-SR traceability
- complete SR-to-SO traceability
- risk-to-crown-jewel traceability
- ADR-to-control relationships
- final post-remediation assurance assessment
- explicit residual assurance gaps
- Architecture Assurance CI enforcement
- Phase 13 acceptance criteria

Final machine-readable assessment:

- `assurance/final-assessment.json`

Final human-readable assessment:

- `docs/assurance/final-assurance-assessment.md`

Phase acceptance:

- `docs/assurance/phase-13-acceptance.md`
