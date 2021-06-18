from abc import ABC, abstractmethod
from typing import Optional

from nelchan.domain.model.guild import Guild


class GuildRepository(ABC):
    @abstractmethod
    async def get_by_id(self, guild_id: str) -> Optional[Guild]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, guild_id: str, topic_category_id: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, guild_id: str, topic_category_id: Optional[str] = None
    ) -> None:
        raise NotImplementedError
