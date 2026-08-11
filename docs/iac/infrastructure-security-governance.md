# Project Redoubt — Infrastructure Security Governance

## Purpose

Phase 11 converts Project Redoubt security architecture into enforceable Infrastructure as Code and Policy as Code.

The objective is to ensure that infrastructure security requirements are evaluated automatically before infrastructure changes are authorised for deployment.

## Governance Model

The Phase 11 decision path is:

    Infrastructure Change
            |
            v
        OpenTofu
            |
            v
        Saved Plan
            |
            v
        Plan JSON
            |
            v
        OPA Policy
        /        \
      DENY       ALLOW
       |           |
       v           v
    Reject      Continue
    Change      Pipeline

The OpenTofu plan is treated as a security-sensitive artifact.

OPA evaluates the proposed infrastructure state rather than relying only on manual review.

## Reference Architecture

The AWS reference environment models the Project Redoubt trust zones:

- Edge
- Application
- Data
- Management
- Recovery
- Telemetry

Only the edge trust zone receives a default Internet route.

Data, management, recovery and telemetry infrastructure remain private by architectural design.

## Security Policy

Project Redoubt implements eleven Infrastructure as Code security guardrails:

- IAC-001 — Internet ingress must use HTTPS
- IAC-002 — Internet-exposed SSH is prohibited
- IAC-003 — Non-edge subnets cannot automatically assign public IP addresses
- IAC-004 — Default Internet routes are restricted to the edge zone
- IAC-005 — Security evidence storage must block public access
- IAC-006 — Security evidence storage must use KMS encryption
- IAC-007 — Security evidence versioning must remain enabled
- IAC-008 — KMS key rotation must remain enabled
- IAC-009 — VPC flow logging must capture all traffic
- IAC-010 — Security-sensitive resources require architecture metadata
- IAC-011 — Unrestricted Internet egress is prohibited

## Validation Strategy

Each guardrail is validated at three levels.

### Policy Unit Validation

Synthetic plan structures are evaluated directly against the OPA policy.

This verifies policy logic independently of the infrastructure provider.

### Real OpenTofu Plan Validation

Controlled insecure infrastructure configurations generate genuine OpenTofu plans.

Examples include:

- public HTTP
- public SSH
- public management subnet addressing
- private default Internet routes
- evidence storage protection removal
- encryption downgrade
- versioning removal
- KMS rotation removal
- incomplete flow logging
- missing security metadata
- unrestricted egress

OPA must reject each resulting plan.

### CI Enforcement

GitHub Actions performs:

1. OpenTofu formatting validation
2. provider lock validation
3. OpenTofu initialisation
4. OpenTofu configuration validation
5. reference plan generation
6. OPA policy evaluation
7. policy unit tests
8. real-plan adversarial tests
9. evidence integrity verification
10. evidence artifact publication

A policy failure causes the infrastructure security workflow to fail.

## Evidence

The CI gate generates machine-readable policy evidence containing:

- Git commit
- Git reference
- OpenTofu version
- OPA version
- OpenTofu plan SHA-256
- OPA policy SHA-256
- provider lockfile SHA-256
- policy decision
- violation count
- violation details

The evidence bundle is uploaded as a GitHub Actions artifact.

This provides traceability between:

    Source Change
        ↓
    Infrastructure Plan
        ↓
    Security Policy
        ↓
    Decision
        ↓
    Evidence

## Security Principle

Infrastructure configuration is treated as executable security architecture.

A documented architecture requirement is not considered sufficient where the requirement can reasonably be enforced automatically.

## Scope Limitations

Phase 11 is intentionally a reference architecture.

It does not claim:

- deployment into a production AWS account
- validation against live AWS state
- continuous cloud configuration drift monitoring
- production IAM architecture
- production network transit architecture
- production-grade state backend design
- hardware-backed infrastructure signing
- enterprise change-management integration

These remain implementation concerns outside the current Project Redoubt laboratory scope.

## Outcome

Phase 11 demonstrates that Project Redoubt can convert architecture requirements into version-controlled, automatically tested and CI-enforced infrastructure security controls.
