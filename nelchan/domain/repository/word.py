from abc import ABC, abstractmethod
from typing import Optional

from nelchan.domain.model import Word


class WordRepository(ABC):
    @abstractmethod
    async def get_by_keyword(self, keyword: str) -> Optional[Word]:
        raise NotImplementedError

    @abstractmethod
    async def create_or_update(self, key: str, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError
