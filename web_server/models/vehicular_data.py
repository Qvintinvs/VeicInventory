from collections.abc import Iterable
from typing import NamedTuple

class VehicularData(NamedTuple):
    years: Iterable[int]
    fuels: Iterable[str]
    subcategories: Iterable[str]
