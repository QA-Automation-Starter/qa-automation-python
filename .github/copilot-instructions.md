# Copilot Instructions

## Testing Strategy

**Module-specific testing approaches:**
- **qa-testing-utils**: Plain unit tests (no BDD, no pytest-commons dependency)
- **qa-pytest-commons**: Plain unit tests for infrastructure (e.g., bdd_scenario_tests.py tests BDD mechanics)
- **qa-pytest-{rest,webdriver,playwright,rabbitmq}**: Plain unit tests for utility classes (e.g., queue_handler_tests.py)
- **qa-pytest-examples**: BDD integration tests using steps from domain modules

**BDD scenarios apply only to qa-pytest-examples.** For BDD scenario structure, see [BDD Guide](../qa-pytest-examples/.specify/memory/bdd-guide.md).

## Coding Practices
- Follow the project's established code style and formatting rules (see `pyproject.toml`).
- Follow code style and re-use functionality of qa-testing-utils and qa-pytest-commons.
- Always add type annotations.
- Always prefer Iterables over lists.

## Preferred Technologies
- Use Python 3.13 syntax for generics.
- Use PDM for adding new dependencies.
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
