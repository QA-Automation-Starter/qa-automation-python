# Copilot Instructions

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
- Use BDD-style for all tests that build on-top of AbstractTestsBase,
  reference qa-pytest-rest and qa-pytest-webdriver modules as examples.

## Project Requirements
- Ensure all code is covered by appropriate unit or integration tests.
- Adhere to the structure and conventions of each submodule.
- Document public APIs and important implementation details.
- Review and refactor Copilot suggestions for clarity.
- Do not introduce license-incompatible code or external dependencies without approval.

## Additional Notes
- Refer to `README.md` and `KNOWN-ISSUES.md` for project-specific guidance.
- All Copilot-generated code must be reviewed before merging.
