#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_DEST="${HERMES_HOME:-$HOME/.hermes}/skills/hermes-loop-master"
if [[ -d "${HERMES_HOME:-$HOME/.hermes}/skills/software-development" ]]; then
  DEFAULT_DEST="${HERMES_HOME:-$HOME/.hermes}/skills/software-development/hermes-loop-master"
fi

DEST="$DEFAULT_DEST"
FORCE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: bash install.sh [--target DIR] [--dry-run] [--force]

  --target DIR  Install into this exact skill directory.
  --dry-run     Validate sources and print the plan without writing.
  --force       Replace a recognized existing install with backup + rollback.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "--target requires a directory" >&2; exit 2; }
      DEST="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

# Normalize trailing separators before sibling staging/backup paths are derived.
while [[ "$DEST" != "/" && "$DEST" == */ ]]; do DEST="${DEST%/}"; done
[[ -n "$DEST" && "$DEST" != "/" && "$DEST" != "$HOME" ]] || {
  echo "Refusing unsafe install target: $DEST" >&2; exit 2;
}

for required in SKILL.md templates scripts examples references; do
  [[ -e "$ROOT/$required" ]] || { echo "Missing source: $ROOT/$required" >&2; exit 1; }
done
python3 "$ROOT/scripts/validate_skill.py" "$ROOT/SKILL.md" >/dev/null

recognized_install() {
  [[ -d "$1" && ! -L "$1" && -f "$1/SKILL.md" ]] || return 1
  grep -Eq '^name:[[:space:]]*hermes-loop-master[[:space:]]*$' "$1/SKILL.md"
}

if [[ -e "$DEST" || -L "$DEST" ]]; then
  if [[ "$FORCE" -ne 1 ]]; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      echo "Destination exists; a real install would require --force."
    else
      echo "Destination already exists: $DEST" >&2
      echo "Re-run with --force to back up and replace a recognized installation." >&2
      exit 1
    fi
  elif ! recognized_install "$DEST"; then
    echo "Refusing --force: target is not a Hermes Loop Master installation: $DEST" >&2
    exit 1
  fi
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run: validated $ROOT/SKILL.md"
  echo "Would install SKILL.md, templates/, scripts/, examples/, and references/ to: $DEST"
  exit 0
fi

mkdir -p "$(dirname "$DEST")"
STAGING="${DEST}.tmp.$$"
BACKUP=""
INSTALLED=0
cleanup() {
  rc=$?
  [[ ! -e "$STAGING" ]] || rm -rf "$STAGING"
  if [[ "$rc" -ne 0 && "$INSTALLED" -eq 0 && -n "$BACKUP" && -e "$BACKUP" && ! -e "$DEST" ]]; then
    mv "$BACKUP" "$DEST" || true
  fi
  exit "$rc"
}
trap cleanup EXIT

mkdir -p "$STAGING"
cp "$ROOT/SKILL.md" "$STAGING/SKILL.md"
for directory in templates scripts examples references; do
  cp -R "$ROOT/$directory" "$STAGING/$directory"
done
python3 "$STAGING/scripts/validate_skill.py" "$STAGING/SKILL.md" >/dev/null

if [[ -e "$DEST" ]]; then
  BACKUP="${DEST}.backup.$(date +%Y%m%d_%H%M%S)"
  mv "$DEST" "$BACKUP"
fi
mv "$STAGING" "$DEST"
INSTALLED=1
trap - EXIT

echo "Installed Hermes Loop Master to: $DEST"
if [[ -n "$BACKUP" ]]; then
  echo "Previous install backed up to: $BACKUP"
fi
echo "Restart Hermes Agent or open a new session if the skill list is cached."
