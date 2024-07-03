from typing import Optional

from model.domain.entities import User
from model.domain.vos import Address, City
from periphery.mongo import db


async def add(user: User) -> None:
    await db.users.insert_one({
        "id": user.id,
        "telegram_chat_id": user.telegram_chat_id,
        "city": user.address.city.name,
    })


async def get_by_telegram_chat_id(telegram_chat_id: int) -> Optional[User]:
    user_record = await db.users.find_one(
        {"telegram_chat_id": telegram_chat_id},
        {"id": 1, "city": 1, "_id": 0},
    )

    if user_record is None:
        return None

    id_ = user_record.get("id")
    city_name = user_record.get("city")

    if None in [id_, city_name]:
        return None

    address = Address(city=City(name=city_name))
    return User(id=id_, telegram_chat_id=telegram_chat_id, address=address)
