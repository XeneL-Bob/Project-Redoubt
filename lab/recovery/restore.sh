#!/bin/sh

set -eu

BACKUP_FILE="${BACKUP_FILE:-/recovery/finance.sql}"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"

if [ ! -s "${BACKUP_FILE}" ]; then
    echo "[FAIL] Recovery backup does not exist"
    exit 1
fi

if [ ! -s "${CHECKSUM_FILE}" ]; then
    echo "[FAIL] Recovery checksum does not exist"
    exit 1
fi

EXPECTED="$(
    cat "${CHECKSUM_FILE}"
)"

ACTUAL="$(
    sha256sum "${BACKUP_FILE}" \
        | awk '{print $1}'
)"

if [ "${EXPECTED}" != "${ACTUAL}" ]; then
    echo "[FAIL] Recovery backup integrity validation failed"
    echo "Expected: ${EXPECTED}"
    echo "Actual:   ${ACTUAL}"
    exit 1
fi

echo "[PASS] Recovery backup integrity verified"

export PGPASSWORD="${POSTGRES_PASSWORD}"

psql \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -v ON_ERROR_STOP=1 \
    -f "${BACKUP_FILE}" \
    >/tmp/redoubt-restore.log

echo "[PASS] Finance recovery copy restored"
