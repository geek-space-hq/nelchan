import os
from typing import Optional

from firebase_admin.firestore import firestore
from nelchan.domain.model.topic_ch import TopicChannel
from nelchan.domain.repository import TopicChannelRepository
from nelchan.infrasturcture.firestore import get_firestore_client


class TopicChannelRepositoryImpl(TopicChannelRepository):
    def __init__(
        self,
    ):
        env = os.environ["ENV"]

        collection_name = "topicChannels" if env == "prod" else "test_topicChannels"
        self.collection: firestore.AsyncCollectionReference = (
            get_firestore_client().collection(collection_name)
        )

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
