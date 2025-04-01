from enum import Enum, auto


class RoundCompletionTryStatus(Enum):
    SUCCESS = auto()
    NOT_FOUND = auto()
    ERROR = auto()
