# Getting Started

Open in Codespace or Dev Container and everything will get installed and configured, otherwise:

0. Install Python 3.13 on your system

1. Install [PDM](https://pdm-project.org):
   ```bash
   pipx install pdm[all]
   ```

2. Generate from template:
    - via [cookiecutter](https://github.com/cookiecutter/cookiecutter?tab=readme-ov-file#installation)
    ```bash
    cookiecutter gh:QA-Automation-Starter/qa-automation-python
    ```
    - or fork/clone [demo project](https://github.com/QA-Automation-Starter/qa-automation-python-demo)
    ```bash
    git clone https://github.com/QA-Automation-Starter/qa-automation-python-demo.git
    ```

3. Install dependencies:
   ```bash
   pdm run install-all
   ```
   
   For Playwright tests, also run:
   ```bash
   pdm run playwright-install
   ```

4. Run all tests from the root:
   ```bash
   pdm run pytest
   ```
   pytest html report is in `report.html`
   > NOTE: Selenium tests require Google Chrome installed.

5. Optional: Generate Allure reports
    ```bash
    pdm run allure-generate
    ```
    then open, `docs/reports/index.html` in a browser.
    
    > NOTE: requires installation of [Allure server](https://docs.qameta.io/allure/)

---

## Available PDM Scripts

The project includes several convenience scripts in `pyproject.toml`:

| Script | Description |
|--------|-------------|
| `pdm run install-all` | Installs all dependencies for the monorepo and sub-packages |
| `pdm run playwright-install` | Installs Playwright browsers (Chrome, Firefox, WebKit) |
| `pdm run clean-all` | Removes all generated files (`.pyc`, `__pycache__`, build artifacts) |
| `pdm run format-all` | Formats all code with `isort` and `autopep8` |
| `pdm run build-all` | Builds all sub-packages |
| `pdm run publish-all` | Publishes all sub-packages to PyPI |
| `pdm run allure-generate` | Generates Allure HTML report from test results |
| `pdm run mkdocs-serve` | Starts local documentation server at http://localhost:8000 |

---

Customize for your needs :)

---
