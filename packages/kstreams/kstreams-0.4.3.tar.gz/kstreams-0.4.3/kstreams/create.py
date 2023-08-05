from typing import Optional, Type

from .backends.kafka import Kafka
from .clients import Consumer, ConsumerType, Producer, ProducerType
from .engine import StreamEngine
from .prometheus.monitor import PrometheusMonitor
from .serializers import ValueDeserializer, ValueSerializer


def create_engine(
    title: Optional[str] = None,
    backend: Optional[Kafka] = None,
    consumer_class: Type[ConsumerType] = Consumer,
    producer_class: Type[ProducerType] = Producer,
    value_serializer: Optional[ValueSerializer] = None,
    value_deserializer: Optional[ValueDeserializer] = None,
    monitor: Optional[PrometheusMonitor] = None,
) -> StreamEngine:

    if monitor is None:
        monitor = PrometheusMonitor()

    if backend is None:
        backend = Kafka()

    return StreamEngine(
        backend=backend,
        title=title,
        consumer_class=consumer_class,
        producer_class=producer_class,
        value_serializer=value_serializer,
        value_deserializer=value_deserializer,
        monitor=monitor,
    )
