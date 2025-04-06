from enum import Enum, auto


class InsertRoundOutputStatus(Enum):
    SUCCESS = auto()
    ROUND_NOT_FOUND = auto()
    ERROR = auto()
