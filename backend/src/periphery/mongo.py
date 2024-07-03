from motor.motor_asyncio import AsyncIOMotorClient

from periphery.envs import Env


client = AsyncIOMotorClient(Env.mongo_connecion_uri)
db = client.mycatalog_db
