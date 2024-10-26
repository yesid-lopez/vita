import asyncio
import logging

from websockets import ConnectionClosedError, ConnectionClosedOK
from websockets.asyncio.server import serve

from vita.utils.config import WEBSOCKET_HOST, WEBSOCKET_PORT

clients = set()

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            logger.info(f"Received: {message}")
            disconnected_clients = set()
            for client in clients:
                if client != websocket:
                    try:
                        await client.send(message)
                    except ConnectionClosedError:
                        disconnected_clients.add(client)
            clients.difference_update(disconnected_clients)
    except ConnectionClosedOK:
        logger.info("Connection closed gracefully.")
    finally:
        clients.remove(websocket)
        logger.info("Client disconnected.")


async def main():
    async with serve(handler, WEBSOCKET_HOST, WEBSOCKET_PORT):
        logger.info(
            f"Server started at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        await asyncio.Future()  # run forever

asyncio.run(main())
