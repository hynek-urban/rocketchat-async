import asyncio
import websockets

from rocketchat_async.dispatcher import Dispatcher
from rocketchat_async.methods import Connect, Login, GetChannels, SendMessage,\
        SendReaction, SendTypingEvent, SubscribeToChannelMessages,\
        SubscribeToChannelChanges, Unsubscribe


class RocketChat:
    """Represents a connection to RocketChat, exposing the API."""

    def __init__(self):
        self.user_id = None
        self.username = None
        self._dispatcher = Dispatcher(verbose=False)

    async def start(self, address, username, password):
        ws_connected = asyncio.get_event_loop().create_future()
        ws_connection = self._start(address, ws_connected)
        self._ws_connection_task = asyncio.create_task(ws_connection)
        await ws_connected
        # Connect and login.
        await self._connect()
        self.user_id = await self._login(username, password)
        self.username = username

    async def run_forever(self):
        await self.dispatch_task

    async def _start(self, address, connected_fut):
        try:
            async with websockets.connect(address) as websocket:
                self.dispatch_task = self._dispatcher.run(websocket)
                # Notify the caller that login has succeeded.
                connected_fut.set_result(True)
                # Finally, create the ever-running dispatcher loop.
                await self.dispatch_task
        except Exception as e:
            connected_fut.set_exception(e)

    async def _connect(self):
        await Connect.call(self._dispatcher)

    async def _login(self, username, password):
        return await Login.call(self._dispatcher, username, password)

    # --> Public API methods start here. <--

    async def get_channels(self):
        """Get a list of channels user is currently member of."""
        return await GetChannels.call(self._dispatcher)

    async def send_message(self, text, channel_id, thread_id=None):
        """Send a text message to a channel."""
        await SendMessage.call(self._dispatcher, text, channel_id, thread_id)

    async def send_reaction(self, orig_msg_id, emoji):
        """Send a reaction to a specific message."""
        await SendReaction.call(self._dispatcher, orig_msg_id, emoji)

    async def send_typing_event(self, channel_id, is_typing):
        """Send the `typing` event to a channel."""
        await SendTypingEvent.call(self._dispatcher, channel_id, self.username,
                                   is_typing)

    async def subscribe_to_channel_messages(self, channel_id, callback):
        """
        Subscribe to all messages in the given channel.

        Returns the subscription ID.

        """
        sub_id = await SubscribeToChannelMessages.call(self._dispatcher,
                                                       channel_id, callback)
        return sub_id

    async def subscribe_to_channel_changes(self, callback):
        """
        Subscribe to all changes in channels.

        Returns the subscription ID.

        """
        sub_id = await SubscribeToChannelChanges.call(self._dispatcher,
                                                      self.user_id, callback)
        return sub_id

    async def unsubscribe(self, subscription_id):
        """Cancel a subscription."""
        await Unsubscribe.call(self._dispatcher, subscription_id)
