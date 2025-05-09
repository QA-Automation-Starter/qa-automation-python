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
├── pyproject.toml           # Root environment definition for Hatch
└── .vscode/                 # Recommended settings for VSCode integration
```

---

## ⚙️ Requirements

- Python 3.13+ (recommended: 3.13.0 or later)
- [Hatch](https://hatch.pypa.io/latest/) (for environment management and packaging)
- [VSCode](https://code.visualstudio.com/) + Python + Pylance extensions

Install Hatch globally:
```bash
pipx install hatch
```

Or:
```bash
pip install --user hatch
```

---

## 🚀 Getting Started

From the monorepo root:

```bash
# Enter the dev environment
hatch shell

# Run tests (across submodules if configured)
hatch run test

# Format code with autopep8
hatch run format

# Run type checks
hatch run lint
```

---

## 🧪 Working Inside a Submodule

Each submodule (e.g. `qa-testing-utils/`) is a standalone Python package.
Each module has its own `pyproject.toml` and can be published independently.

---

## 🧠 VSCode Configuration

The `.vscode/settings.json` file is pre-configured to:

- Use the local Hatch environment
- Enable strict type checking (`mypy`)
- Format code with `autopep8`
- Resolve multi-package imports using `"extraPaths"`

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
hatch new my-new-package
```

Or copy the structure from an existing module like `qa-testing-utils`.

---

## 📦 Publishing to PyPI

Each module (e.g. `qa-testing-utils/`) can be published independently:

```bash
cd qa-testing-utils
hatch build
hatch publish
```

Ensure the `[project]` section in `pyproject.toml` is properly configured with name, version, authors, and dependencies.

---

## 🧹 Cleaning Up

To remove a Hatch environment:
```bash
hatch env remove default
```

To start fresh:
```bash
hatch shell
```

---

## ✅ License

This project is licensed under the Apache 2.0 License.