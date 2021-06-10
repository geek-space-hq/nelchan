from abc import ABC, abstractmethod
from typing import Optional

from nelchan.domain.model.topic_ch import TopicChannel


class TopicChannelRepository(ABC):
    @abstractmethod
    async def get_by_id(self, channel_id: str) -> TopicChannel:
        raise NotImplementedError

    @abstractmethod
    async def create(self, channel_id: str, guild_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, channel_id: str, topic_allocated: bool = False) -> None:
        raise NotImplementedError
