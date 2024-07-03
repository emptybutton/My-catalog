from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from model.domain.errors import NegativePriceError, NegativeQuantityError


@dataclass(frozen=True, kw_only=True)
class Price:
    rubles: int

    def __post_init__(self) -> None:
        if self.rubles < 0:
            raise NegativePriceError


class QuantityUnit(Enum):
    kilogram = auto()
    liter = auto()


@dataclass(frozen=True, kw_only=True)
class Quantity:
    total: int
    unit: Optional[QuantityUnit] = field(default=None)

    def __post_init__(self) -> None:
        if self.rubles < 0:
            raise NegativeQuantityError


@dataclass(frozen=True, kw_only=True)
class Page:
    url: str


@dataclass(frozen=True, kw_only=True)
class City:
    name: str


@dataclass(frozen=True, kw_only=True)
class Address:
    city: City
