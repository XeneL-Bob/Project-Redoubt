# Project Redoubt — Security Architecture

## Phase 4 — Zero-Trust Enterprise Security Architecture

Phase 4 converts the risks and attack paths identified during Phases 2 and 3 into a concrete security architecture for the fictional ResTech enterprise.

The architecture is intentionally vendor-neutral.

Technology products will be selected only after the required architectural capabilities have been defined.

---

## Architecture Objective

Project Redoubt must prevent a single compromise from automatically becoming an enterprise-wide compromise.

The architecture is therefore designed around:

```text
Verify explicitly
        +
Least privilege
        +
Assume compromise
        +
Default deny
        +
Continuous telemetry
        +
Strong recovery
```

---

## Architecture Domains

Phase 4 defines:

1. Enterprise system context
2. Zero Trust control architecture
3. Identity architecture
4. Authorisation architecture
5. Network segmentation
6. Application and workload security
7. Secrets management
8. Security telemetry
9. Management plane
10. Recovery architecture
11. Control traceability

---

## High-Level Architecture

```text
                    ┌───────────────────────┐
                    │      USERS / DEVICES  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      IDENTITY PLANE   │
                    │ Authentication / MFA  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      POLICY PLANE     │
                    │ PE / PA / Context     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  ENFORCEMENT POINTS   │
                    │ Proxy / API / Network │
                    └───────────┬───────────┘
                                │
             ┌──────────────────┼───────────────────┐
             ▼                  ▼                   ▼
        Applications        Workloads           Databases
             │                  │                   │
             └──────────────────┼───────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   TELEMETRY PLANE     │
                    │ SIEM / Detection      │
                    └───────────────────────┘
```

---

## Architectural Planes

Project Redoubt separates critical capabilities into logical planes.

| Plane | Purpose |
|---|---|
| Identity Plane | Establish and validate identity |
| Policy Plane | Decide whether access should occur |
| Enforcement Plane | Enforce access decisions |
| Application Plane | Deliver business services |
| Data Plane | Store sensitive information |
| Management Plane | Administer infrastructure and security |
| Telemetry Plane | Collect security evidence |
| Recovery Plane | Restore trusted operation |

Separating these functions limits concentration of privilege and creates explicit trust boundaries.

---

## Key Architectural Principle

```text
Authentication
≠
Authorisation
```

A successfully authenticated identity does not automatically receive access to a resource.

Access must still be evaluated against policy.

---

## Phase 4 Output

The output of Phase 4 becomes the technical blueprint for later implementation phases.

```text
Threat Model
     ↓
Architecture
     ↓
Technology Selection
     ↓
Implementation
     ↓
Attack Simulation
     ↓
Evidence
```

---

## Phase 11 Extension — Infrastructure Governance

Phase 11 extends the original security architecture into declarative infrastructure governance.

The architecture now includes an Infrastructure Governance capability:

    Security Architecture
            ↓
    OpenTofu
            ↓
    Infrastructure Plan
            ↓
    OPA Policy
            ↓
    ALLOW / DENY
            ↓
    CI Evidence

This capability ensures that selected architectural invariants are evaluated automatically before infrastructure changes become eligible for deployment.

The Infrastructure Governance capability does not replace the Identity, Policy, Enforcement, Management, Telemetry or Recovery planes.

It governs how infrastructure supporting those planes may be changed.
