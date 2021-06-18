from typing import Optional

from firebase_admin.firestore import firestore
from motor.motor_asyncio import AsyncIOMotorCollection
from nelchan.domain.model.topic_ch import TopicChannel
from nelchan.domain.repository import TopicChannelRepository
from nelchan.infrasturcture.firestore import get_firestore_client
from nelchan.infrasturcture.mongo import get_local_client


class TopicChannelRepositoryImpl(TopicChannelRepository):
    def __init__(self, project_id):
        self.collection: firestore.AsyncCollectionReference = get_firestore_client(
            project_id
        ).collection("topicChannels")

    async def get_by_id(self, channel_id: str) -> Optional[TopicChannel]:
        channel = await self.collection.where("channelId", "==", channel_id).get()
        if not channel:
            return None
        channel = channel[0]
        return TopicChannel(
            channel_id=channel.get("channelId"),
            guild_id=channel.get("guildId"),
            topic_allocated=channel.get("topicAllocated"),
        )

    async def create(
        self, channel_id: str, guild_id: str, topic_allocated: bool = False
    ) -> None:
        await self.collection.document().set(
            {
                "channelId": channel_id,
                "guildId": guild_id,
                "topicAllocated": topic_allocated,
            }
        )

    async def update(
        self, channel_id: str, guild_id: str, topic_allocated: bool = False
    ) -> None:
        doc = await self.collection.where("channelId", "==", channel_id).get()
        await doc[0].reference.set(
            {
                "channelId": channel_id,
                "guildId": guild_id,
                "topicAllocated": topic_allocated,
            },
        )

    async def delete(self, channel_id: str) -> None:
        doc = await self.collection.where("channelId", "==", channel_id).get()
        await doc[0].reference.delete()

    async def get_vacant_channel(self, guild_id: str) -> Optional[TopicChannel]:
        channels_collection = (
            await self.collection.where("guildId", "==", guild_id)
            .where("topicAllocated", "==", False)
            .get()
        )
        if not channels_collection:
            return None

        channel = channels_collection[0]
        return TopicChannel(
            channel_id=channel.get("channelId"),
            guild_id=channel.get("guildId"),
            topic_allocated=channel.get("topicAllocated"),
        )


class TopicChannelRepositoryImplForMongo(TopicChannelRepository):
    def __init__(self, mongo_username: str, mongo_password: str):
        self.collection: AsyncIOMotorCollection = get_local_client(
            mongo_username, mongo_password
        ).topicChannels

    async def get_by_id(self, channel_id: str) -> Optional[TopicChannel]:
        channel = await self.collection.find_one({"channelId": channel_id})
        if not channel:
            return None
        return TopicChannel(
            channel_id=channel_id,
            guild_id=channel["guildId"],
            topic_allocated=channel["topicAllocated"],
        )

    async def create(
        self, channel_id: str, guild_id: str, topic_allocated: bool = False
    ) -> None:
        await self.collection.insert_one(
            {
                "channelId": channel_id,
                "guildId": guild_id,
                "topicAllocated": topic_allocated,
            }
        )

    async def update(
        self, channel_id: str, guild_id: str, topic_allocated: bool = False
    ) -> None:
        await self.collection.update_one(
            {"channelId": channel_id},
            {
                "$set": {
                    "guildId": guild_id,
                    "topicAllocated": topic_allocated,
                }
            },
        )

    async def delete(self, channel_id: str) -> None:
        await self.collection.delete_one({"channelId": channel_id})

    async def get_vacant_channel(self, guild_id: str) -> Optional[TopicChannel]:
        channel = await self.collection.find_one(
            {"guildId": guild_id, "topicAllocated": False}
        )
        if not channel:
            return None
        return TopicChannel(
            channel_id=channel["channelId"],
            guild_id=channel["guildId"],
            topic_allocated=channel["topicAllocated"],
        )
