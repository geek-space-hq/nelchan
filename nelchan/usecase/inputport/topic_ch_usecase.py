from abc import ABC, abstractmethod
from dataclasses import dataclass

from discord.ext.commands import Bot, Context


@dataclass
class CreateTopicChannelCategoryInputData:
    category_name: str
    ctx: Context
    bot: Bot


class CreateTopicChannelCategoryUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: CreateTopicChannelCategoryInputData) -> None:
        raise NotImplementedError


@dataclass
class RegisterTopicChannelInputData:
    ctx: Context
    bot: Bot


class RegisterTopicChannelUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: RegisterTopicChannelInputData) -> None:
        raise NotImplementedError
