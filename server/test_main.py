import asyncio
from datetime import timedelta
import yaml
from quart import Quart, websocket
from quart.testing import QuartClient
from quart_rate_limiter import RateLimit, RateLimiter, rate_limit
from websockets.exceptions import ConnectionClosed
import pytest

import main

@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()

async def test_index(client):
    response = await client.get('/')
    assert response.status == 200
    assert response.get_data() == b'Hello, from Ping-Pong server!'

async def test_websocket(client):
    with mock.patch.object(amainp, 'sleep', return_value=None) as mock_sleep:
        async with client.websocket('/ws') as ws:
            await ws.send('ping')
            assert await ws.receive() == 'pong'
            mock_sleep.assert_called_with(0)

async def test_throttling():
    global last_message_time
    throttling_time = 0.5
    last_message_time = 0
    for i in range(10):
        current_time = asyncio.get_event_loop().time()
        delta_time = current_time - last_message_time
        assert delta_time >= throttling_time
        last_message_time = current_time
        await asyncio.sleep(0.1)

async def test_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    assert config.get('throttling_time') == 1
    assert config.get('host') == '0.0.0.0'
    assert config.get('port') == 8000
