# Feature Specification: Kafka BDD Steps Module

**Feature Branch**: `001-qa-pytest-kafka`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "a bdd steps module for kafka"

**Note**: This specification focuses on Kafka-specific requirements. General monorepo practices (type safety, dependency management, testing strategy, architecture patterns) are defined in [constitution.md](../../.specify/memory/constitution.md).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Kafka Message Lifecycle (Priority: P1)

Test engineers need to create topics, publish messages with headers and keys, and consume/verify messages including their content, headers, and metadata in integrated test flows.

**Why this priority**: Core functionality covering the complete message lifecycle - without this, test engineers cannot write realistic Kafka tests. Includes topic creation, partition management, and message verification.

**Independent Test**: Can be fully tested end-to-end by creating a multi-partition topic, publishing a message with headers to a specific partition, consuming it, and verifying all message attributes.

**Acceptance Scenarios**:

```gherkin
Scenario: Complete Kafka message lifecycle with verification
  Given a Kafka broker
  When creating a topic named "test-events" with 3 partitions
  Then the test-events topic has 3 partitions
  When publishing messages to test-events:
    | content                       | headers                           | key      | partition |
    | {"event": "login", "seq": 1}  | {"source": "web", "version": "1"} | user-123 | 0         |
    | {"event": "logout", "seq": 2} | {"source": "web", "version": "1"} | user-123 | 1         |
  Then the messages from test-events partition 0 match:
    | content                       | headers                           | key      | partition | offset |
    | {"event": "login", "seq": 1}  | {"source": "web", "version": "1"} | user-123 | 0         | 0      |
  Then the messages from test-events partition 1 match:
    | content                       | headers                           | key      | partition | offset |
    | {"event": "logout", "seq": 2} | {"source": "web", "version": "1"} | user-123 | 1         | 0      |
  When deleting the test-events topic
  Then the test-events topic no longer exists
```

---

### Edge Cases

- What happens when attempting to consume from a non-existent topic?
- How does the system handle messages that exceed the configured maximum size?
- What happens when a consumer attempts to read from a partition that doesn't exist?
- How are serialization errors handled when publishing or consuming messages?
- What happens when the Kafka broker is unavailable during publish or consume operations?
- How does the system handle duplicate message keys with different values?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide BDD step classes for publishing messages to Kafka topics
- **FR-002**: System MUST provide BDD step classes for consuming messages from Kafka topics
- **FR-003**: System MUST support message serialization for common formats (JSON, string, binary) but NOT Avro schema registry in initial version
- **FR-004**: System MUST allow verification of message content, headers, and metadata
- **FR-005**: System MUST provide fixtures for Kafka broker configuration and connection management
- **FR-006**: System SHOULD support consumer group configuration (optional, for advanced scenarios)
- **FR-007**: System MUST provide utilities for topic creation and deletion during tests
- **FR-008**: System MUST support partition-specific message operations
- **FR-009**: System MUST integrate with pytest and qa-pytest-commons BDD infrastructure
- **FR-010**: System MUST provide proper cleanup mechanisms to ensure test isolation

### Key Entities *(include if feature involves data)*

- **KafkaMessage**: Represents a message with content, headers, key, partition, offset, and timestamp
- **KafkaTopic**: Represents a topic with name, partition count, and configuration
- **KafkaConfiguration**: Test configuration for broker connection, serialization, and consumer settings

## Clarifications

### Session 2026-02-09

- Q: Which Python Kafka client library should this module use? → A: confluent-kafka-python (synchronous API, simpler than async, adequate for task)
- Q: How should the module handle consume timeout when no messages are available? → A: don't handle, use generic retry
- Q: Should the module support Avro schema registry integration for message serialization? → A: No - Start with JSON/string/binary only

### Session 2026-02-12

- Q: Can we use confluent-kafka-python despite incomplete type hints (issue #1310)? → A: YES - Sync API preference outweighs type hint completeness. Use `# type: ignore` pragmatically where needed (similar to how Playwright sync API is preferred over async despite async having better support)
- Q: Should we use threading for background consumption (like queue_handler)? → A: YES - Follow RabbitMQ queue_handler pattern: threading for background work, synchronous public API

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Test engineers can write BDD scenarios for Kafka message flows using Given-When-Then syntax consistent with other qa-pytest modules
- **SC-002**: Message publish and consume operations complete within 5 seconds for standard test scenarios
- **SC-003**: The module provides at least 90% code coverage through its own test suite
- **SC-004**: Integration with qa-pytest-commons allows test engineers to write Kafka tests with the same patterns as REST, WebDriver, and RabbitMQ tests
- **SC-005**: Test cleanup ensures no topic pollution between test runs (100% test isolation)

## Assumptions

- Kafka broker is available and accessible during test execution (similar to RabbitMQ module assumptions)
- Test engineers are familiar with Kafka concepts (topics, partitions, consumer groups)
- JSON is the primary message format, with support for string and binary as alternatives (Avro schema registry support deferred to future versions)
- The module uses confluent-kafka-python library (synchronous API, threading for background consumption like queue_handler)
- Minimal `# type: ignore` pragmas accepted where confluent-kafka type hints incomplete (pragmatic trade-off for sync simplicity)
- Tests run in isolated environments where topic creation/deletion is permitted
