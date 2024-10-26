import json
from collections import deque

from kafka import KafkaConsumer
from websockets.sync.client import connect

from vita.utils.config import (KAFKA_BROKER, KAFKA_PASSWORD,
                               KAFKA_SASL_MECHANISM, KAFKA_SECURITY_PROTOCOL,
                               KAFKA_USERNAME, WEBSOCKET_URI)
from vita.utils.logger import get_logger

logger = get_logger(__name__)

TOPICS = ["glucose"]

consumer = KafkaConsumer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    sasl_mechanism=KAFKA_SASL_MECHANISM,
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda x: x.decode("utf-8"),
)

consumer.subscribe(TOPICS)

glucose_buffer = deque(maxlen=6)

# Establish WebSocket connection once
with connect(WEBSOCKET_URI) as websocket:
    logger.info(f"Websocket server connected to {WEBSOCKET_URI}")

    def handle_event(topic, message):
        logger.info(f"Received message from topic {topic}: {message}")
        if topic == "glucose":
            glucose_buffer.append(message)
            logger.info(f"Buffer: {glucose_buffer}")
            websocket.send(json.dumps(list(glucose_buffer)))

    for message in consumer:
        handle_event(message.topic, message.value)
