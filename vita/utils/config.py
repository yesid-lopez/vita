from dotenv import load_dotenv
from os import getenv

load_dotenv()

KAFKA_TOPIC = getenv("KAFKA_TOPIC")
KAFKA_BROKER = getenv("KAFKA_BROKER")
KAFKA_USERNAME = getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = getenv("KAFKA_PASSWORD")
