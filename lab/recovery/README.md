# Project Redoubt Recovery Plane

Phase 8 implements a controlled Finance backup and isolated restore workflow.

Components:

- backup-agent
- protected recovery_store volume
- SHA-256 integrity manifest
- isolated recovery-db
- dedicated internal recovery_net
- integrity-checked restore utility

Create a backup:

    docker compose --env-file lab/.env -f lab/compose.yaml exec -T backup-agent /usr/local/bin/redoubt-backup

Restore into the isolated recovery database:

    docker compose --env-file lab/.env -f lab/compose.yaml exec -T recovery-db /usr/local/bin/redoubt-restore

Production workloads do not have membership in recovery_net.

The recovery_store is mounted read-only by recovery-db.
