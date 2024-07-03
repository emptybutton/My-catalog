from dataclasses import dataclass

from infrastructure import yandex_lavka_gateway
from infrastructure.repos import users, products, categories
from model.domain.entities import Category, Product, User


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user: User
    category: Category
    products: tuple[Product, ...]


class NoUserError(Exception): ...


async def perform(
    query: str,
    latitude: float,
    longitude: float,
    telegram_chat_id: int,
) -> OutputDTO:
    user = await users.get_by_telegram_chat_id(telegram_chat_id)

    if user is None:
        raise NoUserError

    found_products = tuple(await yandex_lavka_gateway.searth_products_for(
        user,
        query=query,
        latitude=latitude,
        longitude=longitude,
    ))

    await products.extend_by(found_products)

    product_ids = [product.id for product in found_products]

    category = Category(
        user_id=user.id,
        name=query,
        product_ids=product_ids,
        subcategory_ids=list(),
    )

    await categories.add(category)

    return OutputDTO(user=user, category=category, products=products)
