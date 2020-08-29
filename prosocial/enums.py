from enum import unique, Enum


@unique
class PostType(Enum):
    NORMAL = 0
    TICK_POLL = 1


@unique
class ReactionType(Enum):
    LIKE = 0
    HEART = 1
    HAHA = 2
    WOW = 3
    ANGRY = 4

    @staticmethod
    def get_name(value):
        for react in ReactionType:
            if value == react.value:
                return react.name
        return ReactionType.LIKE.name

@unique
class GenderType(Enum):
    MALE = 1
    FEMALE = 0
    OTHER = 2


@unique
class NotificationType(Enum):
    INIT = 0
    LIKE = 1
    COMMENT = 2

@unique
class TargetStatusType(Enum):
    NOT_SCORED = 0
    SCORED = 1
    CONFIRM = 2
