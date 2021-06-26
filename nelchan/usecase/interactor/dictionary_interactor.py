from discord.ext.commands import Bot
from nelchan.domain.repository import WordRepository
from nelchan.usecase.inputport import (
    AddInputData,
    AddUseCase,
    DeleteInputData,
    DeleteUseCase,
    ResponseInputData,
    ResponseUseCase,
)
from nelchan.usecase.outputport import (
    AddOutputData,
    AddOutputPort,
    DeleteOutputData,
    DeleteOutputPort,
    ResponseOutputData,
    ResponseOutputPort,
)


class AddInteractor(AddUseCase):
    def __init__(self, outputport: AddOutputPort, repository: WordRepository):
        self.outputport = outputport
        self.repository = repository

    async def handle(self, input_data: AddInputData):
        if input_data.key == "" or input_data.value == "":
            output_data = AddOutputData(
                input_data.ctx, input_data.key, input_data.value
            )
            await self.outputport.invalid_parameter(output_data)
            return

        await self.repository.create_or_update(input_data.key, input_data.value)
        output_data = AddOutputData(input_data.ctx, input_data.key, input_data.value)
        await self.outputport.complete(output_data)


class DeleteInteractor(DeleteUseCase):
    def __init__(self, outputport: DeleteOutputPort, repository: WordRepository):
        self.outputport = outputport
        self.repository = repository

    async def handle(self, input_data: DeleteInputData):
        if await self.repository.get_by_keyword(input_data.key) is None:
            output_data = DeleteOutputData(input_data.ctx, input_data.key)
            await self.outputport.word_not_found(output_data)
            return

        await self.repository.delete(input_data.key)
        output_data = DeleteOutputData(input_data.ctx, input_data.key)
        await self.outputport.complete(output_data)


class ResponseInteractor(ResponseUseCase):
    def __init__(
        self, repository: WordRepository, outputport: ResponseOutputPort, bot: Bot
    ):
        self.outputport = outputport
        self.repository = repository
        self.bot = bot

    async def handle(self, input_data: ResponseInputData):
        if input_data.message.author.id == self.bot.user.id:
            return

        if (
            word := await self.repository.get_by_keyword(input_data.message.content)
        ) is None:
            return
        output_data = ResponseOutputData(input_data.message, word.value)
        await self.outputport.complete(output_data)
