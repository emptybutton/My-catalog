from model.domain.entities import Category
from periphery.mongo import db


async def add(category: Category) -> None:
    await db.categories.insert_one({
        "id": category.id,
        "user_id": category.user_id,
        "name": category.name,
        "product_ids": category.product_ids,
        "subcategory_ids": category.subcategory_ids,
    })
