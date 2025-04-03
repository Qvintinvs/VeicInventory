from typing import NamedTuple


class WRFRemoteConnectionSettings(NamedTuple):
    hostname: str | None
    username: str | None
    password: str | None
