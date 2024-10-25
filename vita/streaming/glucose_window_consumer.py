from kafka import KafkaConsumer
from vita.utils.config import KAFKA_BROKER, KAFKA_PASSWORD, KAFKA_USERNAME

consumer = KafkaConsumer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)
consumer.subscribe("glucose-window")

for message in consumer:
    topic_info = f"topic: {message.topic} ({message.partition}|{message.offset})"
    message_info = f"key: {message.key}, {message.value}"
    print(f"{topic_info}, {message_info}")
