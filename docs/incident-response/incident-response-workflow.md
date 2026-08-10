# Project Redoubt — Incident Response Workflow

## Purpose

Phase 8 extends Project Redoubt from detection into structured incident handling.

The implemented flow is:

    Security Event
         |
         v
    Detection Rule
         |
         v
    Security Alert
         |
         v
    Incident Responder
         |
         +--> Severity Classification
         |
         +--> Incident Record
         |
         +--> Containment Decision
         |
         v
    Evidence Preservation

## Incident Classification

High and critical detection alerts become security incidents.

Severity mapping:

| Detection Severity | Incident Severity |
|---|---|
| Critical | SEV-1 |
| High | SEV-2 |
| Medium | SEV-3 |
| Low | SEV-4 |

Phase 8 automatically creates incidents for High and Critical alerts.

## Incident Record

Incident evidence records:

- incident identifier
- creation timestamp
- status
- severity
- originating alert
- detection identifier
- affected subject
- affected resource
- correlation identifier
- related risks
- ATT&CK techniques where applicable
- triage priority

## Containment

Phase 8 records simulated containment decisions.

Critical incidents use:

    isolate_resource_path

High-severity incidents use:

    suspend_subject

Containment is intentionally simulated rather than automatically modifying identity or network infrastructure.

This preserves deterministic laboratory behaviour while demonstrating the incident-response decision path.

## Isolation

The incident responder runs with:

    network_mode: none

It consumes security-alert evidence through the runtime evidence volume.

The responder therefore has no direct application, identity, database, Vault or Internet network access.

## Historical Baselining

Existing alerts are treated as historical evidence when the incident responder first starts.

This prevents historical Phase 6 and Phase 7 alerts from being incorrectly classified as newly occurring incidents.
