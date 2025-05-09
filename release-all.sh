#!/bin/bash
set -e

MODULES=(
  qa-testing-utils
  qa-pytest-commons
  qa-pytest-rest
  qa-pytest-webdriver
)

for module in "${MODULES[@]}"; do
  echo "🚀 Building and publishing $module..."
  cd "$module"
  hatch build
  hatch publish
  cd ..
done
