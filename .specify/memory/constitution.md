# QA Automation Python Monorepo Constitution

## Scope
This document defines **governance, principles, architecture patterns, and non-negotiable workflows**.

**For tactical coding instructions (formatting, tools, style), see [.github/copilot-instructions.md](../../.github/copilot-instructions.md).**

## Development Standards

All code must comply with [.github/copilot-instructions.md](../../.github/copilot-instructions.md), which defines:
- Coding practices (type annotations, Iterables preference, one-liners)
- Technology stack (Python 3.13, pytest, pyhamcrest, PDM)
- BDD test structure (see also [bdd-guide.md](bdd-guide.md))

## Core Principles

### I. Module Independence
Each module under `qa-*` is independently:
- **Testable**: Must pass `pytest` with declared dependencies
- **Buildable**: Must build with `pdm build` using well-defined dependencies (internal monorepo modules + external PyPI packages)
- **Publishable**: Can be published to PyPI independently
- **Versioned**: Shares common version number but evolves independently

### II. Test-First (NON-NEGOTIABLE)
Test-Driven Development is mandatory:
1. Write BDD scenario or test case first
2. Verify tests fail (red)
3. Implement minimum code to pass (green)
4. Refactor while maintaining green
5. No implementation commits without corresponding tests

### III. Dependency Direction
```
qa-testing-utils (base utilities)
       ↓
qa-pytest-commons (pytest foundation + BDD steps base)
       ↓
qa-pytest-{rest,webdriver,playwright,rabbitmq} (domain-specific BDD steps)
       ↓
qa-pytest-examples (integration examples)
```

**Dependency Rules:**
- **All modules depend on qa-testing-utils** (directly or transitively)
- **BDD step modules depend on qa-pytest-commons** (rest, webdriver, playwright, rabbitmq)
- **Upward dependencies forbidden**: Lower layers cannot depend on higher layers
- **Cross-domain dependencies forbidden**: `qa-pytest-rest` cannot depend on `qa-pytest-webdriver`
- **External dependencies allowed**: Each module declares PyPI dependencies for its purpose
- **Shared utilities go in commons or utils**: Not in domain modules

**Type Safety Requirements (NON-NEGOTIABLE):**
- **All dependencies MUST have type annotations**: Native type hints preferred, type stubs acceptable
- **No untyped libraries**: Reject dependencies without type support unless no typed alternative exists AND explicitly approved
- **Verify before selection**: Check type annotation support BEFORE adding any dependency
- **Popularity ≠ Type Safety**: Most popular library may not have best type support

### IV. Quality Gates
After adding new test(s):
- **All new tests pass**: use `pdm run pytest -v <module-file>` in order to pick the venv

Before merging to main:
- **All tests pass**: use `pdm run pytest` in order to pick the venv
- **No type errors**: All modules must type-check
- **Format compliance**: `pdm run format-all` applied
- **Documentation updated**: Public APIs documented in docstrings

### V. Source Control Policy (NON-NEGOTIABLE)
**No automatic commits, merges, or pushes:**
- All commits require explicit user approval
- All merges require explicit user approval
- All pushes require explicit user approval
- AI agents must propose changes only — never execute git operations
- User reviews and approves all permanent source control operations

## Monorepo Operations

### Monorepo Structure (NON-NEGOTIABLE)
- **Single .venv**: Only ONE virtual environment at root - NEVER in sub-packages
- **Single pdm.lock**: Only ONE lock file at root - NEVER in sub-packages
- **Editable installs**: Sub-packages installed via root `dev-dependencies` in editable mode
- **Workflow discipline**:
  - After adding/changing dependencies: `pdm run import-all`
  - Before removing dependencies: `pdm run clean-all` then `pdm run import-all`

### Module Structure
Each `qa-*` module contains:
```
qa-MODULE-NAME/
├── src/qa_MODULE_NAME/  # Source code
├── tests/               # Tests mirroring src structure
├── pyproject.toml       # Module-specific dependencies (NO lock file, NO .venv)
└── README.md            # Module documentation
```

### Versioning Coordination
- All modules share version number from root `pyproject.toml`
- Breaking changes in any module trigger MAJOR version bump across all
- Individual module changes trigger MINOR/PATCH version bump

### Build & Release
```bash
pdm run build-all      # Builds all modules
pdm run publish-all    # Publishes all modules to PyPI
pdm run install-all    # Installs all modules in editable mode
```

### CI/CD Configuration (NON-NEGOTIABLE)
**Service configuration must match documented setup:**
- **README as source of truth**: CI service configurations (GitHub Actions) MUST match module README installation instructions
- **Single-instance defaults**: CI environments use single-instance configurations for all backing services (message brokers, databases, caches)
- **Production defaults must be overridden**: Services with multi-node/clustering defaults MUST be configured for single-instance operation in CI
- **Simple health checks**: Prefer simple port checks (`nc -z localhost PORT`) over complex API commands
- **Configuration validation**: After modifying service setup in README, update CI workflow accordingly

**Common configuration patterns:**
- **Replication/clustering**: Override replication factors, cluster sizes, quorum requirements to 1
- **Resource limits**: Set memory, storage, and connection limits appropriate for CI environments
- **Timeouts**: Reduce initial delays, rebalance periods, and other wait times for faster tests
- **Security**: Use minimal authentication for test environments (avoid complex certificate setups)

**Example violations and fixes:**
- ❌ Service with default replication factor 3 → ✓ Override to 1 for single-node CI
- ❌ Complex health check commands that fail despite service running → ✓ Simple `nc -z localhost PORT`
- ❌ CI configuration diverging from README → ✓ Keep both synchronized
- ❌ Multi-node cluster configuration in CI → ✓ Single-node with clustering disabled

## Architecture Patterns

### Reuse Over Reinvention
- **Use qa-pytest-commons infrastructure**: Don't implement custom retry/timeout logic
- **Leverage existing mechanisms**: `retrying`, `eventually_assert_that` for async operations
- **Follow established patterns**: New modules mirror successful existing modules (fixtures, actions, verifications classes)
- **Consistency across domains**: All BDD step modules follow same structure (REST, WebDriver, Playwright, RabbitMQ, Kafka)

### Synchronous API Preference
- **Prefer synchronous APIs** when adequate for the task (simpler to write and maintain)
- **Background processing ≠ async/await**: Use threading for concurrent operations (e.g., queue_handler), keep API synchronous
- **Async complexity justified only when**: Sync API genuinely inadequate AND async provides material benefits
- **Example: Playwright**: Has async API, but sync API + retrying/eventually_assert_that works fine (async doesn't support hamcrest polling)
- **Type safety pragmatism**: Accept minimal `# type: ignore` pragmas rather than force async complexity for type hints alone


### Technology Onboarding Order
- **Install first**: Ensure the technology is installed and runnable locally
- **Document installation**: Provide links to official vendor documentation only (no restating or summarizing)
- **Prove installation**: Add a minimal self-test that verifies the technology works
- **Implement after proof**: Start feature implementation only after the self-test passes

### Testing Strategy by Module Type
- **qa-testing-utils**: Plain unit tests (no BDD, no pytest-commons dependency)
- **qa-pytest-commons**: BDD scenario tests demonstrating that BDD steps infrastructure and Allure reporting work (e.g., bdd_scenario_tests.py)
- **qa-pytest-{domain}**: Plain unit tests for utilities (if any, e.g., queue_handler_tests.py) + self-tests verifying wrapped technology works (e.g., playwright_self_tests.py, webdriver_self_tests.py)
- **qa-pytest-examples**: BDD integration tests using steps from domain modules

## Scope Management

### MVP-First Development
- **Core functionality first**: Get basic features working before advanced capabilities
- **Defer complexity**: Advanced features (e.g., Avro schema registry) deferred to future versions
- **Incremental expansion**: Start with JSON/string/binary, add specialized formats later
- **Value delivery**: Ensure core use cases work end-to-end before expanding scope

## Governance

### Amendment Process
1. Propose change via issue or PR
2. Document rationale and impact
3. Update this constitution
4. Update affected modules

### Conflict Resolution
- **Constitution supersedes** module-specific practices
- **copilot-instructions.md supersedes** for coding style
- **When in doubt**: Simplify, prefer established patterns

**Version**: 1.3.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-17
