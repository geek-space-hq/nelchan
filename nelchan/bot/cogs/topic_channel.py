from discord.ext.commands import Bot, Cog, Context, group
from nelchan.adapter.repository_impl import (
    GuildRepositoryImplForMongo,
    TopicChannelRepositoryImplForMongo,
)
from nelchan.usecase.inputport import (
    CreateTopicChannelCategoryInputData,
    CreateTopicChannelCategoryUseCase,
    RegisterTopicChannelInputData,
    RegisterTopicChannelUseCase,
)
from nelchan.usecase.interactor import (
    CreateTopicChannelCategoryInteractor,
    RegisterTopicChannelInteractor,
)
from nelchan.usecase.presenter import (
    CreateTopicChannelCategoryPresenter,
    RegisterTopicChannelPresneter,
)


class Topic(Cog):
    def __init__(
        self,
        bot: Bot,
        create_category_usecase: CreateTopicChannelCategoryUseCase,
        register_channel_usecase: RegisterTopicChannelUseCase,
    ) -> None:
        self.bot = bot
        self.create_category_usecase = create_category_usecase
        self.register_channel_usecase = register_channel_usecase

    @group(name="world")
    async def topic(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("正確なサブコマンドを指定してよねっ！")

    @topic.command(name="init")
    async def init(self, ctx: Context, category_name: str) -> None:
        input_data = CreateTopicChannelCategoryInputData(category_name, ctx, self.bot)
        await self.create_category_usecase.handle(input_data)

    @topic.command(name="register")
    async def register_channel(self, ctx: Context):
        input_data = RegisterTopicChannelInputData(ctx, self.bot)
        await self.register_channel_usecase.handle(input_data)


def setup(bot: Bot) -> None:
    bot.add_cog(
        Topic(
            bot,
            create_category_usecase=CreateTopicChannelCategoryInteractor(
                presenter=CreateTopicChannelCategoryPresenter(),
                repository=GuildRepositoryImplForMongo("nelchan", "channel"),
            ),
            register_channel_usecase=RegisterTopicChannelInteractor(
                presenter=RegisterTopicChannelPresneter(),
                repository=TopicChannelRepositoryImplForMongo("nelchan", "channel"),
            ),
        )
    )
