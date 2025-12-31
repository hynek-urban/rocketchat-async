# rocketchat-async

asyncio-based Python wrapper for the Rocket.Chat Realtime API.

Supported Rocket.Chat versions: 7.x. (The library might also work or partially work with other versions.)

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
import random
from rocketchat_async import RocketChat


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier,
                   unread, repeated):
    """Simply print the message that arrived."""
    print(msg)


async def main(address, username, password):
    while True:
        try:
            rc = RocketChat()
            await rc.start(address, username, password)
            # Alternatively, use rc.resume for token-based authentication:
            # await rc.resume(address, username, token)

            # A possible workflow consists of two steps:
            #
            # 1. Set up the desired callbacks...
            for channel_id, channel_type in await rc.get_channels():
                await rc.subscribe_to_channel_messages(channel_id,
                                                       handle_message)
            # 2. ...and then simply wait for the registered events.
            await rc.run_forever()
        except (RocketChat.ConnectionClosed,
                RocketChat.ConnectCallFailed) as e:
            print(f'Connection failed: {e}. Waiting a few seconds...')
            await asyncio.sleep(random.uniform(4, 8))
            print('Reconnecting...')


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

#### `RocketChat.send_typing_event(channel_id, thread_id=None)`

Send the "typing" event to a channel or to a specified thread within that channel.

#### `RocketChat.subscribe_to_channel_messages(channel_id, callback)`

Subscribe to all messages in the given channel. Returns the subscription ID.

The provided callback should accept eight arguments: `channel_id`,
`sender_id`, `msg_id`, `thread_id`, `msg_text`, `msg_qualifier`
 and `repeated`. The qualifier can help to determine if e.g. the
message is a system message about the user being removed from
the channel.  The `repeated` flag assists in distinguishing 
whether the message has been received again as a result of 
thread replies or reactions, or if it is a new message post.

#### `RocketChat.subscribe_to_channel_changes(callback)`

Subscribe to all changes in channels. Returns the subscription ID.

The provided callback should accept two arguments: `channel_id`
and `channel_qualifier`. The qualifier helps to determine e.g.
if it's a direct message or a normal room.

#### `RocketChat.subscribe_to_channel_changes_raw(callback)`

Like `RocketChat.subscribe_to_channel_changes` except the callback gets passed the raw message object coming from the API.

#### `RocketChat.subscribe_to_channel_messages_raw(channel_id, callback)`

Like `RocketChat.subscribe_to_channel_messages` except the callback gets passed the raw message object coming from the API.

#### `RocketChat.get_channels_raw()`

Like `RocketChat.get_channels` except the method returns the list of raw channel objects coming from the API.

#### `RocketChat.unsubscribe(subscription_id)`

Cancel a subscription.
