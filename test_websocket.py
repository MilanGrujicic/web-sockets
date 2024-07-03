import asyncio
import pytest
import websockets
from server import echo

@pytest.fixture
def websocket_server():
    server = websockets.serve(echo, "localhost", 8765)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    yield
    server.ws_server.close()
    loop.run_until_complete(server.ws_server.wait_closed())

@pytest.mark.asyncio
async def test_websocket_echo(websocket_server):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Hello, test!"
        await websocket.send(message)
        response = await websocket.recv()
        assert response == message

@pytest.mark.asyncio
async def test_websocket_multiple_messages(websocket_server):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        messages = ["first", "second", "third"]
        for message in messages:
            await websocket.send(message)
            response = await websocket.recv()
            assert response == message
