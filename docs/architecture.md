#   Architecture

> Support for additional technologies, e.g. Playwright, ElasticSearch, can be added by sub-classing these classes and adding specific steps, setup/teardown, and configuration. This allows reusing the basic configuration, reporting, logging, and retrying mechanisms. Further, application tests, steps, and configurations reuse by subclassing from technologies.

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

## Extending the Framework

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

---

## Key Classes

| Class | Description |
|-------|-------------|
| [`AbstractTestsBase`](api/qa-pytest-commons.md#qa_pytest_commons.AbstractTestsBase) | Base for all test scenarios; holds steps and config |
| [`GenericSteps`](api/qa-pytest-commons.md#qa_pytest_commons.GenericSteps) | Base for all step implementations; provides BDD keywords |
| [`BaseConfiguration`](api/qa-pytest-commons.md#qa_pytest_commons.BaseConfiguration) | Base for all configuration objects |
| [`RestTests`](api/qa-pytest-rest.md#qa_pytest_rest.RestTests) | REST-specific test base |
| [`RestSteps`](api/qa-pytest-rest.md#qa_pytest_rest.RestSteps) | REST-specific steps |
| [`RestConfiguration`](api/qa-pytest-rest.md#qa_pytest_rest.RestConfiguration) | REST-specific configuration |
| [`SeleniumTests`](api/qa-pytest-webdriver.md#qa_pytest_webdriver.SeleniumTests) | Selenium-specific test base |
| [`SeleniumSteps`](api/qa-pytest-webdriver.md#qa_pytest_webdriver.SeleniumSteps) | Selenium-specific steps |
| [`SeleniumConfiguration`](api/qa-pytest-webdriver.md#qa_pytest_webdriver.SeleniumConfiguration) | Selenium-specific configuration |
| [`PlaywrightTests`](api/qa-pytest-playwright.md#qa_pytest_playwright.PlaywrightTests) | Playwright-specific test base |
| [`PlaywrightSteps`](api/qa-pytest-playwright.md#qa_pytest_playwright.PlaywrightSteps) | Playwright-specific steps |
| [`PlaywrightConfiguration`](api/qa-pytest-playwright.md#qa_pytest_playwright.PlaywrightConfiguration) | Playwright-specific configuration |
| [`TerminalXConfiguration`](api/qa-pytest-examples.md#qa_pytest_examples.TerminalXConfiguration) | Example: custom UI configuration |

---

## Usage Examples

### TerminalX Tests

```python
--8<-- "terminalx_tests.py:class"
```

#### The Setup Method
The `setup_method` demonstrates how default setup behavior can be overriden.
In real world it would be pulled into a superclass that extends `SeleniumTests`.

#### The Configuration
Furthermore, the `self._configuration.parser["selenium"]["browser_type"]` could
be defined as a method on the `TerminalXConfiguration` class, or a superclass of
it.

The configuration is loaded from two sources, in this example:

1. `TerminalXConfiguration` class looks for a matching
`terminalx_configuration.ini` file under `configurations/`.
2. pytest could be launched with a `--config` parameter to override
this or add properties:
```bash
pytest --config selenium:browser_type=firefox qa-pytest-examples/tests/terminalx_tests.py::TerminalXTests
```

Any subclass of [`BaseConfiguration`](api/qa-pytest-commons.md#qa_pytest_commons.BaseConfiguration)
looks for a matching `ini` file, this way multiple configurations can be used.

If there is a `TEST_ENVIRONMENT` environment variable its value will be chained
to the path of `ini` file, this way one can select which configuration set
shall be used at runtime.

### Swagger Petstore Tests

```python
--8<-- "swagger_petstore_tests.py:class"
```

### Combined Tests

```python
--8<-- "combined_tests.py:class"
```

### RabbitMQ Self Tests

```python
--8<-- "rabbitmq_self_tests.py:class"
```


::: qa_testing_utils.pytest_plugin
    options:
      show_source: true

