import hashlib
import time
from rocketchat_async.response_dataclass import ReceivedMessage
from dacite import from_dict

class RealtimeRequest:
    """Method call or subscription in the RocketChat realtime API."""
    _max_id = 0

    @staticmethod
    def _get_new_id():
        RealtimeRequest._max_id += 1
        return f'{RealtimeRequest._max_id}'


class Connect(RealtimeRequest):
    """Initialize the connection."""

    REQUEST_MSG = {
        'msg': 'connect',
        'version': '1',
        'support': ['1'],
    }

    @classmethod
    async def call(cls, dispatcher):
        await dispatcher.call_method(cls.REQUEST_MSG)


class Resume(RealtimeRequest):
    """Log in to the service with a token."""

    @staticmethod
    def _get_request_msg(msg_id, token):
        return {
            "msg": "method",
            "method": "login",
            "id": msg_id,
            "params": [
                {
                    "resume": token,
                }
            ]
        }

    @staticmethod
    def _parse(response):
        return response['result']['id']

    @classmethod
    async def call(cls, dispatcher, token):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, token)
        response = await dispatcher.call_method(msg, msg_id)
        return cls._parse(response)


class Login(RealtimeRequest):
    """Log in to the service."""

    @staticmethod
    def _get_request_msg(msg_id, username, password):
        pwd_digest = hashlib.sha256(password.encode()).hexdigest()
        return {
            "msg": "method",
            "method": "login",
            "id": msg_id,
            "params": [
                {
                    "user": {"username": username},
                    "password": {
                        "digest": pwd_digest,
                        "algorithm": "sha-256"
                    }
                }
            ]
        }

    @staticmethod
    def _parse(response):
        if "error" in response:
            raise RuntimeError(response['error']['reason'])
        return response['result']['id']

    @classmethod
    async def call(cls, dispatcher, username, password):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, username, password)
        response = await dispatcher.call_method(msg, msg_id)
        return cls._parse(response)


class GetChannelsRaw(RealtimeRequest):
    """
    Get a list of channels user is currently member of.

    Returns the complete channel objects.

    """

    @staticmethod
    def _get_request_msg(msg_id):
        return {
            'msg': 'method',
            'method': 'rooms/get',
            'id': msg_id,
            'params': [],
        }

    @staticmethod
    def _parse(response):
        return response['result']

    @classmethod
    async def call(cls, dispatcher):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id)
        response = await dispatcher.call_method(msg, msg_id)
        return cls._parse(response)


class GetChannels(GetChannelsRaw):
    """
    Get a list of channels user is currently member of.

    Returns a list of (channel id, channel type) pairs.

    """

    @classmethod
    def _parse(cls, response):
        # Return channel IDs and channel types.
        return [(r['_id'], r['t']) for r in super()._parse(response)]


class SendMessage(RealtimeRequest):
    """Send a text message to a channel."""

    @staticmethod
    def _get_request_msg(msg_id, channel_id, msg_text, thread_id=None):
        id_seed = f'{msg_id}:{time.time()}'
        msg = {
            "msg": "method",
            "method": "sendMessage",
            "id": msg_id,
            "params": [
                {
                    "_id": hashlib.md5(id_seed.encode()).hexdigest()[:12],
                    "rid": channel_id,
                    "msg": msg_text
                }
            ]
        }
        if thread_id is not None:
            msg["params"][0]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, msg_text, channel_id, thread_id=None):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, channel_id, msg_text, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)
        return msg["params"][0]["_id"]

class UpdateMessage(RealtimeRequest):
    """Update a sent message"""

    @staticmethod
    def _get_request_msg(msg_id, orig_msg_id, channel_id, msg_text, thread_id=None):
        msg = {
            "msg": "method",
            "method": "updateMessage",
            "id": msg_id,
            "params": [
                {
                    "_id": orig_msg_id,
                    "rid": channel_id,
                    "msg": msg_text
                }
            ]
        }
        if thread_id is not None:
            msg["params"][0]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, msg_text, orig_msg_id, channel_id, thread_id=None):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, orig_msg_id, channel_id, msg_text, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)

class SendReaction(RealtimeRequest):
    """Send a reaction to a specific message."""

    @staticmethod
    def _get_request_msg(msg_id, orig_msg_id, emoji):
        return {
            "msg": "method",
            "method": "setReaction",
            "id": msg_id,
            "params": [
                emoji,
                orig_msg_id,
            ]
        }

    @classmethod
    async def call(cls, dispatcher, orig_msg_id, emoji):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, orig_msg_id, emoji)
        await dispatcher.call_method(msg)


class SendTypingEvent(RealtimeRequest):
    """Send the `typing` event to a channel."""

    @staticmethod
    def _get_request_msg(msg_id, is_typing, channel_id, username, thread_id=None):
        msg = {
            "msg": "method",
            "method": "stream-notify-room",
            "id": msg_id,
            "params": [
                f'{channel_id}/typing',
                username,
                is_typing
            ]
        }
        if(thread_id):
            msg["params"][-1]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, is_typing, channel_id, username, thread_id=None):
        msg_id = cls._get_new_id()
        is_typing = bool(is_typing)
        msg = cls._get_request_msg(msg_id, is_typing, channel_id, username, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)


class SubscribeToChannelMessagesRaw(RealtimeRequest):
    """
    Subscribe to all messages in the given channel.

    Passes the raw message object to the callback.

    """

    @staticmethod
    def _get_request_msg(msg_id, channel_id):
        return {
            "msg": "sub",
            "id": msg_id,
            "name": "stream-room-messages",
            "params": [
                channel_id,
                {
                    "useCollection": False,
                    "args": []
                }
            ]
        }

    @staticmethod
    def _wrap(callback):
        def fn(msg):
            event = msg["fields"]["args"][0]  # TODO: This looks suspicious.
            return callback(event)

        return fn

    @classmethod
    async def call(cls, dispatcher, channel_id, callback):
        # TODO: document the expected interface of the callback.
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, channel_id)
        await dispatcher.create_subscription(msg, cls._wrap(callback))
        return msg_id  # Return the ID to allow for later unsubscription.


class SubscribeToChannelMessagesParsed(SubscribeToChannelMessagesRaw):
    """Subscribe to all messages in the given channel."""
    @staticmethod
    def _wrap(callback):
        def fn(msg):
            event= msg['fields']['args'][0]     # TODO: This looks suspicious, why 0?
            msg_dataclass = from_dict(ReceivedMessage, event)
            return callback(msg_dataclass)
        return fn

class SubscribeToChannelMessages(SubscribeToChannelMessagesRaw):
    """Subscribe to all messages in the given channel."""

    @staticmethod
    def _wrap(callback):
        def fn(msg):
            event = msg['fields']['args'][0]  # TODO: This looks suspicious.
            msg_id = event['_id']
            channel_id = event['rid']
            thread_id = event.get('tmid')
            sender_id = event['u']['_id']
            msg = event['msg']
            qualifier = event.get('t')
            unread = event.get('unread', False)
            repeated = bool(event.get('replies'))
            return callback(channel_id, sender_id, msg_id, thread_id, msg,
                            qualifier, unread, repeated)
        return fn


class SubscribeToChannelChangesRaw(RealtimeRequest):
    """
    Subscribe to all messages in the given channel.

    Passes the raw message object to the callback.

    """

    @staticmethod
    def _get_request_msg(msg_id, user_id):
        return {
            "msg": "sub",
            "id": msg_id,
            "name": "stream-notify-user",
            "params": [
                f'{user_id}/rooms-changed',
                False
            ]
        }

    @staticmethod
    def _wrap(callback):
        def fn(msg):
            payload = msg['fields']['args']
            return callback(payload)
        return fn

    @classmethod
    async def call(cls, dispatcher, user_id, callback):
        # TODO: document the expected interface of the callback.
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, user_id)
        await dispatcher.create_subscription(msg, msg_id, cls._wrap(callback))
        return msg_id  # Return the ID to allow for later unsubscription.


class SubscribeToChannelChanges(SubscribeToChannelChangesRaw):
    """Subscribe to all changes in channels."""

    @staticmethod
    def _wrap(callback):
        def fn(msg):
            payload = msg['fields']['args']
            if payload[0] == 'removed':
                return  # Nothing else to do - channel has just been deleted.
            channel_id = payload[1]['_id']
            channel_type = payload[1]['t']
            return callback(channel_id, channel_type)
        return fn


class Unsubscribe(RealtimeRequest):
    """Cancel a subscription"""

    @staticmethod
    def _get_request_msg(subscription_id):
        return {
            "msg": "unsub",
            "id": subscription_id,
        }

    @classmethod
    async def call(cls, dispatcher, subscription_id):
        msg = cls._get_request_msg(subscription_id)
        await dispatcher.call_method(msg)
