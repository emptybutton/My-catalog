from functools import partial

from faststream.kafka import KafkaRouter

from model import cases
from presentation import events, sculptures


router = KafkaRouter()

subscriber = partial(router.subscriber, group_id="backend-node")
publisher = router.publisher


@subscriber("user-started-registration")
@publisher("user-registered")
async def register_user(
    event: events.UserStartedRegistration
) -> events.UserRegistered:
    user = await cases.register_user.perform(
        event.telegram_chat_id,
        event.city_name,
    )

    return events.UserRegistered(user=sculptures.UserSculpture.of(user))


user_added_category_by_query_publisher = publisher("user-added-category-by-query")
user_cant_add_category_by_query_publisher = publisher("user-cant-add-category-by-query")


@subscriber("user-started-category-adding-with-query")
async def add_category_by_query(
    event: events.UserStartedCategoryAddingWithQuery,
) -> None:
    try:
        result = await cases.add_category_by_query.perform(
            event.query,
            event.latitude,
            event.longitude,
            event.telegram_chat_id,
        )
        event_to_publish = events.UserAddedCategoryByQuery(
            user=sculptures.UserSculpture.of(result.user),
            category=sculptures.CategorySculpture.of(result.category),
            products=list(map(sculptures.ProductSculpture.of, result.products)),
            query=event.query,
        )

        user_added_category_by_query_publisher.publish(event_to_publish)

    except cases.add_category_by_query.NoUserError:
        event_to_publish = events.UserCantAddCategoryByQuery(
            query=event.query,
            latitude=event.latitude,
            longitude=event.longitude,
            telegram_chat_id=event.telegram_chat_id,
        )
        user_cant_add_category_by_query_publisher.publish(event_to_publish)
