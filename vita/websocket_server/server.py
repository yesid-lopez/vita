import asyncio

from websockets import ConnectionClosedOK
from websockets.asyncio.server import serve

from vita.utils.config import WEBSOCKET_HOST, WEBSOCKET_PORT

clients = set()


async def handler(websocket):
    try:
        clients.add(websocket)
        async for message in websocket:
            print(f"Received: {message}")
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except ConnectionClosedOK:
        print("Connection closed gracefully.")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def main():
    async with serve(handler, WEBSOCKET_HOST, WEBSOCKET_PORT):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())
