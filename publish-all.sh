#!/bin/bash
set -euo pipefail

MODULES=(
  qa-testing-utils
  qa-pytest-commons
  qa-pytest-rest
  qa-pytest-webdriver
  qa-pytest-examples
)

for module in "${MODULES[@]}"; do
  echo "🚀 Publishing $module..."
  cd "$module"

  if compgen -G "dist/*" > /dev/null; then
    python3 -m twine upload dist/* -u __token__ -p "$HATCH_INDEX_AUTH__PYPI"
  else
    echo "⚠️  No dist files found in $module — skipping."
  fi

  cd ..
done
