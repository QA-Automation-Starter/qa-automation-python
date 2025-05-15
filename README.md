# QA Automation for Python

[![Build](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml/badge.svg)](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml)
[![Release](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/release.yml/badge.svg)](https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/release.yml)
[![utils](https://img.shields.io/pypi/v/qa-testing-utils.svg?label=utils)](https://pypi.org/project/qa-testing-utils/)
[![commons](https://img.shields.io/pypi/v/qa-pytest-commons.svg?label=commons)](https://pypi.org/project/qa-pytest-commons/)
[![rest](https://img.shields.io/pypi/v/qa-pytest-rest.svg?label=rest)](https://pypi.org/project/qa-pytest-rest/)
[![webdriver](https://img.shields.io/pypi/v/qa-pytest-webdriver.svg?label=webdriver)](https://pypi.org/project/qa-pytest-webdriver/)


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

Open in CodeSpace or devcontainer and everything will get installed and configured,
otherwise:

0. Install Python 3.13 on your system

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

1. branch
2. commit changes
3. pull request -- will trigger a build
4. build succeeds --> tag with vX.X.X, e.g. v1.2.3 -- will trigger a release
5. verify new versions appeared on https://pypi.org/
---


## 🏗 Adding a New Package

```bash
cd qa-automation-python
pdm plugin add pdm-init  # if not already available
pdm init  # or copy an existing module like qa-testing-utils
```

Then edit `pyproject.toml` accordingly.

---


## ✅ License

This project is licensed under the Apache 2.0 License.