# ResTech — Security Control Opportunities

## 1. Purpose

This document records where the future Project Redoubt architecture can interrupt the attack paths identified during Phase 3.

This is not yet a product-selection document.

---

## 2. Identity Control Opportunities

Attack paths affected:

- AP-001
- AP-002
- AP-007

Required capabilities:

- strong authentication
- MFA
- separate privileged identity
- contextual access
- role-based access
- account lifecycle management
- session revocation
- authentication telemetry

---

## 3. Network Control Opportunities

Attack paths affected:

- AP-001
- AP-003
- AP-005
- AP-007

Required capabilities:

- security zones
- default-deny rules
- management isolation
- workload segmentation
- database isolation
- east-west telemetry

---

## 4. Application Control Opportunities

Attack paths affected:

- AP-003

Required capabilities:

- secure application design
- explicit authorisation
- input validation
- workload identity
- secrets protection
- application telemetry

---

## 5. Privileged Access Opportunities

Attack paths affected:

- AP-002
- AP-005
- AP-008

Required capabilities:

- dedicated admin identities
- restricted management paths
- strong MFA
- limited standing privilege
- privileged auditing
- independent recovery administration

---

## 6. Software Supply-Chain Opportunities

Attack paths affected:

- AP-004

Required capabilities:

- protected branches
- code review
- secret scanning
- dependency controls
- isolated build agents
- artifact validation
- controlled production deployment

---

## 7. Security Monitoring Opportunities

Applies across all attack paths.

Telemetry should answer:

```text
Who performed the action?
What identity was used?
What endpoint or workload originated it?
What resource was targeted?
Was the request allowed?
What policy made the decision?
Was the behaviour expected?
```

---

## 8. Recovery Opportunities

Attack path affected:

- AP-005

Required capabilities:

- protected backups
- isolated recovery administration
- immutable recovery copies
- credential recovery
- known-good configuration
- restoration testing

---

## 9. Defence-in-Depth Model

For a high-risk path, Project Redoubt should aim for:

```text
ATTACK
   │
   ▼
PREVENT
   │ failure
   ▼
CONSTRAIN
   │ failure
   ▼
DETECT
   │
   ▼
CONTAIN
   │
   ▼
RECOVER
```

The architecture should not rely on the assumption that prevention will always succeed.

---

## 10. Phase 3 Architectural Output

The threat model establishes the inputs required for Phase 4:

```text
Threat Actor
      +
Attack Surface
      +
Trust Boundary
      +
Attack Path
      +
Risk
      ↓
Required Security Capability
      ↓
Architecture Design
```

Phase 4 can therefore select architecture patterns and technologies based on demonstrated security requirements rather than preference.
