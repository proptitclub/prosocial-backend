from enum import unique, Enum


@unique
class PostType(Enum):
    NORMAL = 0
    TICK_POLL = 1


@unique
class UserGroupRole(Enum):
    ADMIN = 0
    USER = 1
