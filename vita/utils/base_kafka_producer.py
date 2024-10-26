
import json

from kafka import KafkaProducer

from vita.utils.config import (KAFKA_BROKER, KAFKA_PASSWORD,
                               KAFKA_SASL_MECHANISM, KAFKA_SECURITY_PROTOCOL,
                               KAFKA_USERNAME)


class BaseKafkaProducer:
    def __init__(self, topic: str):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=KAFKA_SASL_MECHANISM,
            sasl_plain_username=KAFKA_USERNAME,
            sasl_plain_password=KAFKA_PASSWORD,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def stop_producer(self):
        self.producer.close()
