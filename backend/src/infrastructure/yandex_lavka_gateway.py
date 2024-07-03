from typing import Iterable

import aiohttp

from model.domain.entities import User, Product
from model.domain.vos import Page, Price, QuantityUnit, Quantity


async def searth_products_for(
    user: User,
    *,
    query: str,
    latitude: float,
    longitude: float,
    products_limit: int = 32,
    subcategories_limit: int = 0,
) -> Iterable[Product]:
    url = "https://lavka.yandex.ru/api/v1/providers/search/v2/lavka"
    headers = {
        "accept": "application/json",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrf-token": "3248921c6150c0e59d4f10b94d2b4ac3d9222fb3:1719991575",
        "x-lavka-web-city": "213",
        "x-lavka-web-locale": "ru-RU"
    }
    body = {
        "additionalData": {
            "city": user.city.name,
        },
        "text": query,
        "position": {"location": [latitude, longitude]},
        "productsLimit": products_limit,
        "subcategories_limit": subcategories_limit,
        "depotType": "regular"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers) as response:
            if response.status != 200:
                return None

            raw_product_by_index = await response.json().get("products")

            if raw_product_by_index is None:
                return None

    raw_products = raw_product_by_index.values()

    for raw_product in raw_products:
        rubels = raw_product.get("numberDiscountPrice")
        if rubels is None:
            rubels = raw_product["numberPrice"]

        if "г" in raw_product["amount"] or "кг" in raw_product["amount"]:
            quantity_unit = QuantityUnit.kilogram
        elif "мл" in raw_product["amount"] or "л" in raw_product["amount"]:
            quantity_unit = QuantityUnit.liter
        else:
            quantity_unit = None

        total = int(raw_product["amount"].split("&")[0])

        url = f"https://lavka.yandex.ru/213/good/{raw_product["deepLink"]}"
        name = raw_product["title"]

        yield Product(
            name=name,
            page=Page(url=url),
            price=Price(rubels=rubels),
            quantity=Quantity(total=total, unit=quantity_unit)
        )
