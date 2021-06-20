from discord import Message
from discord.ext.commands import Bot, Cog, Context, group
from nelchan.adapter.repository_impl.word import WordRepositoryImplForDev
from nelchan.usecase.inputport import (
    AddInputData,
    AddUseCase,
    DeleteInputData,
    DeleteUseCase,
    ResponseInputData,
    ResponseUseCase,
)
from nelchan.usecase.interactor.dictionary_interactor import (
    AddInteractor,
    DeleteInteractor,
    ResponseInteractor,
)
from nelchan.usecase.presenter.dictionary_presenter import (
    AddPresenter,
    DeletePresenter,
    ResponsePresenter,
)


class Dictionary(Cog):
    def __init__(
        self,
        bot: Bot,
        add_usecase: AddUseCase,
        delete_usecase: DeleteUseCase,
        response_usecase: ResponseUseCase,
    ) -> None:
        self.bot = bot
        self.add_usecase = add_usecase
        self.delete_usecase = delete_usecase
        self.response_usecase = response_usecase

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        input_data = ResponseInputData(message)
        await self.response_usecase.handle(input_data)

    @group(name="dict", aliases=["d"])
    async def dictionary(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("正確なサブコマンドを指定してよねっ！")

    @dictionary.command(name="add")
    async def add(self, ctx: Context, key: str, value: str) -> None:
        input_data = AddInputData(key, value, ctx)
        await self.add_usecase.handle(input_data)

    @dictionary.command(name="delete", aliases=["del", "remove", "rm"])
    async def delete(self, ctx: Context, key: str) -> None:
        input_data = DeleteInputData(key, ctx)
        await self.delete_usecase.handle(input_data)


def setup(bot: Bot) -> None:
    import os  # pylint: disable=import-outside-toplevel

    environment = os.environ["ENV"]
    if environment == "dev":
        repository = WordRepositoryImplForDev()
    elif environment == "prod":
        # repository = WordRepositoryImpl("nelchan")
        repository = WordRepositoryImplForDev()

    bot.add_cog(
        Dictionary(
            bot,
            add_usecase=AddInteractor(repository=repository, presenter=AddPresenter()),
            delete_usecase=DeleteInteractor(
                repository=repository, presenter=DeletePresenter()
            ),
            response_usecase=ResponseInteractor(
                repository=repository, presenter=ResponsePresenter(), bot=bot
            ),
        )
    )
