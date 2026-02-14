# Copilot Instructions

## Scope
This file provides **tactical coding instructions**: how to write code, which tools to use, formatting standards, and coding practices.

**For governance principles, architecture patterns, and non-negotiable workflows, see [.specify/memory/constitution.md](../.specify/memory/constitution.md).**

## Coding Practices

**Module-specific testing approaches:**
- **qa-testing-utils**: Plain unit tests (no BDD, no pytest-commons dependency)
- **qa-pytest-commons**: Plain unit tests for infrastructure (e.g., bdd_scenario_tests.py tests BDD mechanics)
- **qa-pytest-{rest,webdriver,playwright,rabbitmq}**: Plain unit tests for utility classes (e.g., queue_handler_tests.py)
- **qa-pytest-examples**: BDD integration tests using steps from domain modules

**BDD scenarios apply only to qa-pytest-examples.** For BDD scenario structure, see [BDD Guide](../.specify/memory/bdd-guide.md).

- Follow the project's established code style and formatting rules (see `pyproject.toml`).
- Follow code style and re-use functionality of qa-testing-utils and qa-pytest-commons.
- **Always add type annotations**: Non-negotiable requirement (see constitution Type Safety Requirements)
- Always prefer Iterables over lists.
- **Testing strategy**: See [constitution.md - Testing Strategy by Module Type](../.specify/memory/constitution.md)
  - qa-testing-utils: Plain unit tests
  - qa-pytest-commons: BDD scenario tests
  - qa-pytest-{domain}: Unit tests + self-tests
  - qa-pytest-examples: BDD integration tests (see [BDD Guide](../.specify/memory/bdd-guide.md))

## Preferred Technologies
- Use Python 3.13 syntax for generics.
- Use PDM for adding new dependencies (see constitution Monorepo Structure).
- Always generate `__init__.py` files using `pdm run regenerate-init-and-format` for all modules and subpackages (do not create manually).
- Prefer one-liners unless unreadable.
- Use pytest for all tests.
- Use pyhamcrest for assertions.
- Tests shall comply with `tool.pytest.ini_options` in root pyproject.toml

## Project Requirements
- Ensure all code is covered by appropriate unit or integration tests.
- Adhere to the structure and conventions of each submodule.
- Document public APIs and important implementation details.
- Review and refactor Copilot suggestions for clarity.
- Do not introduce license-incompatible code or external dependencies without approval.

## Additional Notes
- Refer to `README.md` and `KNOWN-ISSUES.md` for project-specific guidance.
- All Copilot-generated code must be reviewed before merging.
