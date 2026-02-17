# SPDX-License-Identifier: Apache-2.0

# qa-pytest-kafka

BDD steps module for Kafka integration testing, following the qa-pytest-* monorepo architecture.

## Features
- BDD step classes for publishing and consuming Kafka messages
- Topic creation/deletion utilities
- Partition-specific operations
- Test isolation and cleanup
- Integration with pytest and qa-pytest-commons

## Usage
See quickstart.md and tests for examples.

## Kafka Prerequisites
A running Kafka broker is required for self-tests and integration tests.

### Installation

1. install in podman/docker
```bash
podman pull docker.io/apache/kafka:latest
```

2. run it
```bash
podman run -d \
  --name my-kafka \
  -p 9092:9092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  apache/kafka:latest
```

3. create a topic for testing
```bash
podman exec my-kafka /opt/kafka/bin/kafka-topics.sh \
  --create --topic test-topic \
  --bootstrap-server localhost:9092
```

4. send a test message
```bash
echo "hello kafka" | podman exec -i my-kafka /opt/kafka/bin/kafka-console-producer.sh \
  --topic test-topic \
  --bootstrap-server localhost:9092
```

5. read messages
```bash
podman exec my-kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic test-topic \
  --from-beginning \
  --bootstrap-server localhost:9092 \
  --max-messages 1
```
> NOTE: if you want queue behavior add `--group my-pytest-group`
