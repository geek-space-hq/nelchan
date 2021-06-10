from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection
from nelchan.domain.model.guild import Guild
from nelchan.domain.repository import GuildRepository
from nelchan.infrasturcture.mongo import get_local_client


class GuildRepositoryImplForMongo(GuildRepository):
    def __init__(self, mongo_username: str, mongo_password: str):
        self.collection: AsyncIOMotorCollection = get_local_client(
            mongo_username, mongo_password
        ).guilds

    async def get_by_id(self, guild_id: str) -> Optional[Guild]:
        guild = await self.collection.find_one({"guildId": guild_id})
        if not guild:
            return None
        return Guild(guild_id=guild_id, topic_category_id=guild["topicCategoryId"])

    async def create(
        self, guild_id: str, topic_category_id: Optional[str] = None
    ) -> None:
        await self.collection.insert_one(
            {"guildId": guild_id, "topicCategoryId": topic_category_id}
        )

    async def update(self, guild_id: str, topic_category_id: Optional[str]) -> None:
        await self.collection.update_one(
            {"guildId": guild_id}, {"topicCategoryId": topic_category_id}
        )
