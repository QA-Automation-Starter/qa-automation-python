# SPDX-License-Identifier: Apache-2.0
"""
qa_pytest_rabbitmq.rabbitmq_tests

Base BDD test class for RabbitMQ, similar to AbstractRabbitMqTest.java.
"""
from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_rabbitmq.rabbitmq_configuration import RabbitMqConfiguration
from qa_pytest_rabbitmq.queue_handler import QueueHandler
from typing import Any


class RabbitMqTests(
    AbstractTestsBase
    [GenericSteps[RabbitMqConfiguration],
     RabbitMqConfiguration]):
    """Base class for RabbitMQ BDD tests."""
    configuration: RabbitMqConfiguration
    queue_handler: QueueHandler[Any, Any]
    # ...implementation placeholder for setup/teardown and BDD step composition...
    pass
