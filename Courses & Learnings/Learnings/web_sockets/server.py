import asyncio

from websockets.asyncio.server import Server, ServerConnection, serve


async def echo(websocket: ServerConnection) -> None:
    """
    Handles an individual WebSocket connection.

    Args:
        websocket: The connection instance used to send and receive messages.
    """
    async for messages in websocket:
        print(f"Received: {messages}")
        await websocket.send(messages)


async def main() -> None:
    """
    Starts the WebSocket server and keeps it running.
    """
    async with serve(echo, "localhost", 8765) as server:
        server: Server
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
