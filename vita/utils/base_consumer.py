import json

from kafka import KafkaConsumer

from vita.utils.config import (
    KAFKA_BROKER,
    KAFKA_PASSWORD,
    KAFKA_SASL_MECHANISM,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_USERNAME,
)


class BaseConsumer:
    def __init__(self, topic: str):
        self.consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BROKER,
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=KAFKA_SASL_MECHANISM,
            sasl_plain_username=KAFKA_USERNAME,
            sasl_plain_password=KAFKA_PASSWORD,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )
        self.topic = topic
