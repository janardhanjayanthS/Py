import asyncio

from websockets.asyncio.client import ClientConnection, connect


async def hello() -> None:
    """
    Connects to the server, sends a message, and waits for an echo.
    """
    async with connect("ws://localhost:8765") as websocket:
        websocket: ClientConnection
        message_to_send: str = input("Enter message to server: ")
        await websocket.send(message_to_send)

        # recv() returns Union[str, bytes] depending on what the server sends
        message: str | bytes = await websocket.recv()
        print(message)


if __name__ == "__main__":
    asyncio.run(hello())
