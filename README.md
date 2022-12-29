# rocketchat-async

asyncio-based Python wrapper for the Rocket.Chat Realtime API.

## When should you use this library?

Use this library if you:

- want to integrate with Rocket.Chat from Python
- are using [asyncio](https://docs.python.org/3/library/asyncio.html) to drive your application
- want to use Rocket.Chat's efficient websockets-based Realtime API

## Example usage

```python
import asyncio
from rocketchat_async import RocketChat


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier):
    """Simply print the message that arrived."""
    print(msg)


async def subscribe_to_messages(rc, channel):
    """Subscribe to a channel message."""
    await rc.subscribe_to_channel_messages(channel, handle_message)


async def main(address, username, password):
    rc = RocketChat()
    await rc.start(address, username, password)
    # One possible workflow consists of two steps:
    #
    # 1. Set up the desired callbacks...
    for channel_id, channel_type in await rc.get_channels():
        await subscribe_to_messages(rc, channel_id)
    # 2. ...and then simply wait for the registered events.
    await rc.run_forever()


# Side note: Don't forget to use the wss:// scheme when TLS is used.
asyncio.run(main('ws://localhost:3000/websocket', 'username', 'password'))
```
