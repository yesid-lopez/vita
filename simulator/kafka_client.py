import json

from kafka import KafkaProducer

from vita.utils.config import KAFKA_BROKER, KAFKA_PASSWORD, KAFKA_USERNAME

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD,
)

hostname = str.encode("glucose-device")


def on_success(metadata):
    print(f"Sent to topic '{metadata.topic}' at offset {metadata.offset}")


def on_error(e):
    print(f"Error sending message: {e}")


def send(bg: float, ts):
    payload = {
        "bg": float(bg),
        "ts": ts,
    }
    future = producer.send(
        "glucose",
        key=hostname,
        value=json.dumps(payload).encode("utf-8"),
    )
    future.add_callback(on_success)
    future.add_errback(on_error)


def stop_producer():
    producer.flush()
    producer.close()
