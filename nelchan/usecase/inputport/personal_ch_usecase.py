from abc import ABC, abstractmethod
from dataclasses import dataclass

from discord.ext.commands import Bot, Context


@dataclass
class CreateCategoryForPersonalChannelInputData:
    category_name: str
    ctx: Context
    bot: Bot


class CreateCategoryForPersonalChannelUseCase(ABC):
    @abstractmethod
    async def handle(
        self, input_data: CreateCategoryForPersonalChannelInputData
    ) -> None:
        raise NotImplementedError
