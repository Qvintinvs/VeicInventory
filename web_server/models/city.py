from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    fuel_consumption: Mapped[float] = mapped_column(nullable=False)

    def __init__(self, name: str, fuel_consumption: float):
        self.name = name
        self.fuel_consumption = fuel_consumption
