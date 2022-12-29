import asyncio
import websockets

from rocketchat_async.dispatcher import Dispatcher
from rocketchat_async.methods import Connect, Login, GetChannels, SendMessage,\
        SendReaction, SendTypingEvent, SubscribeToChannelMessages,\
        SubscribeToChannelChanges, Unsubscribe


class RocketChat:
    """Represents a connection to RocketChat, exposing the API."""

    def __init__(self):
        self._dispatcher = Dispatcher(verbose=True)
        self.user_id = None

    async def start(self, address, username, password):
        ws_connected = asyncio.get_event_loop().create_future()
        ws_connection = self._start(address, ws_connected)
        self._ws_connection_task = asyncio.create_task(ws_connection)
        await ws_connected
        # Connect and login.
        await self._connect()
        self.user_id = await self._login(username, password)

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
        return await GetChannels.call(self._dispatcher)

    async def send_message(self, context, text):
        await SendMessage.call(self._dispatcher, context, text)

    async def send_reaction(self, orig_msg_id, emoji):
        await SendReaction.call(orig_msg_id, emoji)

    async def send_typing_event(self, context, is_typing):
        await SendTypingEvent.call(self._dispatcher, context, False)

    async def subscribe_to_channel_messages(self, channel_id, callback):
        sub_id = await SubscribeToChannelMessages.call(self._dispatcher,
                                                       channel_id, callback)
        return sub_id

    async def subscribe_to_channel_changes(self, callback):
        sub_id = await SubscribeToChannelChanges.call(self._dispatcher,
                                                      self.user_id, callback)
        return sub_id

    async def unsubscribe(self, subscription_id):
        await Unsubscribe.call(self._dispatcher, subscription_id)
