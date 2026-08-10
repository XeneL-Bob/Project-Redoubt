#!/bin/sh
set -eu

echo "[vault-init] Waiting for Vault..."

until vault status >/dev/null 2>&1; do
    sleep 1
done

echo "[vault-init] Vault is available."

vault auth enable approle >/dev/null 2>&1 || true

vault policy write finance-api /config/finance-api.hcl >/dev/null

vault kv put secret/finance/db \
    username="finance_app" \
    password="${FINANCE_DB_PASSWORD}" \
    host="finance-db" \
    port="5432" \
    database="finance" \
    >/dev/null

vault write auth/approle/role/finance-api \
    token_type="batch" \
    token_policies="finance-api" \
    token_ttl="15m" \
    token_max_ttl="30m" \
    secret_id_ttl="0" \
    secret_id_num_uses="0" \
    >/dev/null

ROLE_ID="$(vault read -field=role_id auth/approle/role/finance-api/role-id)"
SECRET_ID="$(vault write -field=secret_id -f auth/approle/role/finance-api/secret-id)"

umask 077

printf '%s\n' "${ROLE_ID}" > /bootstrap/finance-api-role-id
printf '%s\n' "${SECRET_ID}" > /bootstrap/finance-api-secret-id

chmod 0444 \
    /bootstrap/finance-api-role-id \
    /bootstrap/finance-api-secret-id

echo "[vault-init] Finance API AppRole provisioned."
echo "[vault-init] Finance database secret stored in Vault KV."
