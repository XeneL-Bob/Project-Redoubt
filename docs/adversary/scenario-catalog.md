# Project Redoubt — Adversary Scenario Catalog

## ADV-001 — Compromised Employee Attempts Finance Access

Attack path:

    AP-001 — Phished Employee to Crown Jewel

Assumption:

The attacker already possesses a valid employee session.

Action:

Attempt access to the restricted Finance API.

Controls exercised:

- authenticated identity
- OPA authorisation
- least privilege
- Finance resource restriction
- security telemetry

Expected result:

    HTTP 403
    DET-001

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-002 — Finance Identity from Untrusted Device

Attack path:

    AP-001 — Phished Employee to Crown Jewel

Action:

Use a valid Finance identity while presenting an untrusted device context.

Controls exercised:

- contextual Zero Trust policy
- role verification
- device trust
- OPA
- DET-002

Expected result:

    HTTP 403
    DET-002


## ADV-003 — Repeated Developer Privilege Expansion

Attack path:

    AP-001 — Phished Employee to Crown Jewel

Action:

A developer repeatedly attempts access to Finance resources outside their role.

Controls exercised:

- least privilege
- default deny
- threshold detection
- DET-003

Expected result:

    403
    403
    403
    DET-003


## ADV-004 — Contractor Scope Escape

Attack path:

    AP-007 — Contractor to Internal Resource

Action:

A contractor identity attempts access beyond its approved scope.

Controls exercised:

- contractor role restriction
- explicit authorisation
- least privilege

Expected result:

    HTTP 403


## ADV-005 — Employee Workload Lateral Movement

Attack paths:

    AP-001
    AP-003

Action:

The Employee API workload attempts to resolve and reach the Finance API workload.

Control exercised:

    Docker application-zone segmentation

Expected result:

    Finance workload is not resolvable from Employee workload.


## ADV-006 — Gateway Direct Data-Tier Access

Attack path:

    AP-003 — Public Application to Database

Action:

The gateway attempts to resolve the Finance database directly.

Control exercised:

    Data-tier segmentation

Expected result:

    Finance database is not reachable from the gateway network context.


## ADV-007 — Direct Backend Access

Attack path:

    AP-003 — Public Application to Database

Action:

Attempt direct Finance API access using an invalid workload gateway credential.

Controls exercised:

- workload-specific gateway credential
- backend access enforcement
- security telemetry
- DET-006

Expected result:

    HTTP 403
    DET-006


## ADV-008 — Finance Policy-Path Bypass

Attack path:

    AP-003 — Public Application to Database

Method:

Controlled synthetic telemetry injection.

Action:

Generate a Finance application-success event without a preceding correlated gateway policy ALLOW.

Control exercised:

    DET-004 — Finance Application Policy Bypass

Expected result:

    Critical DET-004 alert

This scenario validates detection logic and does not represent exploitation of the application itself.


## ADV-009 — Secret Access Without Policy Authorisation

Attack path:

    AP-003 — Public Application to Database

Method:

Controlled synthetic telemetry injection.

Action:

Generate a Finance Vault secret-access event without a preceding correlated policy ALLOW.

Control exercised:

    DET-005 — Secret Access Without Policy Authorisation

Expected result:

    Critical DET-005 alert

This scenario validates detection logic without extracting or exposing an actual secret.


## ADV-010 — Compromised Developer Attempts Dirty-Source Build

Attack path:

    AP-004 — Developer to Software Supply Chain

Risk:

    R-006 — CI/CD Supply-Chain Compromise

Action:

A compromised developer attempts to enter locally modified or uncommitted source into the trusted build process.

Controls exercised:

- trusted builder
- clean-source policy
- supply-chain telemetry
- DET-016

Expected result:

    BUILD DENIED
    DET-016

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-011 — Post-Build Artifact Tampering

Attack path:

    AP-004 — Developer to Software Supply Chain

Action:

Modify the release artifact after the trusted build has completed.

Controls exercised:

- SHA-256 artifact digest
- signed provenance
- independent release verifier
- DET-013

Expected result:

    RELEASE DENIED
    DET-013

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-012 — Forged Release Provenance

Attack path:

    AP-004 — Developer to Software Supply Chain

Action:

Modify signed provenance after release signing in an attempt to claim a different builder identity.

Controls exercised:

- Ed25519 provenance signature
- trusted release public key
- independent verifier
- DET-014

Expected result:

    RELEASE DENIED
    DET-014

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-013 — Signed Artifact from Untrusted Builder

Attack path:

    AP-004 — Developer to Software Supply Chain

Action:

Produce an artifact using an untrusted builder identity and then sign its provenance with the valid laboratory signing authority.

Control objective:

A valid signature must not override release policy.

Controls exercised:

- required-builder policy
- signed provenance
- release verifier
- DET-015

Expected result:

    RELEASE DENIED
    DET-015

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-014 — Unsigned Release Attempt

Attack path:

    AP-004 — Developer to Software Supply Chain

Action:

Attempt release verification without the required provenance signature.

Controls exercised:

- mandatory signed provenance
- release verifier
- DET-017

Expected result:

    RELEASE DENIED
    DET-017

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-015 — Trusted-Build Path Bypass Against Deployment Boundary

Attack path:

    AP-004 — Developer to Software Supply Chain

Risk:

    R-006 — CI/CD Supply-Chain Compromise

Action:

Submit an otherwise valid signed release to the release verifier using a correlation identifier that does not match the trusted build recorded in signed provenance.

Control chain exercised:

    Release Verifier
        |
        +--> DET-018
        |
        v
    Independent Release Approver
        |
       DENY
        |
        +--> DET-019
        |
        v
    Deployment Gate
        |
       DENY
        |
        +--> DET-020

Controls exercised:

- trusted-build correlation
- signed provenance
- independent release verification
- independent deployment approval
- separate deployment approval signing key
- mandatory signed deployment approval
- deployment admission enforcement
- DET-018
- DET-019
- DET-020

Expected result:

    release anomaly detected
    deployment approval denied
    no deployment approval issued
    deployment denied

Security outcome:

    PREVENTED
    DETECTED
    CONTAINED


## ADV-016 — Signing-Key Isolation

Attack path:

    AP-004 — Developer to Software Supply Chain

Action:

A compromised trusted-build context attempts to locate the release-signing private key.

Controls exercised:

- builder/signer separation
- isolated container execution
- no signing-key mount in builder
- least privilege

Expected result:

    KEY_ISOLATED

Security outcome:

    PREVENTED
    CONTAINED
