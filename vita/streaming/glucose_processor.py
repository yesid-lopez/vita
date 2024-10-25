from datetime import timedelta

from quixstreams import Application

from vita.clients.kafka_client import connection
from vita.clients.websocket_client import send
from vita.streaming.reducers.glucose_reducer import (custom_ts_extractor,
                                                     initializer, reducer)
from vita.utils.config import KAFKA_TOPIC
from vita.utils.logger import logging

logger = logging.getLogger(__name__)

app = Application(
    broker_address=connection,
    consumer_group=None,
    # consumer_group="glucose-processor",
    use_changelog_topics=False,
    auto_offset_reset="earliest",
)

input_topic = app.topic(
    KAFKA_TOPIC,
    timestamp_extractor=custom_ts_extractor,
    value_deserializer="json",
)
output_topic = app.topic(
    "glucose-window",
    value_serializer="json",
)

sdf = app.dataframe(input_topic)
sdf = sdf.update(lambda value: logger.info(f"Input value: {value}"))

sdf = (
    sdf.tumbling_window(timedelta(minutes=10), grace_ms=timedelta(minutes=5))
    .reduce(reducer=reducer, initializer=initializer)
    .final()
)

sdf = sdf.apply(
    lambda value: {
        "time": value["end"],
        "glucose": value["value"],
    }
)

sdf = sdf.to_topic(output_topic)
sdf = sdf.update(lambda value: send(value))

app.clear_state()
app.run(sdf)
