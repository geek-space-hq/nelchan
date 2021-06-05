from discord.ext.commands import Bot, Cog, Context, command
from nelchan.usecase.inputport import (
    CreateCategoryForPersonalChannelInputData,
    CreateCategoryForPersonalChannelUseCase,
)
from nelchan.usecase.interactor import CreateCategoryForPersonalChannelInteractor
from nelchan.usecase.presenter import CreateCategoryForPersonalChannelPresenter


class CreateCategoryForPersonalChannel(Cog):
    def __init__(
        self, bot: Bot, usecase: CreateCategoryForPersonalChannelUseCase
    ) -> None:
        self.bot = bot
        self.usecase = usecase

    @command()
    async def init(self, ctx: Context, category_name: str) -> None:
        input_data = CreateCategoryForPersonalChannelInputData(
            category_name, ctx, self.bot
        )
        await self.usecase.handle(input_data)


def setup(bot: Bot) -> None:
    bot.add_cog(
        CreateCategoryForPersonalChannel(
            bot,
            CreateCategoryForPersonalChannelInteractor(
                CreateCategoryForPersonalChannelPresenter()
            ),
        )
    )
