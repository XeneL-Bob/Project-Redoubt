# Project Redoubt — Independent Release Approval and Deployment Gate

## Purpose

Release verification and deployment authority are intentionally separate security decisions.

A cryptographically valid software artifact must not automatically receive permission to deploy.

## Trust Model

Project Redoubt uses separate trust domains for:

    Trusted Builder
    Release Signer
    Release Verifier
    Release Approver
    Deployment Gate

No single component possesses all authority required to construct, approve and deploy software.

## Cryptographic Separation

Release provenance uses its own Ed25519 key pair.

Deployment approvals use a separate Ed25519 key pair.

The deployment approval private key exists only in the release-approval trust domain.

The deployment gate receives only the deployment approval public key.

## Deployment Approval

The independent approver validates:

- release provenance signature
- release artifact SHA-256 digest
- trusted builder identity
- verification receipt
- verification receipt digest
- verification receipt builder identity
- trusted-build correlation
- verification correlation
- permitted target environment

Successful approval produces:

    deployment-approval.json
    deployment-approval.sig

The approval is short-lived and environment-bound.

## Deployment Admission

The deployment gate validates:

- presence of deployment approval
- approval signature
- ALLOW decision
- approved environment
- approval expiry
- artifact digest

Only after every check succeeds is the artifact copied into the simulated deployment destination.

## Security Property

The architecture enforces:

    Verification != Deployment Authority

A component capable of verifying a release cannot independently authorise deployment.

A component capable of deploying a release cannot create its own valid deployment approval.

## Detection Coverage

Deployment approval rejection generates:

    DET-019 — Deployment Approval Denied

Deployment admission rejection generates:

    DET-020 — Deployment Gate Denied

A release-verifier success without correlated trusted-build evidence additionally generates:

    DET-018 — Release Without Correlated Trusted Build

## AP-004

The deployment gate closes the primary preventive gap identified by ADV-015.

The attack path is therefore classified as:

    Substantially validated

rather than fully validated because the laboratory does not implement a real production registry, production deployment environment, or enterprise release-management platform.
