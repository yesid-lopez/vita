from datetime import timedelta

from quixstreams import Application

from vita.stream_processing.reducers.glucose_reducer import (
    custom_ts_extractor,
    initializer,
    reducer,
)
from vita.utils.config import KAFKA_TOPIC
from vita.utils.logger import logging
from vita.utils.quix_kafka_connection import connection

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

sdf = (
    sdf.tumbling_window(timedelta(minutes=10))
    .reduce(reducer=reducer, initializer=initializer)
    .final()
)

sdf = sdf.apply(
    lambda value: {
        "time": value["end"],
        "glucose": value["value"],
    }
)
sdf = sdf.update(lambda value: logger.info(f"Window: {value}"))

sdf = sdf.to_topic(output_topic)

app.clear_state()
app.run(sdf)
