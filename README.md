# rocketchat-async

asyncio-based Python wrapper for the Rocket.Chat Realtime API.

## When should you use this library?

Use this library if you:

- want to integrate with Rocket.Chat from Python
- are using [asyncio](https://docs.python.org/3/library/asyncio.html) to drive your code
- want to use Rocket.Chat's efficient websockets-based Realtime API

## Installation

`pip install rocketchat-async`

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
    # A possible workflow consists of two steps:
    #
    # 1. Set up the desired callbacks...
    for channel_id, channel_type in await rc.get_channels():
        await subscribe_to_messages(rc, channel_id)
    # 2. ...and then simply wait for the registered events.
    await rc.run_forever()


# Side note: Don't forget to use the wss:// scheme when TLS is used.
asyncio.run(main('ws://localhost:3000/websocket', 'username', 'password'))
```

## API Overview

Brief overview of the currently implemented methods.

As of now, Rocket.Chat's API is only covered partially (based on my original
needs). I am open to both feature requests as well as pull requests.

### Methods

#### `RocketChat.get_channels()`

Get a list of channels the logged-in user is currently member of.

#### `RocketChat.send_message(text, channel_id, thread_id=None)`

Send a text message to a channel.

#### `RocketChat.send_reaction(orig_msg_id, emoji)`

Send a reaction to a specific message.

#### `RocketChat.send_typing_event(channel_id, is_typing)`

Send the "typing" event to a channel.

#### `RocketChat.subscribe_to_channel_messages(channel_id, callback)`

Subscribe to all messages in the given channel. Returns the subscription ID.

The provided callback should accept six arguments: `channel_id`,
`sender_id`, `msg_id`, `thread_id`, `msg_text` and
`msg_qualifier`. The qualifier can help to determine if e.g. the
message is a system message about the user being removed from
the channel.

#### `RocketChat.subscribe_to_channel_changes(callback)`

Subscribe to all changes in channels. Returns the subscription ID.

The provided callback should accept two arguments: `channel_id`
and `channel_qualifier`. The qualifier helps to determine e.g.
if it's a direct message or a normal room.

#### `RocketChat.unsubscribe(subscription_id)`

Cancel a subscription.
