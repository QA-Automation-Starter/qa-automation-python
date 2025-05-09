#!/bin/bash
set -e

MODULES=(
  qa-testing-utils
  qa-pytest-commons
  qa-pytest-rest
  qa-pytest-webdriver
)

for module in "${MODULES[@]}"; do
  echo "🚀 Building $module..."
  cd "$module"
  hatch build
  cd ..
done
