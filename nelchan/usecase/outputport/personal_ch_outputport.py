from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from discord.ext.commands import Context


@dataclass
class CreateCategoryForPersonalChannelOutputData:
    ctx: Context
    error: Optional[Exception] = None


class CreateCategoryForPersonalChannelOutputPort(ABC):
    @abstractmethod
    async def forbidden(self, output_data: CreateCategoryForPersonalChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: CreateCategoryForPersonalChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: CreateCategoryForPersonalChannelOutputData):
        raise NotImplementedError
