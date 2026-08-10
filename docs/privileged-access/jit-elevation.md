# Project Redoubt — Just-in-Time Privileged Elevation

## Purpose

Administrative identity alone is insufficient to access the Project Redoubt management plane.

Phase 9 requires a separately issued short-lived elevation grant.

## Elevation Flow

    Administrator
         |
         v
    Authenticate
         |
         v
    Privilege Broker
         |
         +-- verify admin client
         +-- verify eligible role
         +-- verify trusted admin device
         |
         v
    Signed Elevation Grant
         |
         v
    Management Gateway
         |
         +-- verify signature
         +-- verify issuer
         +-- verify audience
         +-- verify expiry
         +-- verify subject
         +-- verify resource
         +-- verify action
         |
         v
      Admin OPA

## Grant Properties

Elevation grants contain:

- subject
- unique grant identifier
- issue time
- not-before time
- expiry time
- administrative domain
- allowed resource
- allowed actions
- trusted-device state

The grant is signed by the privilege broker.

## Lifetime

The laboratory enforces a maximum elevation duration of:

    120 seconds

Automated tests also verify that expired grants are rejected.

The short duration is intentionally aggressive because Project Redoubt is a security-control laboratory.

## Domain Scoping

An infrastructure elevation grant cannot be used against the security-management domain.

A security elevation grant cannot be used against infrastructure-management resources.

## Subject Binding

An elevation grant is bound to the identity for which it was issued.

A grant cannot be transferred to another authenticated administrator.

## Device Context

A trusted administrative device is required both when elevation is issued and when privileged access is performed.

A previously issued grant therefore does not remove the requirement for current management-plane device posture.

## Security Benefit

The elevation mechanism reduces the value of a compromised privileged password.

A compromised administrative credential does not by itself provide an active privileged management session.

Additional controls must still be satisfied before administrative operations are permitted.

## Laboratory Limitation

The current laboratory uses a shared symmetric key between the privilege broker and management gateway for elevation-grant signing and verification.

A production architecture should prefer asymmetric signing or a dedicated workload-identity mechanism so that the verifying component does not also possess the signing key.
