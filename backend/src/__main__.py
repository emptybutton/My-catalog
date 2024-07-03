import asyncio
from contextlib import asynccontextmanager

from faststream import FastStream, ContextRepo

from periphery import mongo
from periphery.brokers import kafka_broker
from presentation.event_routes import router


@asynccontextmanager
async def faststream_lifespan(context: ContextRepo) -> None:
    yield
    await mongo.client.close()


async def start_faststream() -> None:
    faststream = FastStream(kafka_broker, lifespan=faststream_lifespan)
    kafka_broker.include_router(router)

    await faststream.run()


async def main() -> None:
    await start_faststream()


if __name__ == "__main__":
    asyncio.run(main())

