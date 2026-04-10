#!/usr/bin/env bash
# GrowthOS Rollback — One-command rollback to previous state
# Usage: ./rollback.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/deploy.sh" --rollback
