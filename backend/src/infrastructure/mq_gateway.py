from pydantic import BaseModel

from periphery.brokers import redis_broker


class _MultiplicationOccurred(BaseModel):
    a: int
    b: int
    result: int


async def push_multiplication_occurred(a: int, b: int, result: int) -> None:
    event  = _MultiplicationOccurred(a=a, b=b, result=result)

    async with redis_broker:
        await redis_broker.publish(event, "multiplication_occurred")
