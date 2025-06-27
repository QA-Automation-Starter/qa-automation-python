# QA Automation Starter for Python

<p align="center">
    <!-- Build and Release -->
    <a href="https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml">
        <img alt="Build" src="https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/build.yml/badge.svg">
    </a>
    <a href="https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/release.yml">
        <img alt="Release" src="https://github.com/QA-Automation-Starter/qa-automation-python/actions/workflows/release.yml/badge.svg">
    </a>
    <br>
    <!-- Published Packages -->
    <a href="https://pypi.org/project/qa-testing-utils/">
        <img alt="utils" src="https://img.shields.io/pypi/v/qa-testing-utils.svg?label=utils">
    </a>
    <a href="https://pypi.org/project/qa-pytest-commons/">
        <img alt="commons" src="https://img.shields.io/pypi/v/qa-pytest-commons.svg?label=commons">
    </a>
    <a href="https://pypi.org/project/qa-pytest-rest/">
        <img alt="rest" src="https://img.shields.io/pypi/v/qa-pytest-rest.svg?label=rest">
    </a>
    <a href="https://pypi.org/project/qa-pytest-webdriver/">
        <img alt="webdriver" src="https://img.shields.io/pypi/v/qa-pytest-webdriver.svg?label=webdriver">
    </a>
    <br>
    <!-- License -->
    <a href="LICENSE">
        <img alt="License: Apache 2.0" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
    </a>
    <br>
    <!-- Codespaces / Dev Container -->
    <a href="https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=QA-Automation-Starter%2Fqa-automation-python">
        <img alt="Open in GitHub Codespaces" src="https://img.shields.io/badge/Open%20in-GitHub%20Codespaces-blue?logo=github">
    </a>
    <a href="https://vscode.dev/github/QA-Automation-Starter/qa-automation-python">
        <img alt="Open in Dev Container" src="https://img.shields.io/badge/Open%20in-Dev%20Container-blue?logo=visualstudiocode">
    </a>
    <!-- Test Report -->
    <a href="https://qa-automation-starter.github.io/qa-automation-python/reports/index.html">
        <img alt="Allure Report" src="https://img.shields.io/badge/Test%20Report-Allure-blueviolet">
    </a>

</p>

User documentation
https://python.qa-automation-starter.github.io

# Getting Started

Open in Codespace or Dev Container and everything will get installed and configured, otherwise:

0. Install Python 3.13 on your system

1. Install [PDM](https://pdm-project.org):
   ```bash
   pipx install pdm[all]
   ```

2. Install dependencies:
   ```bash
   pdm run install-all
   ```
   > NOTE: This must be run whenever new dependencies, or versions are changed.

3. Run all tests from the root:
   ```bash
   pdm run pytest
   ```

4. Generate Allure reports
    ```bash
    pdm run allure-generate
    ```

5. Serve MkDocs site
    ```bash
    pdm run mkdocs-serve
    ```
    then open http://127.0.0.1:8000/qa-automation-python in a browser

---

# Project Structure

```
qa-automation-python/
├── qa-testing-utils/        # Shared low-level utility functions
├── qa-pytest-commons/       # Technology-agnostic test infrastructure
├── qa-pytest-rest/          # REST-specific steps and config
├── qa-pytest-webdriver/     # Selenium-specific implementation
├── qa-pytest-template/      # TBD: Cookiecutter project template
├── qa-pytest-examples/      # Usage examples for application test projects
├── pyproject.toml           # Root environment definition for PDM
└── .vscode/                 # Recommended settings for VSCode integration
```

---

# Releasing

1. branch
2. commit changes
3. pull request -- will trigger a build
4. build succeeds --> tag with vX.X.X, e.g. v1.2.3 -- will trigger a release:

    4.1. ensure you are on main and up-to-date
    
    4.2. verify which tags exists in local repo
    ```bash
    git tag
    ```
    4.3. create new tag, e.g. `v0.0.8`
    ```bash
    git tag v0.0.8
    ```
    4.4. push it
    ```bash
    git push origin v0.0.8
    ```

5. verify new versions appeared on https://pypi.org/

---

# Adding Exportable Symbols

Whenever adding a new global symbol (class/method/constant), these might need
to be exported, thus listed in the `__init__.py` of the respective module.

Can be done automatically with `mkinit`:
```bash
pdm run regenerate-init
```

# Formatting and Sorting Imports

Before committing:
```bash
pdm run format-all
```

# Adding a New Package

```bash
cd qa-automation-python
pdm plugin add pdm-init  # if not already available
pdm init  # or copy an existing module like qa-testing-utils
```

Then edit `pyproject.toml` accordingly.

---

# License

This project is licensed under the Apache 2.0 License.
