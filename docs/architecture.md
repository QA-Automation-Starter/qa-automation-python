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

## Key Classes

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
