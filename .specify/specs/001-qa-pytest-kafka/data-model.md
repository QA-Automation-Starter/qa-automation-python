# Data Model: Kafka BDD Steps Module

## Key Entities

- **KafkaMessage**: Represents a Kafka message with the following fields:
  - content: JSON, string, or binary
  - headers: dict[str, str]
  - key: str | bytes
  - partition: int
  - offset: int
  - timestamp: int | None

- **KafkaTopic**: Represents a Kafka topic
  - name: str
  - partition_count: int
  - config: dict[str, str]

- **KafkaConfiguration**: Test configuration for broker connection, serialization, and consumer settings
  - bootstrap_servers: str
  - security_protocol: str
  - group_id: str
  - auto_offset_reset: str
  - additional: dict[str, Any]

## Relationships

- KafkaMessage is published to a KafkaTopic (partition specified)
- KafkaConfiguration is used by all steps and handlers

## Notes
- No Avro/schema registry in v1
- All fields must be type-annotated
- Data model mirrors RabbitMQ and REST modules for consistency
