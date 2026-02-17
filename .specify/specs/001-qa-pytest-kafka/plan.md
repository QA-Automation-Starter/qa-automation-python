# Implementation Plan: [FEATURE]


**Branch**: `001-qa-pytest-kafka` | **Date**: 2026-02-14 | **Spec**: [.specify/specs/001-qa-pytest-kafka/spec.md]
**Input**: Feature specification from `/.specify/specs/001-qa-pytest-kafka/spec.md`

## Summary

Implement a BDD steps module for Kafka, enabling test engineers to create topics, publish messages (with headers and keys), and consume/verify messages (content, headers, metadata) in integrated test flows. The module will follow the established monorepo architecture and patterns, mirroring the RabbitMQ steps module, and will use confluent-kafka-python (sync API, threading for background consumption). No Avro/schema registry in v1. All error/edge case handling will propagate API exceptions (fail fast, no extra retrying at BDD layer).

## Technical Context

- **Language/Version**: Python 3.13
- **Primary Dependencies**: confluent-kafka-python (with types-confluent-kafka), pytest, pyhamcrest, qa-pytest-commons, qa-testing-utils
- **Storage**: N/A (Kafka topics are ephemeral for tests)
- **Testing**: pytest, pyhamcrest, pytest-cov, pytest-html, allure-pytest
- **Target Platform**: Linux server (CI and local dev)
- **Project Type**: Monorepo, modular (qa-pytest-kafka as a new qa-* module)
- **Performance Goals**: Message publish/consume within 5 seconds (per spec)
- **Constraints**: 90%+ code coverage, type safety, test isolation, no Avro in v1
- **Scale/Scope**: Single module, integration with existing BDD infra

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Module must be independently testable, buildable, publishable, versioned
- Must use Python 3.13, pytest, pyhamcrest, PDM
- All code must be type safe (type annotations or stubs)
- Must follow dependency direction: qa-testing-utils → qa-pytest-commons → qa-pytest-kafka → qa-pytest-examples
- No custom retry/timeout logic; use qa-pytest-commons infra
- Synchronous API preferred; threading for background, not async/await
- No Avro/schema registry in v1
- Must provide self-test verifying Kafka works before implementing features
- All code must be covered by tests (unit + self-test)
- No .venv or lock file in submodules; only at root
- Editable install via root dev-dependencies

No violations detected. All requirements are compatible with the planned Kafka module.


## Project Structure

### Documentation (this feature)


```text
.specify/specs/001-qa-pytest-kafka/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code

```text
qa-pytest-kafka/
├── src/qa_pytest_kafka/         # Kafka BDD steps implementation
├── tests/                       # Unit and self-tests
├── pyproject.toml               # Module-specific dependencies
└── README.md                    # Module documentation
```

**Structure Decision**: New qa-pytest-kafka module, following the established qa-* pattern. Source in src/qa_pytest_kafka/, tests in tests/, config in pyproject.toml, docs in README.md. No .venv or lock file in submodule.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
