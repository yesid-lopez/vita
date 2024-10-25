import json
from websockets.sync.client import connect

from vita.utils.config import WEBSOCKET_SERVER_URI


def send(message):
    with connect(WEBSOCKET_SERVER_URI) as websocket:
        websocket.send(json.dumps(message))
