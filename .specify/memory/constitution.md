# QA Automation Python Monorepo Constitution

## Development Standards

All code must comply with [.github/copilot-instructions.md](../../.github/copilot-instructions.md), which defines:
- Coding practices (type annotations, Iterables preference, one-liners)
- Technology stack (Python 3.13, pytest, pyhamcrest, PDM)
- BDD test structure (see also [qa-pytest-examples/.specify/memory/bdd-guide.md](../../qa-pytest-examples/.specify/memory/bdd-guide.md))

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

### IV. Quality Gates
Before merging to main:
- **All tests pass**: `pdm run pytest` across all modules
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

### Module Structure
Each `qa-*` module contains:
```
qa-MODULE-NAME/
├── src/qa_MODULE_NAME/  # Source code
├── tests/               # Tests mirroring src structure
├── pyproject.toml       # Module-specific dependencies
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

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
