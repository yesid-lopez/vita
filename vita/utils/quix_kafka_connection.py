from quixstreams.kafka.configuration import ConnectionConfig

from vita.utils.config import (
    KAFKA_BROKER,
    KAFKA_PASSWORD,
    KAFKA_USERNAME,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_SASL_MECHANISM,
)

connection = ConnectionConfig(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    sasl_mechanism=KAFKA_SASL_MECHANISM,
    sasl_username=KAFKA_USERNAME,
    sasl_password=KAFKA_PASSWORD,
)
