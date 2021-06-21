from abc import ABC, abstractmethod
from typing import Optional

from nelchan.domain.model import TopicChannelLog


class TopicChannelLogRepository(ABC):
    @abstractmethod
    async def get_latest_log_channel(
        self, channel_id: str
    ) -> Optional[TopicChannelLog]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        action: str,
        channel_id: str,
        message_id: str,
        executed_user_id: str,
        topic_title: str,
    ) -> None:
        raise NotImplementedError
