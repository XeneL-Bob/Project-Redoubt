#!/bin/sh

set -eu

: "${FINANCE_DB_PASSWORD:?FINANCE_DB_PASSWORD is required}"

BACKUP_FILE="${BACKUP_FILE:-/recovery/finance.sql}"
TEMP_FILE="${BACKUP_FILE}.tmp"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

echo "[INFO] Creating Finance database recovery copy"

rm -f \
    "${TEMP_FILE}" \
    "${CHECKSUM_FILE}"

PGPASSWORD="${FINANCE_DB_PASSWORD}" \
pg_dump \
    -h finance-db \
    -U finance_app \
    -d finance \
    --clean \
    --if-exists \
    --no-owner \
    --no-privileges \
    > "${TEMP_FILE}"

mv -f \
    "${TEMP_FILE}" \
    "${BACKUP_FILE}"

sha256sum "${BACKUP_FILE}" \
    | awk '{print $1}' \
    > "${CHECKSUM_FILE}"

chmod 0444 \
    "${BACKUP_FILE}" \
    "${CHECKSUM_FILE}"

echo "[PASS] Recovery copy created"

echo -n "[INFO] SHA-256: "
cat "${CHECKSUM_FILE}"
