from enum import Enum, auto


class WRFRoundStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()
