from functools import lru_cache
from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@lru_cache
def get_local_client(username: str, password: str) -> AsyncIOMotorDatabase:
    return AsyncIOMotorClient(
        f"mongodb://{quote_plus(username)}:{quote_plus(password)}@db:27017"
    )["nelchan"]
