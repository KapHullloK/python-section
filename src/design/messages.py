import enum
from dataclasses import dataclass

from abc import ABC, abstractmethod


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class IMessageParser(ABC):
    @abstractmethod
    def parse(self, json_message: JsonMessage) -> ParsedMessage:
        ...


class TelegramMessageParser(IMessageParser):
    def parse(self, json_message: JsonMessage) -> ParsedMessage:
        ...


class MattermostMessageParser(IMessageParser):
    def parse(self, json_message: JsonMessage) -> ParsedMessage:
        ...


class SlackMessageParser(IMessageParser):
    def parse(self, json_message: JsonMessage) -> ParsedMessage:
        ...


class MessageParserFactory:
    def __init__(self):
        self._parsers: dict[MessageType, IMessageParser] = {}

    def register(self, message_type: MessageType, parser: IMessageParser) -> None:
        self._parsers[message_type] = parser

    def get_parser(self, message_type: MessageType) -> IMessageParser:
        return self._parsers[message_type]
