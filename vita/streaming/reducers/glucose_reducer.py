from vita.utils.logger import logging

logger = logging.getLogger(__name__)


def initializer(value: dict) -> dict:
    return {
        "count": 1,
        "min": value["bg"],
        "max": value["bg"],
        "mean": value["bg"],
    }


def reducer(aggregated: dict, value: dict) -> dict:
    aggcount = aggregated["count"] + 1
    return {
        "count": aggcount,
        "min": min(aggregated["min"], value["bg"]),
        "max": max(aggregated["max"], value["bg"]),
        "mean": (aggregated["mean"] * aggregated["count"] + value["bg"])
        / (aggregated["count"] + 1),
    }


def custom_ts_extractor(value, headers=None, partition=0, timestamp_type=None):
    milliseconds = int(value["ts"] * 1000)
    value["timestamp"] = milliseconds
    logger.info(f"Value of new timestamp is: {value['timestamp']}")
    return value["timestamp"]
