# SPDX-License-Identifier: Apache-2.0

from typing import Any, Generic, TypeVar, override

import pika
from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_rabbitmq.rabbitmq_configuration import RabbitMqConfiguration
from qa_pytest_rabbitmq.rabbitmq_steps import RabbitMqSteps

_K = TypeVar("_K")
_V = TypeVar("_V")
_TConfiguration = TypeVar("_TConfiguration", bound=RabbitMqConfiguration)
_TSteps = TypeVar("_TSteps", bound=RabbitMqSteps[Any, Any, Any])


class RabbitMqTests(
        Generic[_K, _V, _TSteps, _TConfiguration],
        AbstractTestsBase[_TSteps, _TConfiguration]):
    _connection: pika.BlockingConnection

    @override
    def setup_method(self):
        super().setup_method()
        self._connection = pika.BlockingConnection(
            self._configuration.connection_uri)

    @override
    def teardown_method(self):
        try:
            self._connection.close()
        finally:
            super().teardown_method()
