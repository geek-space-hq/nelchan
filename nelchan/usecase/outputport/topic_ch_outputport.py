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
    async def fail(
        self, output_data: CreateTopicChannelCategoryOutputData, error: Exception
    ):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: CreateTopicChannelCategoryOutputData):
        raise NotImplementedError


@dataclass
class RegisterTopicChannelOutputData:
    ctx: Context
    error: Optional[Exception] = None


class RegisterTopicChannelOutputPort(ABC):
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
    async def fail(self, output_data: RegisterTopicChannelOutputData, error: Exception):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: RegisterTopicChannelOutputData):
        raise NotImplementedError
