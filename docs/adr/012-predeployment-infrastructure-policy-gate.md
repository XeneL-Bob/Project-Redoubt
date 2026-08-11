# ADR-012 — Evaluate Infrastructure Plans Before Deployment Authority

## Status

Accepted

## Context

Evaluating static Infrastructure as Code files does not always reveal the complete infrastructure change that a provisioning engine intends to perform.

Computed values, provider behaviour and resource relationships become clearer in the generated infrastructure plan.

Security policy should therefore evaluate the proposed machine-readable change before the infrastructure becomes eligible for deployment.

## Decision

Project Redoubt requires infrastructure security policy evaluation against an OpenTofu plan before deployment eligibility.

The control path is:

    Infrastructure Change
            ↓
    OpenTofu Configuration
            ↓
    Validation
            ↓
    Saved Plan
            ↓
    Plan JSON
            ↓
    OPA Security Policy
            ↓
       ALLOW / DENY
        ↙         ↘
     Reject     Eligible
               to Continue

A DENY decision causes the CI infrastructure security gate to fail.

## Security Drivers

The decision supports:

- preventive infrastructure security
- evaluation of intended change
- deterministic policy enforcement
- negative security testing
- governance evidence
- reduced insecure configuration drift through approved delivery paths

## Alternatives Considered

### Evaluate Source Configuration Only

Policy evaluates only `.tf` source files.

Reason not selected:

- source does not always expose the complete proposed infrastructure state
- derived provider values may not be represented directly

### Detect Misconfiguration After Deployment

Security tooling detects insecure infrastructure only after it exists.

Reason not selected:

- insecure architecture is temporarily deployed
- remediation becomes reactive rather than preventive

### Advisory Policy Results

Policy violations generate warnings but do not fail CI.

Reason not selected:

- insecure changes may continue despite known violations
- architecture controls would not be enforceable

## Consequences

### Positive

- insecure tested configurations are blocked before deployment eligibility
- policy decisions correspond to proposed infrastructure state
- architecture controls become CI-enforceable
- negative scenarios demonstrate fail-closed behaviour
- policy decisions generate auditable evidence

### Negative / Trade-offs

- plan generation is required before policy evaluation
- CI depends on OpenTofu and OPA availability
- plan formats must remain compatible with policy evaluation
- live state after deployment still requires separate drift controls

## Security Traceability

### Risks

- R-003
- R-004
- R-006
- R-008
- R-009
- R-011

### Security Objectives

- SO-003 — Limit Lateral Movement
- SO-004 — Protect Sensitive Data
- SO-007 — Centralise Security Visibility
- SO-010 — Maintain Recoverability
- SO-011 — Make Policy Testable
- SO-012 — Produce Security Evidence

## Implementation

Implemented through:

- saved OpenTofu plans
- `tofu show -json`
- OPA/Rego infrastructure policy
- policy evaluator
- real-plan negative test suite
- CI security gate
- SHA-256 evidence manifest
- GitHub Actions evidence artifact

## Validation Evidence

Phase 11 validates controlled misconfigurations including:

- public HTTP
- public SSH
- management public IP assignment
- private-zone default Internet routing
- evidence public-access exposure
- encryption downgrade
- disabled versioning
- disabled KMS rotation
- incomplete flow logging
- missing security metadata
- unrestricted Internet egress

All expected policy violations are rejected before deployment eligibility.

## Residual Risk

This decision does not provide:

- continuous live-cloud drift detection
- validation of manual out-of-band cloud changes
- production cloud admission enforcement
- production state-backend protection

The current assurance claim is limited to proposed infrastructure changes passing through the Project Redoubt IaC security gate.

## Review Triggers

Reconsider this ADR if:

- continuous cloud drift enforcement is introduced
- infrastructure admission moves directly into the target platform
- deployment architecture no longer uses OpenTofu plans
