from infrastructure.repos import users
from model.domain.entities import User
from model.domain.vos import Address, City


async def perform(telegram_chat_id: int, city_name: str) -> User:
    user = await users.get_by_telegram_chat_id(telegram_chat_id)

    if user is not None:
        return user

    address = Address(city=City(name=city_name))
    user = User(telegram_chat_id=telegram_chat_id, address=address)

    await users.add(user)

    return user
