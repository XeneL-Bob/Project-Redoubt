# Project Redoubt Incident Responder

The incident responder converts High and Critical Project Redoubt detection alerts into structured incident evidence.

Runtime inputs:

    evidence/runtime/security-alerts.jsonl

Runtime outputs:

    evidence/runtime/incidents.jsonl
    evidence/runtime/containment-actions.jsonl
    evidence/runtime/incident-state.json

The responder has no Docker network connectivity.

Containment actions are currently simulated and recorded rather than automatically enforced.
