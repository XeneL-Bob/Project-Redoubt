# ResTech — Security Telemetry Architecture

## 1. Purpose

Project Redoubt requires security evidence from every major control plane.

Logging is treated as architecture rather than an afterthought.

---

## 2. Telemetry Sources

### Identity

- authentication
- MFA
- role changes
- account changes
- session events

### Endpoint

- process execution
- authentication activity
- security alerts
- suspicious persistence
- network connections

### Network

- firewall decisions
- IDS alerts
- connection metadata
- denied connections

### Application

- authentication context
- authorisation decisions
- sensitive actions
- application errors

### Policy

- requested identity
- requested resource
- requested action
- policy result
- reason for decision

### Workload

- service authentication
- API requests
- secret access
- database access

### Infrastructure

- privileged administration
- configuration changes
- deployments

### Backup

- backup job
- deletion request
- restore
- administrative change

---

## 3. Telemetry Flow

```text
Identity ───────┐
Endpoints ──────┤
Network ────────┤
Applications ───┤
Policy Engine ──┤
Workloads ──────┤
Infrastructure ─┤
Backups ────────┘
       │
       ▼
Central Collection
       │
       ▼
Security Event Store
       │
       ▼
Detection Engine
       │
       ▼
Alert
       │
       ▼
Security Analyst
```

---

## 4. Security Event Schema

Where practical, events should identify:

```text
timestamp
subject
subject_type
device
source
destination
resource
action
result
policy
session
risk
correlation_id
```

---

## 5. Detection Use Cases

Project Redoubt should eventually detect:

- repeated authentication failures
- impossible or abnormal privilege changes
- unauthorised Finance access
- direct database connection attempts
- lateral movement
- unusual secret access
- suspicious CI/CD activity
- log deletion attempts
- backup deletion attempts

---

## 6. Tamper Resistance

A compromised application should not be able to silently delete all evidence relating to its own activity.

Where practical:

```text
Source
  ↓
Forward Telemetry
  ↓
Independent Security Storage
```

---

## 7. Attack Validation

Later attack simulation will compare:

```text
Attack Performed
      ↓
Expected Telemetry
      ↓
Observed Telemetry
      ↓
Detection Triggered?
      ↓
Response Performed?
```

This becomes evidence of security effectiveness.
