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
</p>

**Modular Python packages for maintainable, BDD-style automated tests with [`pytest`](https://docs.pytest.org/), [`Hamcrest`](https://hamcrest.org/), [`Allure`](https://docs.qameta.io/allure/) reporting, and configurable logging.**

Technology-agnostic; example REST and Selenium implementations included.

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

##   Architecture

> Support for additional technologies, e.g. RabbitMQ, can be added by sub-classing these classes and adding specific steps, setup/teardown, and configuration. This allows reusing the basic configuration, reporting, logging, and retrying mechanisms. Further, application tests, steps, and configurations reuse by subclassing from technologies.

```mermaid
flowchart TD
    A[Tests: Define BDD scenarios as series of steps, also define specific setup and teardown] --> |contains| B[Steps: encapsulate UI or API operations and verifications, and may be composed of other steps]
    B --> |contains| C[Configurations: can be per environment, such as dev, qa, staging, and contain URLs, users, authentication schemes, encryption, etc.]
    B --> |uses| D[Matchers: Hamcrest matchers for single objects or for iterables]
    A --> |contains| C
    B --> |uses| E[Models: domain objects]

    subgraph Inheritance
        A1[GenericTests] -.-> |inherits| A2[Tests]
        B1[GenericSteps] -.-> |inherits| B2[Steps]
        C1[AbstractConfiguration] -.-> |inherits| C2[Configuration]
    end
```

---

### Extending the Framework

> To add support for a new technology (e.g., messaging, database), create:
> - `MyTechConfiguration(BaseConfiguration)`
> - `MyTechSteps(GenericSteps[MyTechConfiguration])`
> - `MyTechTests(AbstractTestsBase[MyTechSteps, MyTechConfiguration])`
> This pattern ensures you reuse the core BDD, configuration, and reporting mechanisms.

```mermaid
classDiagram
    %% Core Abstractions
    class AbstractTestsBase {
        <<abstract>>
        +steps
        +_configuration
        +setup_method()
        +teardown_method()
    }
    class GenericSteps {
        <<abstract>>
        +given
        +when
        +then
        +and_
        +with_
        +retrying()
        +eventually_assert_that()
    }
    class BaseConfiguration {
        <<abstract>>
        +parser
    }

    %% Technology-Specific Extensions
    class RestTests
    class RestSteps
    class RestConfiguration

    class SeleniumTests
    class SeleniumSteps
    class SeleniumConfiguration

    %% Example: Custom Extension
    class TerminalXTests
    class TerminalXSteps
    class TerminalXConfiguration

    %% Relationships
    AbstractTestsBase <|-- RestTests
    AbstractTestsBase <|-- SeleniumTests
    SeleniumTests <|-- TerminalXTests

    GenericSteps <|-- RestSteps
    GenericSteps <|-- SeleniumSteps
    SeleniumSteps <|-- TerminalXSteps

    BaseConfiguration <|-- RestConfiguration
    BaseConfiguration <|-- SeleniumConfiguration
    SeleniumConfiguration <|-- TerminalXConfiguration

    RestTests o-- RestSteps : uses
    RestTests o-- RestConfiguration : configures

    SeleniumTests o-- SeleniumSteps : uses
    SeleniumTests o-- SeleniumConfiguration : configures

    TerminalXTests o-- TerminalXSteps : uses
    TerminalXTests o-- TerminalXConfiguration : configures

    %% Example extension note
    %% You can add new technologies by subclassing the three core abstractions:
    %% AbstractTestsBase, GenericSteps, and BaseConfiguration.
```

**Key Classes (with links to source code):**

| Class | Description | Source |
|-------|-------------|--------|
| `AbstractTestsBase` | Base for all test scenarios; holds steps and config | [abstract_tests_base.py](qa-pytest-commons/src/qa_pytest_commons/abstract_tests_base.py) |
| `GenericSteps` | Base for all step implementations; provides BDD keywords | [generic_steps.py](qa-pytest-commons/src/qa_pytest_commons/generic_steps.py) |
| `BaseConfiguration` | Base for all configuration objects | [base_configuration.py](qa-pytest-commons/src/qa_pytest_commons/base_configuration.py) |
| `RestTests` | REST-specific test base | [rest_tests.py](qa-pytest-rest/src/qa_pytest_rest/rest_tests.py) |
| `RestSteps` | REST-specific steps | [rest_steps.py](qa-pytest-rest/src/qa_pytest_rest/rest_steps.py) |
| `RestConfiguration` | REST-specific configuration | [rest_configuration.py](qa-pytest-rest/src/qa_pytest_rest/rest_configuration.py) |
| `SeleniumTests` | Selenium-specific test base | [selenium_tests.py](qa-pytest-webdriver/src/qa_pytest_webdriver/selenium_tests.py) |
| `SeleniumSteps` | Selenium-specific steps | [selenium_steps.py](qa-pytest-webdriver/src/qa_pytest_webdriver/selenium_steps.py) |
| `SeleniumConfiguration` | Selenium-specific configuration | [selenium_configuration.py](qa-pytest-webdriver/src/qa_pytest_webdriver/selenium_configuration.py) |
| `TerminalXTests` | Example: custom UI test base | [terminalx_tests.py](qa-pytest-examples/src/qa_pytest_examples/terminalx_tests.py) |
| `TerminalXSteps` | Example: custom UI steps | [terminalx_steps.py](qa-pytest-examples/src/qa_pytest_examples/terminalx_steps.py) |
| `TerminalXConfiguration` | Example: custom UI configuration | [terminalx_configuration.py](qa-pytest-examples/src/qa_pytest_examples/terminalx_configuration.py) |

---

## 🚀 Quick Start (Locally with [PDM](https://pdm-project.org))

Open in Codespace or Dev Container and everything will get installed and configured, otherwise:

0. Install Python 3.13 on your system

1. Install [PDM](https://pdm-project.org):
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

## Reports

1. `report.html` is generated in the root folder; just open it in a browser
2. `allure-results/` is generated for Allure reporting (requires [Allure server](https://docs.qameta.io/allure/)).
   To view Allure reports, install Allure and run:
   ```bash
   allure serve allure-results/
   ```

---

## Example Tests

Below are example test cases demonstrating BDD-style usage with this framework:

```python
# Example: UI search test
# (Assumes self.login_section and self._configuration.users are defined)
def should_find(self):
    self.login_section(random.choice(self._configuration.users))
    for word in ["hello", "kitty"]:
        (self.steps
            .when.searching_for(word)
            .then.the_search_hints(
                yields_item(contains_string_ignoring_case(word))))
```

```python
# Example: API add test
def should_add(self):
    random_pet = SwaggerPetstorePet.random()
    (self.steps
        .when.adding(random_pet)
        .then.the_available_pets(yields_item(is_(random_pet))))
```

---

## Requirements

- Python 3.13
- Google Chrome for local Selenium testing
- [PDM](https://pdm-project.org) (Python package manager)

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