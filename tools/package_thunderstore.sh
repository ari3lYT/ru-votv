#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGE_VERSION="${1:-1.0.0}"
PACKAGE_NAME="Ariels_Russian_Translation"
OUT_DIR="$ROOT_DIR/dist"
BUILD_DIR="$OUT_DIR/thunderstore-$PACKAGE_NAME"
ZIP_PATH="$OUT_DIR/${PACKAGE_NAME}-${PACKAGE_VERSION}.zip"

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "[ru-votv] missing file: $path" >&2
    exit 1
  fi
}

for pak in ZZ_GameRuPatch_P.pak ZZ_EngineRuPatch_P.pak ZZ_UISettingsRuPatch_P.pak; do
  require_file "$ROOT_DIR/$pak"
done

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/pak" "$OUT_DIR"

cp "$ROOT_DIR/ZZ_GameRuPatch_P.pak" "$BUILD_DIR/pak/"
cp "$ROOT_DIR/ZZ_EngineRuPatch_P.pak" "$BUILD_DIR/pak/"
cp "$ROOT_DIR/ZZ_UISettingsRuPatch_P.pak" "$BUILD_DIR/pak/"
cp "$ROOT_DIR/README.md" "$BUILD_DIR/README.md"

{
  printf '{\n'
  printf '  "name": "%s",\n' "$PACKAGE_NAME"
  printf '  "version_number": "%s",\n' "$PACKAGE_VERSION"
  printf '  "website_url": "https://github.com/ari3lYT/ru-votv",\n'
  printf '  "description": "Russian translation for Voices of the Void 0.9.0k, based on Manual Russian Translation by Antoha256M and MrLololoshenka plus Engine/UI patches.",\n'
  printf '  "dependencies": [\n'
  printf '    "Thunderstore-unreal_shimloader-1.1.4"\n'
  printf '  ]\n'
  printf '}\n'
} > "$BUILD_DIR/manifest.json"

if [[ -f "$ROOT_DIR/icon.png" ]]; then
  cp "$ROOT_DIR/icon.png" "$BUILD_DIR/icon.png"
elif command -v convert >/dev/null 2>&1; then
  convert -size 256x256 xc:'#1b1b1b' \
    -fill '#f1f1f1' -gravity center -font DejaVu-Sans-Bold -pointsize 68 \
    -annotate +0-18 'RU' \
    -fill '#8fd3ff' -gravity center -font DejaVu-Sans -pointsize 20 \
    -annotate +0+58 'VotV 0.9.0k' \
    "$BUILD_DIR/icon.png"
else
  echo "[ru-votv] ImageMagick convert is required to create icon.png" >&2
  exit 1
fi

rm -f "$ZIP_PATH"
(
  cd "$BUILD_DIR"
  zip -qr "$ZIP_PATH" manifest.json README.md icon.png pak
)

echo "[ru-votv] built $ZIP_PATH"
