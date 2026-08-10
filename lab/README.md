# Project Redoubt — Phase 5 Working Lab

Phase 5 is the first executable implementation of the Project Redoubt architecture.

## Implemented Components

| Architecture Function | Lab Component |
|---|---|
| Identity Provider | Keycloak |
| User authentication | OpenID Connect |
| Policy Decision Point | Open Policy Agent |
| Policy Enforcement Point | FastAPI gateway |
| Employee workload | Employee API |
| Restricted workload | Finance API |
| Restricted database | PostgreSQL |
| Workload-to-secret authentication | Vault AppRole |
| Secrets store | Vault KV v2 |
| Security telemetry | Central JSON telemetry collector |
| Segmentation | Docker user-defined networks |

## Access Flow

```text
User
  │
  ▼
Keycloak
  │
  │ Signed Access Token
  ▼
Policy Enforcement Gateway
  │
  ├────────> OPA
  │            │
  │      ALLOW / DENY
  │            │
  ◄────────────┘
  │
  ├────────> Employee API
  │
  └────────> Finance API
                 │
                 ├────> Vault
                 │       AppRole
                 │
                 └────> Finance DB
```

## Segmentation

The Docker Compose topology deliberately separates:

```text
edge_net
identity_net
policy_net
employee_net
finance_net
data_net
secrets_net
```

The Employee API and Finance API do not share an application network.

The telemetry collector is multi-homed onto the specific application networks that require telemetry delivery, rather than creating a shared security network between workloads.

The Finance database is only attached to the data network.

OPA is only attached to the policy network.

Vault is only attached to the secrets network.

Only the gateway and Keycloak publish host ports.

## Demonstrated Policy

### Employee

```text
alice.employee
    +
employee role
    ↓
Employee API
    =
ALLOW
```

### Employee to Finance

```text
alice.employee
    ↓
Finance API
    =
DENY
```

### Finance User from Untrusted Device

```text
carol.finance
    +
finance-reader
    +
device_trusted = false
    ↓
Finance API
    =
DENY
```

### Finance User from Trusted Device

```text
carol.finance
    +
finance-reader
    +
device_trusted = true
    ↓
Finance API
    =
ALLOW
```

## Secrets Flow

The Finance API does not receive its database password directly through Docker Compose.

Instead:

```text
Finance API
     │
     ▼
Vault AppRole
     │
     ▼
Short-Lived Vault Token
     │
     ▼
secret/finance/db
     │
     ▼
Database Credential
```

The AppRole credentials are generated at lab startup by `vault-init`.

## Telemetry

Security events are written to:

```text
evidence/runtime/security-events.jsonl
```

Runtime evidence is intentionally excluded from Git.

Later Project Redoubt phases will convert selected security events into sanitised evidence and detection artefacts.

## Development-Only Components

Keycloak uses `start-dev`.

Vault uses development server mode.

These modes are intentionally used to make the portfolio lab reproducible and disposable.

They are not representative of production deployment hardening.

## Phase 5 Limitations

The current implementation intentionally leaves several improvements for later phases:

- browser-based authentication and MFA
- explicit OAuth audience mapping
- production TLS
- mutual TLS between workloads
- SPIFFE/SPIRE workload identities
- production Vault storage/unseal architecture
- SIEM integration
- endpoint telemetry
- network IDS
- automated attack simulation

These are future implementation and validation milestones rather than hidden limitations.
