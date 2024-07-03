from dataclasses import dataclass, field
from uuid import UUID, uuid4

from model.domain.errors import FreeProductError
from model.domain.vos import Price, Page, Quantity, Address


@dataclass(kw_only=True)
class User:
    id: UUID = field(default_factory=uuid4)
    telegram_chat_id: int
    address: Address


@dataclass(kw_only=True)
class Category:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    name: str
    product_ids: list[UUID]
    subcategory_ids: list[UUID]


@dataclass(kw_only=True)
class Product:
    id: UUID = field(default_factory=uuid4)
    name: str
    price: Price
    quantity: Quantity
    page: Page

    def __post_init__(self) -> None:
        if self.price.rubles == 0:
            raise FreeProductError
