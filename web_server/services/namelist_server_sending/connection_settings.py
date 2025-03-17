from typing import NamedTuple


class ConnectionSettings(NamedTuple):
    hostname: str | None
    username: str | None
    password: str | None
