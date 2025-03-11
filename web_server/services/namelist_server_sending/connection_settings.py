from typing import NamedTuple


class ConnectionSettings(NamedTuple):
    hostname: str
    username: str
    password: str | None
