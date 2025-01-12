from enum import Enum


# Note: the mix-in classes should be eventually replaced by StrEnum.


class MessageQualifier(str, Enum):
    """Lists special message types."""
    REMOVE_USER = "ru"


class ChannelQualifier(str, Enum):
    """Lists special message types."""
    DIRECT_MESSAGE = "d"
    PRIVATE_CHANNEL = "p"
    PUBLIC_CHANNEL = "c"


class Emoji(str, Enum):
    """Selection of emojis that are subjectively "most fun"."""
    GRIN = ':grin:'
    SWEAT_SMILE = ':sweat_smile:'
    JOY = ':joy:'
    HEART_EYES = ':heart_eyes:'
    SMILING_FACE_WITH_3_HEARTS = ':smiling_face_with_3_hearts:'
    NERD = ':nerd:'
    SUNGLASSES = ':sunglasses:'
    PARTYING_FACE = ':partying_face:'
    SOB = ':sob:'
    EXPLODING_HEAD = ':exploding_head:'
    FEARFUL = ':fearful:'
    ROLLING_EYES = ':rolling_eyes:'
    THUMBSUP = ':thumbsup:'
    THUMBSDOWN = ':thumbsdown:'
    FINGERS_CROSSED = ':fingers_crossed:'
    METAL = ':metal:'
    V = ':v:'
    MAN_FACEPALMING = ':man_facepalming:'
    POINT_UP = ':point_up:'
    PENGUIN = ':penguin:'
