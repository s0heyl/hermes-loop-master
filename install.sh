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
  --force       Replace an existing install after creating a timestamped backup.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "--target requires a directory" >&2; exit 2; }
      DEST="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for required in SKILL.md templates scripts examples references; do
  [[ -e "$ROOT/$required" ]] || { echo "Missing source: $ROOT/$required" >&2; exit 1; }
done
python3 "$ROOT/scripts/validate_skill.py" "$ROOT/SKILL.md" >/dev/null

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run: validated $ROOT/SKILL.md"
  echo "Would install SKILL.md, templates/, scripts/, examples/, and references/ to: $DEST"
  if [[ -e "$DEST" && "$FORCE" -ne 1 ]]; then
    echo "Destination exists; a real install would require --force."
  fi
  exit 0
fi

if [[ -e "$DEST" && "$FORCE" -ne 1 ]]; then
  echo "Destination already exists: $DEST" >&2
  echo "Re-run with --force to create a backup and replace it." >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
STAGING="${DEST}.tmp.$$"
BACKUP=""
cleanup() {
  [[ ! -e "$STAGING" ]] || rm -rf "$STAGING"
}
trap cleanup EXIT
mkdir -p "$STAGING"
cp "$ROOT/SKILL.md" "$STAGING/SKILL.md"
cp -R "$ROOT/templates" "$STAGING/templates"
cp -R "$ROOT/scripts" "$STAGING/scripts"
cp -R "$ROOT/examples" "$STAGING/examples"
cp -R "$ROOT/references" "$STAGING/references"
python3 "$STAGING/scripts/validate_skill.py" "$STAGING/SKILL.md" >/dev/null

if [[ -e "$DEST" ]]; then
  BACKUP="${DEST}.backup.$(date +%Y%m%d_%H%M%S)"
  mv "$DEST" "$BACKUP"
fi
mv "$STAGING" "$DEST"
trap - EXIT

echo "Installed Hermes Loop Master to: $DEST"
if [[ -n "$BACKUP" ]]; then
  echo "Previous install backed up to: $BACKUP"
fi
echo "Restart Hermes Agent or open a new session if the skill list is cached."
