import os
from typing import Optional

from firebase_admin.firestore import firestore
from nelchan.domain.model.guild import Guild
from nelchan.domain.repository import GuildRepository
from nelchan.infrasturcture.firestore import get_firestore_client


class GuildRepositoryImpl(GuildRepository):
    def __init__(self):
        env = os.environ["ENV"]

        collection_name = "guilds" if env == "prod" else "test_guilds"
        self.collection: firestore.AsyncCollectionReference = (
            get_firestore_client().collection(collection_name)
        )

    async def get_by_id(self, guild_id: str) -> Optional[Guild]:
        guild = await self.collection.where("guildId", "==", guild_id).get()
        if not guild:
            return None
        guild = guild[0]
        return Guild(guild_id=guild_id, topic_category_id=guild.get("topicCategoryId"))

    async def create(
        self, guild_id: str, topic_category_id: Optional[str] = None
    ) -> None:
        await self.collection.document().set(
            {"guildId": guild_id, "topicCategoryId": topic_category_id}
        )

    async def update(
        self, guild_id: str, topic_category_id: Optional[str] = None
    ) -> None:
        doc = await self.collection.where("guildId", "==", guild_id).get()
        await doc[0].reference.set(
            {"guildId": guild_id, "topicCategoryId": topic_category_id}
        )
