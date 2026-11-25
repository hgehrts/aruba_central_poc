#!/usr/bin/env bash
# Package aruba_central_poc into dist/aruba_central_poc-<version>.tar.gz (+ .sha256).
set -euo pipefail
cd "$(dirname "$0")/.."

APP=aruba_central_poc
VERSION="$(sed -n 's/^version = //p' "$APP/default/app.conf" | head -1)"

rm -rf dist
mkdir -p dist
COPYFILE_DISABLE=1 tar -czf "dist/${APP}-${VERSION}.tar.gz" \
  --exclude='local' --exclude='.DS_Store' "$APP"
(cd dist && shasum -a 256 "${APP}-${VERSION}.tar.gz" > "${APP}-${VERSION}.tar.gz.sha256")
ls -l dist/
