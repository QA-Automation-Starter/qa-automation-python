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
- **Refactoring completeness**: When refactoring shared code, verify updates in ALL affected files:
  - Primary module implementation (src/)
  - Integration tests (qa-pytest-examples/tests/)
  - Unit tests (qa-pytest-MODULE/tests/) ← Often overlooked
  - Self-tests (technology verification)
- **Testing strategy**: See [constitution.md - Testing Strategy by Module Type](../.specify/memory/constitution.md)
  - qa-testing-utils: Plain unit tests
  - qa-pytest-commons: BDD scenario tests
  - qa-pytest-{domain}: Unit tests + self-tests
  - qa-pytest-examples: BDD integration tests (see [BDD Guide](../.specify/memory/bdd-guide.md))
  - **Context managers mandatory**: All resources with cleanup (consumers, producers, handlers, connections) SHOULD use `with` statements, unless there is a specific
  reason to hold them open at the instance-level, and then the instance SHALL support
  the context manager protocol
  - **Dependency injection**: In order to allow configuration of dependencies,
  these must be supplied from outside, not hardcoded
  - **Single-param mandatory**: All methods/functions SHOULD have a single-param
  signature unless there is a special reason not to do so; that parameter can
  be a type of declared class with multiple fields
  - **Fast-return**: All methods/functions SHOULD prefer having `return` as their
  first and last statement; this also means, small functions, that do one thing
  - **Inlining**: SHOULD prefer inlining calls in order to reduce number of variables

## Preferred Technologies
- Use Python 3.13 syntax for generics: **PEP 695 syntax preferred** (`class Foo[T]: ...` instead of `class Foo(Generic[T]): ...` with `TypeVar`).
- Use PDM for adding new dependencies (see constitution Monorepo Structure).
- Always generate `__init__.py` files using `pdm run regenerate-init-and-format` for all modules and subpackages (do not create manually).
- Prefer one-liners unless unreadable.
  - Use pytest for all tests.
  - Always run tests using `pdm run pytest ...` to ensure the correct virtual environment and dependencies are used.
- Use pyhamcrest for assertions.
- Tests shall comply with `tool.pytest.ini_options` in root pyproject.toml
  - Test function names must match the `python_functions` pattern (e.g., `should_*`)
  - Each new module (e.g., qa-pytest-kafka) must be added to `.vscode/settings.json` in both `python.testing.pytestArgs` and `python.analysis.extraPaths` for test discovery and analysis, matching the pattern used for other modules.

## Project Requirements
- Ensure all code is covered by appropriate unit or integration tests.
- Adhere to the structure and conventions of each submodule.
- Document public APIs and important implementation details.
- Review and refactor Copilot suggestions for clarity.
- Do not introduce license-incompatible code or external dependencies without approval.

## Configuration Maintenance

**When adding new qa-pytest-* module:**
1. Update `pyproject.toml`: testpaths, pythonpath, dev-dependencies
2. Update `.vscode/settings.json`: pytestArgs, extraPaths
3. Update `mkdocs.yml`: paths, base_path, nav
4. Create `docs/api/qa-pytest-MODULE.md`
5. Verify test discovery: `pdm run pytest --collect-only` (should show all tests)

**When modifying pytest configuration:**
- Always verify test discovery still works: `pdm run pytest --collect-only | tail -3`
- Check that test count matches expectations
- Run locally before pushing to CI

**CI/Local parity:**
- CI test command must match local test discovery
- Validate pytest config changes don't break test collection

## Code Style Exceptions

Certain infrastructure patterns require relaxing the "single-param", "one-thing", "fast-return", and "inlining" rules. These exceptions are intentional and documented below.

**Important**: These exceptions are rare. When tempted to relax the rules, ask: "Is this background infrastructure, a DSL, or a language protocol?" If none apply, follow the rules strictly.

### Background Event Loops & Polling Patterns
- **Where**: Message broker handlers, queue consumers, event listeners (background worker threads)
- **Why exception exists**: Event loops must continuously poll/subscribe and cannot follow "fast-return" (single return at end) or "one-thing" (single responsibility) patterns without becoming unreadable
- **Acceptable pattern**: A main loop method may contain `while not shutdown` with error handling and dispatch to focused helper methods
- **Mitigation**: Extract business logic into focused single-purpose methods called from the loop

### DSL-Style Fluent APIs
- **Where**: BDD step methods in UI automation, fluent builders, domain-specific languages
- **Why exception exists**: Multi-parameter signatures are essential for readability and developer familiarity in domain-specific contexts
- **Acceptable pattern**: Methods like `.action(param1, param2)` are clearer than `.action(ActionObject(param1, param2))` when params are closely related
- **Mitigation**: Document multi-param design decisions in method docstrings; keep parameter count to 2-3 maximum

### Magic Methods & Protocol Implementations
- **Where**: `__init__()`, `__setattr__()`, `__get__()`, context manager methods
- **Why exception exists**: Python protocols and dunder methods have fixed signatures; compliance with language semantics overrides architecture rules
- **Mitigation**: Delegate complex logic to focused helper methods

## Additional Notes
- Refer to `README.md` and `KNOWN-ISSUES.md` for project-specific guidance.
- All Copilot-generated code must be reviewed before merging.
