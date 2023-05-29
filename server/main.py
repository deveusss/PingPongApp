import asyncio
from datetime import timedelta
import ssl
import yaml
from quart import Quart, websocket
from quart_rate_limiter import RateLimit, RateLimiter, rate_limit
from websockets.exceptions import ConnectionClosed

app = Quart(__name__)

async def sleep(duration):
    await asyncio.sleep(duration)

last_message_time = 0

@app.route('/')
async def index():
    return 'Hello, from Ping-Pong server!'

# apply rate limiting to the WebSocket endpoint
@app.websocket('/ws')
async def ws():
    global last_message_time
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            delta_time = current_time - last_message_time
            # throttle the messages
            if delta_time < throttling_time:
                await sleep(throttling_time - delta_time)
            data = await websocket.receive()
            print(data)
            if data == 'ping':
                await websocket.send('pong')
                last_message_time = asyncio.get_event_loop().time()
        except ConnectionClosed:
            # the connection was closed, so we need to reconnect
            await asyncio.sleep(1)
            last_message_time = asyncio.get_event_loop().time()
            await ws()

if __name__ == '__main__':
    # read the configuration from a YAML file
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    # set the throttling time
    throttling_time = config.get('throttling_time', 1)
    # set the host and port
    host = config.get('host', '0.0.0.0')
    port = config.get('port', 8080)
    # run the app
    app.run(host=host, port=port)
