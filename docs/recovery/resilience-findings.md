# Project Redoubt — Resilience Findings

## RF-001 — Vault AppRole SecretID Lifecycle

### Finding

During repeated Phase 8 validation, the Finance API began returning HTTP 503 for otherwise valid trusted Finance requests.

The application path remained authorised, but the Finance API could no longer retrieve its database credential from Vault.

### Root Cause

The Finance workload used a Vault AppRole SecretID configured with a thirty-minute TTL.

The Finance API performs a new AppRole login when retrieving its database secret.

After the SecretID expired, new Vault authentication attempts failed.

### Impact

The failure produced an availability issue:

    Valid Finance Request
           |
           v
       OPA ALLOW
           |
           v
      Finance API
           |
           v
       Vault Login
           |
           X
        SecretID expired
           |
           v
        HTTP 503

This was a credential-lifecycle resilience failure rather than an authorisation failure.

### Laboratory Remediation

For the persistent local Project Redoubt laboratory:

    secret_id_ttl = 0

The SecretID remains valid for the lifetime of the lab.

Vault access tokens remain short-lived:

    token_ttl = 15m
    token_max_ttl = 30m

### Production Interpretation

A non-expiring SecretID is not the preferred production architecture.

A production implementation should use an appropriate mechanism such as:

- automated SecretID rotation
- platform workload identity
- short-lived machine credentials
- Vault Agent
- Kubernetes authentication
- cloud-native workload federation

The Phase 8 configuration is therefore an explicit laboratory availability tradeoff rather than a production credential-management recommendation.

## RF-002 — Recovery Store Trust Boundary

The recovery database receives the backup store as read-only.

The backup agent requires write access so that controlled backups can be created.

This demonstrates separation between production workloads and recovery consumption, but it is not equivalent to immutable backup infrastructure.

Future hardening should introduce an independently administered immutable or object-locked recovery tier.
