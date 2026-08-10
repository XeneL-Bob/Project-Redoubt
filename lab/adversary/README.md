# Project Redoubt Adversary Validation

Phase 7 executes controlled adversary scenarios against the Project Redoubt laboratory.

The purpose is not exploitation for its own sake.

The objective is to validate whether documented security controls interrupt known attack paths.

## Execution

Run:

    python3 lab/adversary/runner.py

Results are written to:

    evidence/runtime/adversary-results.jsonl

Runtime evidence remains excluded from Git.

## Result Model

Each scenario can produce:

    PREVENTED
    DETECTED
    CONTAINED
    MISSED

Example:

    Attempt
       |
       v
    OPA denies request
       |
       +--> PREVENTED
       |
       v
    Security telemetry
       |
       v
    Detection rule
       |
       +--> DETECTED
       |
       v
    Sensitive resource remains inaccessible
               |
               +--> CONTAINED

## Scope

The Phase 7 runner only exercises attack paths supported by implemented laboratory components.

Scenarios requiring privileged administration, CI/CD, ransomware recovery, research systems or security-management interfaces remain deferred.
