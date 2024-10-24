import json  # used for serializing data
import uuid  # used for message id creation
from dataclasses import asdict, dataclass  # used to define the data schema
from datetime import datetime, timedelta
from time import sleep  # used to slow down the data generator
import logging

from quixstreams import Application
from quixstreams.kafka.configuration import ConnectionConfig

from vita.utils.config import (
    KAFKA_BROKER,
    KAFKA_PASSWORD,
    KAFKA_TOPIC,
    KAFKA_USERNAME,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection = ConnectionConfig(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_username=KAFKA_USERNAME,
    sasl_password=KAFKA_PASSWORD,
)

app = Application(
    broker_address=connection,
    consumer_group="quix-stream-processor",
    auto_offset_reset="earliest",
)
app.clear_state()

def custom_ts_extractor(value, headers=None, partition=0, timestamp_type=None):
    # Assuming `value["ts"]` is in seconds, convert to milliseconds for Quix compatibility
    milliseconds = int(value["ts"] * 1000)
    value["timestamp"] = milliseconds
    logger.info(f"Value of new timestamp is: {value['timestamp']}")
    return value["timestamp"]


input_topic = app.topic(
    KAFKA_TOPIC,
    timestamp_extractor=custom_ts_extractor,
    value_deserializer="json"
)
output_topic = app.topic("reducer_glucose", value_serializer="json")


def initializer(value: dict) -> dict:

    return {
        'count': 1,
        'min': value['bg'],
        'max': value['bg'],
        'mean': value['bg'],
    }


def reducer(aggregated: dict, value: dict) -> dict:
    aggcount = aggregated['count'] + 1
    return {
        'count': aggcount,
        'min': min(aggregated['min'], value['bg']),
        'max': max(aggregated['max'], value['bg']),
        'mean': (aggregated['mean'] * aggregated['count'] + value['bg']) / (aggregated['count'] + 1)
    }


sdf = app.dataframe(input_topic)
sdf = sdf.update(lambda value: print(f"Input value received: {value}"))


sdf = (
    sdf.tumbling_window(timedelta(minutes=10), grace_ms=timedelta(minutes=5))  # Try increasing grace period
    .reduce(reducer=reducer, initializer=initializer)
    .final()
)

sdf = sdf.apply(
    lambda value: {
        "time": value["end"], # Use the window end time as the timestamp for message sent to the 'agg-temperature' topic
        "temperature": value["value"], # Send a dictionary of {count, min, max, mean} values for the temperature parameter
    }
)

sdf = sdf.to_topic(output_topic)
sdf = sdf.update(lambda value: logger.info(f"Produced value: {value}"))
app.run(sdf)
