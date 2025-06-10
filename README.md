# QA Automation for Python

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

Project documentation
https://qa-automation-starter.github.io/qa-automation-python

## 🧪 Releasing

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

## 🏗 Adding a New Package

```bash
cd qa-automation-python
pdm plugin add pdm-init  # if not already available
pdm init  # or copy an existing module like qa-testing-utils
```

Then edit `pyproject.toml` accordingly.

---

<details>
<summary>TODO</summary>

- Add browser matrix support (Firefox, Safari, Edge)
- Make the BDD intro words appear in Allure report
- Extend test examples (API + UI)

</details>

---

## ✅ License

This project is licensed under the Apache 2.0 License.