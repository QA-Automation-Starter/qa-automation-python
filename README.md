# QA Automation for Python

[![Build](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml/badge.svg)](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml)
![Release](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/release.yml)
[![PyPI version](https://img.shields.io/pypi/v/qa-testing-utils.svg)](https://pypi.org/project/qa-testing-utils/)
[![PyPI version](https://img.shields.io/pypi/v/qa-pytest-commons.svg)](https://pypi.org/project/qa-pytest-commons/)
[![PyPI version](https://img.shields.io/pypi/v/qa-pytest-rest.svg)](https://pypi.org/project/qa-pytest-rest/)
[![PyPI version](https://img.shields.io/pypi/v/qa-pytest-webdriver.svg)](https://pypi.org/project/qa-pytest-webdriver/)


This monorepo contains modular, reusable Python packages for building structured, maintainable, BDD-style automated tests using `pytest`, `Hamcrest`, and related tooling.
It is designed to support test automation for diverse technologies like REST APIs, web UI (Selenium), messaging (RabbitMQ), and more.

---

## 📦 Project Structure

```
qa-automation-python/
├── qa-testing-utils/        # Shared low-level utility functions
├── qa-pytest-commons/       # Technology-agnostic test infrastructure
├── qa-pytest-rest/          # REST-specific steps and config
├── qa-pytest-webdriver/     # Selenium-specific implementation
├── qa-pytest-template/      # Cookiecutter project template
├── qa-pytest-examples/      # Usage examples for application test projects
├── pyproject.toml           # Root environment definition for PDM
└── .vscode/                 # Recommended settings for VSCode integration
```

---

## 🚀 Quick Start (Locally with [PDM](https://pdm-project.org))

> ⚠️ Requires Python 3.13 installed on your system.

1. Install PDM:
   ```bash
   pipx install pdm[all]
   ```

2. Install dependencies:
   ```bash
   pdm install
   ```

3. Run all tests from the root:
   ```bash
   pdm run pytest
   ```
---

## 🧪 Releasing

0. Ensure PyPi username and token are in the environment:
   ```bash
   env | grep PDM
   ```
   Should yield something like:
   ```
   PDM_PUBLISH_USERNAME=__token__
   PDM_PUBLISH_PASSWORD=...
   ```

1. Clean up local build/test artifacts:
   ```bash
   pdm run clean-all
   ```

2. Commit and create a tag for this version:
   ```bash
   git commit -m "release X.X.X"
   git tag vX.X.X
   git push
   ```

3. Build all and publish:
   ```bash
   pdm run build-all
   pdm run publish-all
   ```

 4. Verify new versions appeared on https://pypi.org/
---

## 🧠 VSCode Configuration

The `.vscode/settings.json` file is pre-configured to:

- Use `.venv` with PDM
- Enable strict type checking (Pylance)
- Format code with `autopep8`
- Resolve multi-package imports using `"python.analysis.extraPaths"`

### 🔧 VSCode Setup (if needed)

Install recommended extensions:

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)

Then reload the window:
```
Ctrl+Shift+P → Reload Window
```

---

## 🏗 Adding a New Package

```bash
cd qa-automation-python
pdm plugin add pdm-init  # if not already available
pdm init  # or copy an existing module like qa-testing-utils
```

Then edit `pyproject.toml` accordingly.

---

## 📦 Publishing to PyPI

Each module can be published separately:

```bash
cd qa-pytest-commons
pdm bump patch
pdm build
pdm publish
```

You can also define a centralized `release-all` script in the root `pyproject.toml` to version and publish all modules at once.

---

## ✅ License

This project is licensed under the Apache 2.0 License.