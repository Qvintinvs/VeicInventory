from collections.abc import Iterable
from typing import NamedTuple

class VehicularData(NamedTuple):
    year: Iterable[int]
    fuel: Iterable[str]
    subcategory: Iterable[str]
