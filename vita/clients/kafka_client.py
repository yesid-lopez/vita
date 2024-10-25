from quixstreams.kafka.configuration import ConnectionConfig

from vita.utils.config import (
    KAFKA_BROKER,
    KAFKA_PASSWORD,
    KAFKA_USERNAME,
)

connection = ConnectionConfig(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_username=KAFKA_USERNAME,
    sasl_password=KAFKA_PASSWORD,
)
