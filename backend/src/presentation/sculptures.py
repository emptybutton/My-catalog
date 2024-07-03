from typing import Self
from uuid import UUID

from pydantic import BaseModel

from model import domain


class QuantitySculpture(BaseModel):
    total: int
    unit_code: int

    @classmethod
    def of(cls, quantity: domain.vos.Quantity) -> Self:
        return cls(
            total=quantity.total,
            unit_code=quantity.unit.value,
        )


class ProductSculpture(BaseModel):
    id: UUID
    name: str
    url: str
    price: int
    quantity: QuantitySculpture

    @classmethod
    def of(cls, product: domain.entities.Product) -> Self:
        return cls(
            id=product.id,
            name=product.name,
            url=product.page.url,
            price=product.price.rubles,
            quantity=QuantitySculpture.of(product.quantity),
        )


class CategorySculpture(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    product_ids: list[UUID]
    subcategory_ids: list[UUID]

    @classmethod
    def of(cls, category: domain.entities.Category) -> Self:
        return cls(
            id=category.id,
            user_id=category.user_id,
            name=category.name,
            product_ids=category.product_ids,
            subcategory_ids=category.subcategory_ids,
        )


class UserSculpture(BaseModel):
    id: UUID
    telegram_chat_id: int
    city_name: str

    @classmethod
    def of(cls, user: domain.entities.User) -> Self:
        return cls(
            id=user.id,
            telegram_chat_id=user.telegram_chat_id,
            city_name=user.city_name,
        )
