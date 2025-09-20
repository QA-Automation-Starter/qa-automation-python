# Getting Started

Open in Codespace or Dev Container and everything will get installed and configured, otherwise:

0. Install Python 3.13 on your system

1. Install [PDM](https://pdm-project.org):
   ```bash
   pipx install pdm[all]
   ```

2. Generate from template:
   ```bash
   cookiecutter gh:QA-Automation-Starter/qa-automation-python
   ```
   
   or
   
   Fork/Clone [demo project](https://github.com/QA-Automation-Starter/qa-automation-python-demo), e.g.:
   ```bash
   git clone https://github.com/QA-Automation-Starter/qa-automation-python-demo.git
   ```

3. Install dependencies:
   ```bash
   pdm run install-all
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



Customize for your needs :)

---
