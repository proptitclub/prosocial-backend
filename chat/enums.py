from enum import unique, Enum

@unique
class MessageType(Enum):
    TEXT = 0
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3