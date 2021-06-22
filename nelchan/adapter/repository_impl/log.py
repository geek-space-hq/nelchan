from datetime import datetime, timedelta, timezone
from typing import Optional

from firebase_admin.firestore import firestore
from motor.motor_asyncio import AsyncIOMotorCollection
from nelchan.domain.model import TopicChannelLog
from nelchan.domain.repository import TopicChannelLogRepository
from nelchan.infrasturcture.firestore import get_firestore_client
from nelchan.infrasturcture.mongo import get_local_client
from pymongo import DESCENDING

TZ_JST = timezone(timedelta(hours=9))


class TopicChannelLogRepositoryImpl(TopicChannelLogRepository):
    def __init__(self, project_id):
        self.collection: firestore.AsyncCollectionReference = get_firestore_client(
            project_id
        ).collection("TopicChannelLogs")

    async def get_latest_log_channel(
        self, channel_id: str
    ) -> Optional[TopicChannelLog]:
        log = (
            await self.collection.where("channelId", "==", channel_id)
            .limit_to_last(1)
            .get()
        )
        if not log:
            return None

        log: firestore.DocumentSnapshot = log[0]  # type: ignore
        created_at_raw = log.get("createdAt")
        return TopicChannelLog(
            action=log.get("action"),
            channel_id=log.get("channelId"),
            message_id=log.get("messageId"),
            executed_user_id=log.get("executedUserId"),
            created_at=datetime(
                created_at_raw.year,
                created_at_raw.month,
                created_at_raw.day,
                created_at_raw.hour,
                created_at_raw.minute,
                created_at_raw.second,
                created_at_raw.microsecond,
                TZ_JST,
            ),
            topic_title=log.get("topicTitle"),
        )

    async def create(
        self,
        action: str,
        channel_id: str,
        message_id: str,
        executed_user_id: str,
        created_at: datetime,
        topic_title: Optional[str] = None,
    ) -> None:
        await self.collection.document().set(
            {
                "action": action,
                "channelId": channel_id,
                "messageId": message_id,
                "executedUserId": executed_user_id,
                "createdAt": created_at,
                "topicTitle": topic_title,
            }
        )


class TopicChannelLogRepositoryImplForMongo(TopicChannelLogRepository):
    def __init__(self, mongo_username: str, mongo_password: str):
        self.collection: AsyncIOMotorCollection = get_local_client(
            mongo_username, mongo_password
        ).topicChannelLogs

    async def get_latest_log_channel(
        self, channel_id: str
    ) -> Optional[TopicChannelLog]:
        log = await self.collection.find_one({"channelId": channel_id}, sort=DESCENDING)
        if not log:
            return None

        return TopicChannelLog(
            action=log["action"],
            channel_id=log["channelId"],
            message_id=log["messageId"],
            executed_user_id=log["executedUserId"],
            created_at=log["createdAt"],
            topic_title=log["topicTitle"],
        )

    async def create(
        self,
        action: str,
        channel_id: str,
        message_id: str,
        executed_user_id: str,
        created_at: datetime,
        topic_title: Optional[str] = None,
    ) -> None:
        await self.collection.insert_one(
            {
                "action": action,
                "channelId": channel_id,
                "messageId": message_id,
                "executedUserId": executed_user_id,
                "topicTitle": topic_title,
                "createdAt": created_at,
            }
        )
