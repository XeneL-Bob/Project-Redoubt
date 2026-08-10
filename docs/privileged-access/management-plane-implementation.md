# Project Redoubt — Privileged Management Plane

## Purpose

Phase 9 converts the Project Redoubt management-plane architecture into an executable privileged-access control system.

Administrative access is separated from normal user and workload access.

## Architecture

The privileged path is:

    Dedicated Administrator Identity
                 |
                 v
          Admin OIDC Client
                 |
                 v
          Privilege Broker
                 |
                 v
        Short-Lived JIT Grant
                 |
                 v
         Management Gateway
              [PEP]
                 |
                 v
             Admin OPA
              [PDP]
                 |
                 v
          Management API
                 |
                 v
       Privileged Operation

Normal application workloads do not participate in this path.

## Administrative Identities

Phase 9 introduces dedicated privileged identities.

    ian.infrastructure
        infrastructure-admin

    sophie.security
        security-admin

These identities are separate from normal employee identities.

Administrative privilege is therefore not granted by adding privileged roles to a user's normal working identity.

## Administrative Client

Privileged authentication uses the dedicated client:

    redoubt-admin-cli

The standard Project Redoubt client:

    redoubt-test-cli

is not accepted by the management gateway.

Possession of a valid normal application token therefore does not grant access to the privileged management path.

## Management Networks

Phase 9 introduces dedicated management-plane networks:

    management_edge_net
    management_policy_net
    management_net

The protected management API exists on management_net.

Normal application gateways and Finance workloads cannot resolve or directly reach the management API.

## Policy Enforcement

The management gateway acts as the Policy Enforcement Point.

It validates:

- privileged identity token
- administrative client origin
- JIT elevation grant
- elevation grant signature
- elevation grant expiry
- elevation subject
- permitted resource
- permitted operation
- administrative device trust

Only after these checks does the gateway request an authorisation decision from Admin OPA.

## Policy Decision

Admin OPA independently evaluates:

- administrative role
- requested resource
- requested action
- trusted administrative device context
- active validated elevation state

Default policy is deny.

## Backend Protection

The management API also requires a workload-specific management gateway credential.

This prevents direct callers from bypassing the Policy Enforcement Point even if they gain network access to the management backend.

## Administrative Separation

Current administrative domains include:

    infrastructure-admin
        infrastructure-management

    security-admin
        security-management

An infrastructure administrator cannot automatically operate security-management resources.

A security administrator cannot automatically operate infrastructure-management resources.

This implements separation of administrative duties.
