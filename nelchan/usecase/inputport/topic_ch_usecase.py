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
class InitTopicChannelCategoryInputData:
    category_id: str
    ctx: Context
    bot: Bot


class InitTopicChannelCategoryUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: InitTopicChannelCategoryInputData) -> None:
        raise NotImplementedError


@dataclass
class RegisterTopicChannelInputData:
    ctx: Context
    bot: Bot


class RegisterTopicChannelUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: RegisterTopicChannelInputData) -> None:
        raise NotImplementedError


@dataclass
class UnregisterTopicChannelInputData:
    ctx: Context
    bot: Bot


class UnregisterTopicChannelUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: UnregisterTopicChannelInputData) -> None:
        raise NotImplementedError


@dataclass
class SetTopicInputData:
    title: str
    ctx: Context
    bot: Bot


class SetTopicUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: SetTopicInputData) -> None:
        raise NotImplementedError


@dataclass
class UnsetTopicInputData:
    ctx: Context
    bot: Bot


class UnsetTopicUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: UnsetTopicInputData) -> None:
        raise NotImplementedError


@dataclass
class AllocateInputData:
    category_name: str
    ctx: Context
    bot: Bot


class AllocateUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: AllocateInputData) -> None:
        raise NotImplementedError
