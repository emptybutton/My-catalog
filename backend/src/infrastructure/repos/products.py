from typing import Iterable

from model.domain.entities import Product
from periphery.mongo import db


async def add(product: Product) -> None:
    await db.products.insert_one(_document_of(product))


async def extend_by(products: Iterable[Product]) -> None:
    await db.products.insert_many(map(_document_of, products))


def _document_of(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "price_rubles": product.price.rubles,
        "page_url": product.page.url,
        "quantity": {
            "total": product.quantity.total,
            "unit_code": product.quantity.unit.value,
        },
    }