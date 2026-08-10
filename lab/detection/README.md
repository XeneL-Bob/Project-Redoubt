# Project Redoubt Detection Engine

The Phase 6 detection engine consumes central Project Redoubt JSON security telemetry and generates structured security alerts.

## Architecture

    Identity / Gateway / Workloads
                │
                ▼
       Security Telemetry
                │
                ▼
         Detection Engine
                │
                ▼
          Alert Evidence

## Detection Types

The engine currently supports:

- exact event matching
- threshold detection
- temporal correlation
- missing-prior-event detection

## Network Isolation

The detection container uses:

    network_mode: none

The engine therefore requires no direct network access to:

- Keycloak
- OPA
- Gateway
- application workloads
- Vault
- PostgreSQL
- the Internet

It consumes telemetry through the shared runtime evidence volume.

## Historical Event Baseline

On first startup, existing telemetry is treated as historical baseline data.

This prevents pre-Phase-6 telemetry without correlation identifiers from generating false-positive policy-bypass alerts.

Only new events after the baseline are actively evaluated.

## Runtime Outputs

    evidence/runtime/security-events.jsonl
    evidence/runtime/security-alerts.jsonl
    evidence/runtime/detection-state.json

These runtime files are intentionally excluded from Git.
