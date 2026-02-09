# Feature Specification: Kafka BDD Steps Module

**Feature Branch**: `001-qa-pytest-kafka`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "a bdd steps module for kafka"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Message Publishing and Consumption (Priority: P1)

Test engineers need to verify that messages can be published to and consumed from Kafka topics in BDD-style tests, enabling basic end-to-end message flow validation.

**Why this priority**: Core functionality - without the ability to send and receive messages, no meaningful Kafka testing can occur. This represents the minimum viable functionality.

**Independent Test**: Can be fully tested by publishing a message to a test topic and verifying it can be consumed, delivering immediate value for basic message flow testing.

**Acceptance Scenarios**:

1. **Given** a Kafka broker is running and a test topic exists, **When** a message is published to the topic, **Then** the message appears in the topic and can be consumed
2. **Given** a message has been published to a topic, **When** a consumer reads from the topic, **Then** the consumed message matches the published message content
3. **Given** multiple messages are published to a topic, **When** a consumer reads from the topic, **Then** all messages are consumed in the correct order

---

### User Story 2 - Message Content Verification (Priority: P2)

Test engineers need to verify the content, headers, and metadata of consumed messages to ensure message integrity and correct processing in their applications.

**Why this priority**: Essential for validating message structure and content, but depends on basic publish/consume capability (P1).

**Independent Test**: Can be tested by publishing messages with specific content and headers, then verifying the consumed messages match expected values.

**Acceptance Scenarios**:

1. **Given** a message with specific headers is published, **When** the message is consumed, **Then** the headers match expected values
2. **Given** a message with JSON payload is published, **When** the message is consumed, **Then** the payload can be parsed and verified
3. **Given** a message with metadata (partition, offset, timestamp), **When** the message is consumed, **Then** the metadata is accessible and correct

---

### User Story 3 - Topic and Partition Management (Priority: P3)

Test engineers need to manage topics and partitions during tests to verify partition-specific behavior and ensure proper test isolation.

**Why this priority**: Important for advanced scenarios and test isolation, but not required for basic message testing.

**Independent Test**: Can be tested by creating topics with specific partition counts, publishing to specific partitions, and verifying partition assignment.

**Acceptance Scenarios**:

1. **Given** a test requires a new topic, **When** the topic is created with specified partition count, **Then** the topic exists with the correct configuration
2. **Given** a topic with multiple partitions, **When** messages are published to a specific partition, **Then** messages are only consumed from that partition
3. **Given** a test is complete, **When** the test topic is deleted, **Then** the topic no longer exists in the broker

---

### User Story 4 - Consumer Group Testing (Priority: P3)

Test engineers need to verify consumer group behavior to ensure proper message distribution and offset management across multiple consumers.

**Why this priority**: Advanced use case for testing distributed consumption patterns, but not required for basic message validation.

**Independent Test**: Can be tested by configuring consumer groups, publishing messages, and verifying message distribution and offset commits.

**Acceptance Scenarios**:

1. **Given** multiple consumers in the same consumer group, **When** messages are published, **Then** messages are distributed among consumers
2. **Given** a consumer in a consumer group processes messages, **When** the consumer commits offsets, **Then** the offsets are persisted in Kafka
3. **Given** a consumer group has committed offsets, **When** a new consumer joins the group, **Then** it resumes from the last committed offset

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
- **FR-006**: System MUST support consumer group configuration for testing distributed consumption
- **FR-007**: System MUST provide utilities for topic creation and deletion during tests
- **FR-008**: System MUST support partition-specific message operations
- **FR-009**: System MUST integrate with pytest and qa-pytest-commons BDD infrastructure
- **FR-010**: System MUST provide proper cleanup mechanisms to ensure test isolation
- **FR-011**: System MUST delegate timeout and retry handling to qa-pytest-commons generic retry mechanisms (retrying, eventually_assert_that)
- **FR-012**: Kafka operations MUST provide simple success/failure responses without internal retry logic

### Key Entities *(include if feature involves data)*

- **KafkaMessage**: Represents a message with content, headers, key, partition, offset, and timestamp
- **KafkaTopic**: Represents a topic with name, partition count, and configuration
- **ConsumerGroup**: Represents a consumer group with group ID and offset management
- **KafkaConfiguration**: Test configuration for broker connection, serialization, and consumer settings

## Clarifications

### Session 2026-02-09

- Q: Which Python Kafka client library should this module use? → A: kafka-python
- Q: How should the module handle consume timeout when no messages are available? → A: don't handle, use generic retry
- Q: Should the module support Avro schema registry integration for message serialization? → A: No - Start with JSON/string/binary only

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
- The module follows the same architectural patterns as qa-pytest-rabbitmq (fixtures, actions, verifications classes)
- JSON is the primary message format, with support for string and binary as alternatives (Avro schema registry support deferred to future versions)
- The module uses the kafka-python library for Kafka operations
- Tests run in isolated environments where topic creation/deletion is permitted
