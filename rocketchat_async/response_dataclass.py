from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict

@dataclass
class PlainText:
    type: str
    value: str

@dataclass
class MentionUser:
    type: str
    value: PlainText

@dataclass
class LinkValue:
    label: List[PlainText]
    src: PlainText

@dataclass
class Link:
    type: str
    value: LinkValue

@dataclass
class ParagraphValue:
    type: str
    value: Union[PlainText, MentionUser, Link, ]

@dataclass
class Paragraph:
    type: str
    value: List[ParagraphValue]

@dataclass
class CodeLine:
    type: str
    value: PlainText

@dataclass
class Code:
    language: str
    type: str
    value: List[CodeLine]

@dataclass
class LineBreak:
    type: str

@dataclass
class InlineCode:
    type: str
    value: PlainText

@dataclass
class Bold:
    type: str
    value: List[PlainText]

@dataclass
class Italic:
    type: str
    value: List[PlainText]

@dataclass
class Strike:
    type: str
    value: List[PlainText]

@dataclass
class MdElement:
    type: str
    value: Optional[Union[List[Paragraph], List[CodeLine], None]] = None
    language: Optional[str] = None

@dataclass
class Mention:
    _id: str
    name: str
    type: str
    username: str

@dataclass
class Url:
    meta: Dict
    url: str
    headers: Optional[Dict[str, str]]=None

@dataclass
class User:
    _id: str
    name: str
    username: str

# TODO: this only works for parsing received message. Other events (e.g. user join channel) will not work, need to be generalized
@dataclass
class ReceivedMessage:
    _id: str
    _updatedAt: Dict[str, int]
    channels: List
    # TODO: should be List[MdElement], but currently not work
    md: List
    mentions: List[Mention]
    msg: str
    rid: str
    ts: Dict[str, int]
    u: User
    urls: List[Url]
