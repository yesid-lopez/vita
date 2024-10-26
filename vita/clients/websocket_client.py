import json
from websockets.sync.client import connect

from vita.utils.config import WEBSOCKET_HOST, WEBSOCKET_PORT


def send(message):
    print(f"Websocket server uri: ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    with connect(f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}") as websocket:
        websocket.send(json.dumps(message))
