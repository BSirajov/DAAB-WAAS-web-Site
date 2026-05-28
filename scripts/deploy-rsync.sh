#!/usr/bin/env bash
# Upload DAAB static site to production via rsync + SSH.
# Run from repository root:  ./scripts/deploy-rsync.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_FILE="$ROOT/scripts/deploy.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE — copy scripts/deploy.env.example and edit." >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

: "${DEPLOY_HOST:?Set DEPLOY_HOST in scripts/deploy.env}"
: "${DEPLOY_USER:?Set DEPLOY_USER in scripts/deploy.env}"
: "${DEPLOY_PATH:?Set DEPLOY_PATH in scripts/deploy.env}"

DEPLOY_PORT="${DEPLOY_PORT:-22}"
DEPLOY_DELETE="${DEPLOY_DELETE:-0}"
SKIP_VALIDATE="${SKIP_VALIDATE:-0}"

if [[ "$SKIP_VALIDATE" != "1" ]]; then
  echo "==> Validating site..."
  python helpers/_validate_site.py
fi

RSYNC_OPTS=(
  -avz
  --human-readable
  --progress
  --exclude-from="$ROOT/.deployignore"
)

if [[ "$DEPLOY_DELETE" == "1" ]]; then
  echo "WARNING: DEPLOY_DELETE=1 — remote files not in local tree will be removed."
  RSYNC_OPTS+=(--delete)
fi

DEST="$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/"
echo "==> Uploading to $DEST"
echo "    Exclusions: .deployignore"

rsync "${RSYNC_OPTS[@]}" \
  -e "ssh -p $DEPLOY_PORT" \
  ./ "$DEST"

echo "==> Done. Smoke-test: https://daab-waas.com/az/index.html"
