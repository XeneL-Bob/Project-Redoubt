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
