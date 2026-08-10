# ResTech — Recovery Architecture

## 1. Purpose

Security architecture must support restoration of trusted operation after compromise.

Recovery is not simply data backup.

It includes:

- identity
- configuration
- infrastructure
- applications
- data
- security controls

---

## 2. Recovery Principle

```text
Compromised Production
       │
       X
       │
       ▼
Destroy All Recovery Capability
```

The recovery environment must maintain independent protections.

---

## 3. Recovery Layers

### Layer 1 — Data

- database backups
- application data
- research data

### Layer 2 — Configuration

- infrastructure configuration
- firewall policy
- application configuration
- security configuration

### Layer 3 — Identity

- identity configuration
- privileged recovery process
- trusted credentials

### Layer 4 — Infrastructure

- infrastructure definitions
- deployment automation
- known-good images

---

## 4. Backup Architecture

```text
Production
    │
    │ controlled backup
    ▼
Backup Service
    │
    ▼
Protected Backup Store
    │
    ├── Current Recovery
    └── Immutable / Isolated Recovery
```

---

## 5. Administrative Separation

Backup administration should be separated from normal production administration where practical.

---

## 6. Recovery Order

Example recovery priority:

```text
1. Identity
2. Network / Core Infrastructure
3. Security Monitoring
4. Secrets
5. Critical Applications
6. Critical Databases
7. Development Systems
8. Normal Business Services
```

Actual recovery priorities will be refined during resilience testing.

---

## 7. Recovery Validation

A backup is not considered reliable solely because the backup job succeeded.

Testing should validate:

```text
Backup Exists
     ↓
Backup Accessible
     ↓
Backup Not Corrupted
     ↓
Restore Works
     ↓
Restored System Trusted
     ↓
Service Operational
```

---

## 8. Attack Scenario

For AP-005 ransomware:

```text
Attacker
   ↓
Production Compromise
   ↓
Attempts Backup Deletion
   ↓
DENIED / CONSTRAINED
   ↓
Protected Recovery Copy Remains
   ↓
Trusted Restore
```

---

## 9. Related Risk

- R-009 Backup Destruction During Ransomware
