from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from discord.ext.commands import Context


@dataclass
class CreateTopicChannelCategoryOutputData:
    ctx: Context
    error: Optional[Exception] = None


class CreateTopicChannelCategoryOutputPort(ABC):
    @abstractmethod
    async def already_exist(self, output_data: CreateTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: CreateTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: CreateTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: CreateTopicChannelCategoryOutputData):
        raise NotImplementedError


@dataclass
class InitTopicChannelCategoryOutputData:
    ctx: Context
    error: Optional[Exception] = None


class InitTopicChannelCategoryOutputPort(ABC):
    @abstractmethod
    async def already_exist(self, output_data: InitTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: InitTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: InitTopicChannelCategoryOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: InitTopicChannelCategoryOutputData):
        raise NotImplementedError


@dataclass
class RegisterTopicChannelOutputData:
    ctx: Context
    error: Optional[Exception] = None


class RegisterTopicChannelOutputPort(ABC):
    @abstractmethod
    async def category_is_not_exist(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def not_world_category(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def already_registered(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError


@dataclass
class UnregisterTopicChannelOutputData:
    ctx: Context
    error: Optional[Exception] = None


class UnregisterTopicChannelOutputPort(ABC):
    @abstractmethod
    async def category_is_not_exist(
        self, output_data: UnregisterTopicChannelOutputData
    ):
        raise NotImplementedError

    @abstractmethod
    async def not_world_category(self, output_data: UnregisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def not_registered(self, output_data: UnregisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: UnregisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: UnregisterTopicChannelOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: UnregisterTopicChannelOutputData):
        raise NotImplementedError


@dataclass
class SetTopicOutputData:
    ctx: Context
    error: Optional[Exception] = None


class SetTopicOutputPort(ABC):
    @abstractmethod
    async def topic_already_allocated(self, output_data: SetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: SetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: SetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: SetTopicOutputData):
        raise NotImplementedError


@dataclass
class UnsetTopicOutputData:
    ctx: Context
    error: Optional[Exception] = None


class UnsetTopicOutputPort(ABC):
    @abstractmethod
    async def topic_not_allocated(self, output_data: UnsetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def forbidden(self, output_data: UnsetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: UnsetTopicOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: UnsetTopicOutputData):
        raise NotImplementedError


@dataclass
class AllocateOutputData:
    ctx: Context
    error: Optional[Exception] = None
    channel_mention: Optional[str] = None


class AllocateOutputPort(ABC):
    @abstractmethod
    async def forbidden(self, output_data: AllocateOutputData):
        raise NotImplementedError

    @abstractmethod
    async def fail(self, output_data: AllocateOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: AllocateOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete_with_create_channel(self, output_data: AllocateOutputData):
        raise NotImplementedError
