# Project Redoubt — Privileged Access Detection

## Purpose

Phase 9 extends Project Redoubt detection engineering into privileged management activity.

Administrative controls are not considered complete merely because access is denied or allowed.

Privileged activity must also be observable.

## Detection Chain

    Administrator Activity
            |
            v
      Privilege Broker
            |
            v
     Management Gateway
            |
            v
        Admin OPA
            |
            v
      Management API
            |
            v
         Telemetry
            |
            v
     Detection Engine
            |
            v
          Alert
            |
            v
     Incident Response

## Phase 9 Detections

| ID | Detection | Severity |
|---|---|---|
| DET-007 | Privileged Elevation Denied | High |
| DET-008 | Repeated Privileged Elevation Denials | Critical |
| DET-009 | Direct Management Backend Access Attempt | Critical |
| DET-010 | Privileged Access from Untrusted Device | High |
| DET-011 | Security Control Modification | Medium |
| DET-012 | Management Policy Bypass | Critical |

## DET-007 — Privileged Elevation Denied

Detects rejected requests for JIT privileged elevation.

Examples include:

- non-administrator requesting elevation
- administrator requesting the wrong administrative domain
- elevation from an untrusted administrative device

## DET-008 — Repeated Privileged Elevation Denials

Detects three denied privileged-elevation attempts for the same subject within sixty seconds.

This provides threshold-based detection for repeated attempts to acquire privileged access.

## DET-009 — Direct Management Backend Access Attempt

Detects direct access attempts against the management backend using an invalid management-gateway workload credential.

This detects attempted Policy Enforcement Point bypass.

## DET-010 — Privileged Access from Untrusted Device

Detects management requests denied because administrative device trust is absent.

Identity and a previously issued elevation grant remain insufficient without the required device context.

## DET-011 — Security Control Modification

Records authorised security-control modification.

The laboratory operation:

    update-detection

is simulated and does not rewrite the live detection engine.

The operation provides observable administrative evidence for security-sensitive changes.

## DET-012 — Management Policy Bypass

Detects a successful privileged management operation without a correlated preceding management-gateway ALLOW decision.

Expected control path:

    Management Gateway ALLOW
            |
            v
       Management API
            |
            v
    Privileged Operation

A downstream privileged operation without this preceding policy decision is treated as a critical management-plane anomaly.

## Validation

DET-007 through DET-012 are covered by automated detection unit tests and live validation against the running Project Redoubt environment.

Runtime telemetry and alert evidence remain excluded from source control.
