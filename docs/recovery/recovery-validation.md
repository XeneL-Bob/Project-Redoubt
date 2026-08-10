# Project Redoubt — Recovery Validation

## Purpose

Phase 8 validates the recovery architecture implemented for Project Redoubt.

The objective is to prove that a known-good copy of Finance data can survive a change to the production state and be restored independently.

## Recovery Flow

    Finance Production Database
              |
              | controlled backup
              v
         Backup Agent
              |
              v
      Recovery Data Store
              |
              | read-only
              v
       Isolated Recovery DB
              |
              v
      Integrity Verification
              |
              v
        Trusted Restore

## Recovery Isolation

The recovery database is attached only to the dedicated internal recovery network.

Normal production components are not members of that network.

Validated production components include:

- Policy Enforcement Gateway
- Employee API
- Finance API
- Finance database

The Finance workload is unable to resolve the recovery database.

## Backup Integrity

Each Finance backup produces:

    finance.sql
    finance.sql.sha256

Before restoration, the restore workflow calculates the SHA-256 digest of the backup and compares it with the stored digest.

Restoration stops if integrity validation fails.

## Recovery Test

Phase 8 performs the following controlled sequence:

1. Write a known-good marker into the Finance database.
2. Create a protected recovery copy.
3. Calculate and store the backup SHA-256 digest.
4. Modify the production marker after backup.
5. Verify that production now differs from the recovery point.
6. Validate backup integrity.
7. Restore the recovery copy into the isolated recovery database.
8. Verify that the restored marker matches the original known-good value.
9. Verify that the production database remains independently modified.

This proves that validation is occurring against an independent recovery state rather than simply reading the production database.

## AP-005 Coverage

Phase 8 partially validates:

    AP-005 — Ransomware to Recovery Infrastructure

Validated properties include:

- independent recovery network
- production-to-recovery network separation
- protected recovery data path
- backup integrity verification
- recovery after simulated production corruption
- independent restore validation

Not yet validated:

- immutable or object-locked backups
- offline backup media
- backup-administrator compromise
- destructive production-wide ransomware
- identity-plane recovery
- infrastructure reconstruction
- disaster recovery across independent physical or cloud environments

Project Redoubt therefore records AP-005 as partially validated rather than fully validated.
