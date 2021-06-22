from abc import ABC, abstractmethod
from dataclasses import dataclass

from discord import Message
from discord.ext.commands import Context


@dataclass
class AddInputData:
    key: str
    value: str
    ctx: Context


class AddUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: AddInputData) -> None:
        raise NotImplementedError


@dataclass
class DeleteInputData:
    key: str
    ctx: Context


class DeleteUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: DeleteInputData) -> None:
        raise NotImplementedError


@dataclass
class ResponseInputData:
    message: Message


class ResponseUseCase(ABC):
    @abstractmethod
    async def handle(self, input_data: ResponseInputData) -> None:
        raise NotImplementedError
