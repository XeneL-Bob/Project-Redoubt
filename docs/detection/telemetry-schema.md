# Project Redoubt — Security Telemetry Schema

## Event Model

Project Redoubt uses structured JSON security telemetry.

Core fields:

| Field | Purpose |
|---|---|
| timestamp | UTC event timestamp |
| source | Component producing the event |
| event_type | Normalised security event type |
| outcome | allow, deny or error |
| subject | Human or workload identity |
| resource | Target protected resource |
| correlation_id | Connects events belonging to one transaction |
| details | Event-specific security context |

## Correlation

Phase 6 introduces transaction correlation across security boundaries.

Example successful Finance request:

    correlation_id = UUID

    Gateway
    └── policy_decision = allow
            │
            ▼
    Finance API
    ├── vault_secret_access = allow
    │
    └── application_access = allow

All events associated with the request carry the same correlation identifier.

This allows detection logic to identify expected event chains and detect missing control-plane events.

## Alerts

Detection alerts include:

| Field | Purpose |
|---|---|
| alert_id | Unique alert identifier |
| timestamp | Detection generation time |
| detection_id | Project Redoubt detection identifier |
| title | Detection name |
| severity | Alert severity |
| subject | Relevant identity |
| resource | Relevant protected resource |
| correlation_id | Related transaction |
| attack_techniques | ATT&CK context where applicable |
| risk_ids | Related Project Redoubt risks |
| source_event_type | Event responsible for the alert |

## Runtime Evidence

Runtime telemetry is stored in:

    evidence/runtime/security-events.jsonl

Alerts are stored in:

    evidence/runtime/security-alerts.jsonl

Detection processing state is stored in:

    evidence/runtime/detection-state.json

Runtime evidence remains excluded from Git.
