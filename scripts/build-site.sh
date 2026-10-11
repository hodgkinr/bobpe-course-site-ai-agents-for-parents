#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${COURSE_PACKAGE_DIR:-$(cd "$repo_root/../bobpe-course-design-ai-workforce/ai-agents-for-parents" && pwd)}"
theme="${1:-${SITE_THEME:-generic}}"
site_dir="$repo_root/site"

case "$theme" in
  generic|cu-boulder|colorado-state|minnesota-carlson) ;;
  *) echo "Theme must be generic, cu-boulder, colorado-state, or minnesota-carlson." >&2; exit 2 ;;
esac
if [[ -L "$site_dir" ]]; then
  echo "Refusing to replace a symlink at the designated site output path." >&2
  exit 2
fi
if [[ -e "$site_dir" && ! -d "$site_dir" ]]; then
  echo "Refusing to replace a non-directory at the designated site output path." >&2
  exit 2
fi
if [[ ! -x "$repo_root/.venv/bin/course-publisher" || ! -x "$repo_root/.venv/bin/course-package" ]]; then
  echo "Create .venv and install the local package-spec and publisher projects; see README.md." >&2
  exit 2
fi

stage="$(mktemp -d "${TMPDIR:-/tmp}/parents-course-site.XXXXXX")"
trap 'rm -rf "$stage"' EXIT
if [[ -n "${SITE_BASE_URL:-}" ]]; then
  "$repo_root/.venv/bin/course-publisher" build \
    --package "$package_dir" \
    --theme "$theme" \
    --output "$stage/site" \
    --site-base-url "$SITE_BASE_URL" \
    --validator "$repo_root/.venv/bin/course-package"
else
  "$repo_root/.venv/bin/course-publisher" build \
    --package "$package_dir" \
    --theme "$theme" \
    --output "$stage/site" \
    --validator "$repo_root/.venv/bin/course-package"
fi
python3 "$repo_root/scripts/annotate-recording-status.py" \
  --package "$package_dir" --site "$stage/site"

# Replace only the dedicated generated site directory after a complete successful build.
if [[ -d "$site_dir" ]]; then mv "$site_dir" "$stage/previous-site"; fi
if ! mv "$stage/site" "$site_dir"; then
  if [[ -d "$stage/previous-site" ]]; then mv "$stage/previous-site" "$site_dir"; fi
  echo "Could not install the generated site." >&2
  exit 1
fi
printf 'Site built at %s using theme %s.\n' "$site_dir" "$theme"
