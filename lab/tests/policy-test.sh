#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker run --rm \
    -v "${LAB_DIR}/policy:/policy:ro" \
    openpolicyagent/opa:1.17.0 \
    test /policy -v
