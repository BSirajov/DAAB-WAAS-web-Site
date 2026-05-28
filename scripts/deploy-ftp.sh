#!/usr/bin/env bash
# Upload DAAB static site via FTP mirror (lftp).
# Run from repository root:  ./scripts/deploy-ftp.sh
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

: "${FTP_HOST:?Set FTP_HOST in scripts/deploy.env}"
: "${FTP_USER:?Set FTP_USER in scripts/deploy.env}"
: "${FTP_PASS:?Set FTP_PASS in scripts/deploy.env}"

FTP_PATH="${FTP_PATH:-/public_html}"
FTP_PORT="${FTP_PORT:-21}"
SKIP_VALIDATE="${SKIP_VALIDATE:-0}"

if ! command -v lftp >/dev/null 2>&1; then
  echo "lftp not found. Install: https://lftp.yar.ru/ (or apt install lftp / choco install lftp)" >&2
  exit 1
fi

if [[ "$SKIP_VALIDATE" != "1" ]]; then
  echo "==> Validating site..."
  python helpers/_validate_site.py
fi

echo "==> FTP mirror to $FTP_HOST:$FTP_PATH"

lftp -c "
set cmd:fail-exit true
set net:timeout 30
open -u $FTP_USER,$FTP_PASS -p $FTP_PORT $FTP_HOST
lcd $ROOT
cd $FTP_PATH
mirror -R --verbose --parallel=4 \
  --exclude-glob helpers/** \
  --exclude-glob documents/** \
  --exclude-glob sources/** \
  --exclude-glob templates/** \
  --exclude-glob data/** \
  --exclude-glob node_modules/** \
  --exclude-glob _archive/** \
  --exclude-glob cv/** \
  --exclude-glob az/application/** \
  --exclude-glob en/application/** \
  --exclude-glob .git/** \
  --exclude-glob .cursor/** \
  --exclude-glob .vscode/** \
  --exclude-glob scripts/** \
  --exclude-glob '*.py' \
  --exclude-glob '*.md' \
  --exclude-glob forum_2024/*.docx \
  --exclude-glob 'forum_2024/~\$*' \
  --exclude-glob forum_2024/*.jpg \
  --exclude-glob forum_2024/*.jpeg \
  --exclude-glob images/flags/**
.
bye
"

echo "==> Done. Smoke-test: https://daab-waas.com/az/index.html"
