# Project Redoubt — Software Supply-Chain Security

## Purpose

Phase 10 extends Project Redoubt into software build, CI/CD and release security.

The primary attack path is:

    AP-004 — Developer to Software Supply Chain

The related enterprise risk is:

    R-006 — CI/CD Supply-Chain Compromise

## Architecture

The local trusted release path is:

    Source
      |
      v
    Trusted Builder
      |
      +--> deterministic artifact
      |
      +--> SHA-256 digest
      |
      +--> provenance
      |
      v
    Dedicated Signer
      |
      +--> Ed25519 signature
      |
      v
    Independent Release Verifier
      |
      +--> signature validation
      +--> artifact digest validation
      +--> trusted builder validation
      +--> clean-source validation
      +--> source commit validation
      +--> source ref validation
      |
      v
    Release Decision

## Trust-Domain Separation

The trusted builder does not receive the release-signing private key.

The signer receives:

- release provenance
- release private key

The verifier receives:

- release artifact
- provenance
- provenance signature
- trusted public key
- release policy

The verifier does not receive the signing private key.

## Network Isolation

The builder, signer and verifier execute with:

    --network none

They do not require direct application, identity, database or Internet connectivity.

## Telemetry Architecture

Supply-chain workloads do not receive the central telemetry ingestion credential.

Instead:

    Builder / Verifier
          |
          v
    Local JSON Event Spool
          |
          v
    Supply-Chain Telemetry Relay
          |
          v
    Central Telemetry
          |
          v
    Detection Engine

This preserves build isolation while retaining security observability.

## Detection Engineering

Phase 10 introduces:

- DET-013 — Supply Chain Artifact Integrity Failure
- DET-014 — Supply Chain Provenance Signature Failure
- DET-015 — Untrusted Builder Release Attempt
- DET-016 — Dirty Source Build Attempt
- DET-017 — Unsigned Release Attempt
- DET-018 — Release Without Correlated Trusted Build

## GitHub CI/CD Controls

The Project Redoubt GitHub Actions workflow provides:

- explicit least-privilege permissions
- immutable action commit pinning
- checkout credential persistence disabled
- Gitleaks secret scanning
- CodeQL static analysis
- dependency review on pull requests
- adversarial supply-chain testing
- trusted release build
- SHA-256 release digest
- SPDX SBOM generation
- GitHub build-provenance attestation
- GitHub SBOM attestation
- controlled release-evidence artifact generation

The CI implementation does not copy the local Ed25519 release private key into GitHub Actions.

The local signing model and the GitHub attestation model intentionally represent separate trust mechanisms.

## AP-004 Adversary Validation

Phase 10 validates:

- ADV-010 — dirty-source build attempt
- ADV-011 — post-build artifact tampering
- ADV-012 — forged provenance
- ADV-013 — signed artifact from untrusted builder
- ADV-014 — unsigned release
- ADV-015 — trusted-build path bypass
- ADV-016 — signing-key access from build context

## Deployment Admission Boundary

Phase 10 implements an independent deployment approval and admission boundary.

The complete release path is:

    Source
      |
      v
    Trusted Builder
      |
      v
    Signed Provenance
      |
      v
    Release Verifier
      |
      v
    Verification Receipt
      |
      v
    Independent Release Approver
      |
      v
    Signed Short-Lived Deployment Approval
      |
      v
    Deployment Gate
      |
      v
    Deployment Record

A successful release-verifier decision is not sufficient authority to deploy.

The release approver independently validates trusted-build correlation and release evidence before issuing a deployment approval.

The deployment gate independently validates:

- deployment approval signature
- approval decision
- target environment
- approval expiry
- approved artifact digest

The deployment-approval signing private key is unavailable to the builder, release signer, verifier and deployer.

## AP-004 Status

AP-004 is:

    Substantially validated

ADV-015 demonstrates that a release-path bypass is detected and cannot progress through the independent deployment boundary.

## Residual Limitations

The laboratory does not claim full production validation.

Remaining limitations include:

- active GitHub repository ruleset enforcement
- mandatory human review enforcement
- production registry admission
- production deployment infrastructure
- hosted CI runner compromise
- enterprise change/release management integration
- realistic third-party dependency compromise
