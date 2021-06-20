from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from discord import Message
from discord.ext.commands import Context


@dataclass
class AddOutputData:
    ctx: Context
    key: str
    value: str
    error: Optional[Exception] = None


class AddOutputPort(ABC):
    @abstractmethod
    async def complete(self, output_data: AddOutputData):
        raise NotImplementedError


@dataclass
class DeleteOutputData:
    ctx: Context
    key: str
    error: Optional[Exception] = None


class DeleteOutputPort(ABC):
    @abstractmethod
    async def word_not_found(self, output_data: DeleteOutputData):
        raise NotImplementedError

    @abstractmethod
    async def complete(self, output_data: DeleteOutputData):
        raise NotImplementedError


@dataclass
class ResponseOutputData:
    message: Message
    response_text: str
    error: Optional[Exception] = None


class ResponseOutputPort(ABC):
    @abstractmethod
    async def complete(self, output_data: ResponseOutputData):
        raise NotImplementedError
