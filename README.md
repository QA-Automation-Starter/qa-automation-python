# QA Automation for Python

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

1. Install PDM and UV (if not installed):
   ```bash
   pipx install pdm[all]
   pipx install uv
   pdm config --global use_uv true
   ```

2. Install dependencies:
   ```bash
   pdm install
   ```

3. Run all tests from the root:
   ```bash
   pdm run pytest
   ```

4. Clean up local build/test artifacts:
   ```bash
   pdm run clean-all
   ```

---

## 🧪 Working Inside a Submodule

Each submodule (e.g. `qa-testing-utils/`) is a standalone Python package.
Each module has its own `pyproject.toml` and can be built/published independently using PDM:

```bash
cd qa-testing-utils
pdm bump patch     # or set a specific version
pdm build
pdm publish
```

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