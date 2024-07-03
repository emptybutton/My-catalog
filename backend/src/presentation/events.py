from pydantic import BaseModel

from presentation import sculptures


class UserStartedRegistration(BaseModel):
    telegram_chat_id: int
    city_name: str


class UserRegistered(BaseModel):
    user: sculptures.UserSculpture


class UserStartedCategoryAddingWithQuery(BaseModel):
    query: str
    latitude: float
    longitude: float
    telegram_chat_id: int


class UserAddedCategoryByQuery(BaseModel):
    user: sculptures.UserSculpture
    category: sculptures.CategorySculpture
    products: tuple[sculptures.ProductSculpture, ...]
    query: str


class UserCantAddCategoryByQuery(BaseModel):
    query: str
    latitude: float
    longitude: float
    telegram_chat_id: int
