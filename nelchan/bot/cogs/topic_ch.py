from discord.ext.commands import Bot, Cog, Context, group
from nelchan.adapter.repository_impl import (
    GuildRepositoryImpl,
    TopicChannelLogRepositoryImpl,
    TopicChannelRepositoryImpl,
)
from nelchan.presenter import (
    AllocatePresenter,
    CreateTopicChannelCategoryPresenter,
    InitTopicChannelCategoryPresenter,
    RegisterTopicChannelPresneter,
    SetTopicPresenter,
    UnregisterTopicChannelPresneter,
    UnsetTopicPresenter,
)
from nelchan.usecase import outputport
from nelchan.usecase.inputport import (
    AllocateInputData,
    AllocateUseCase,
    CreateTopicChannelCategoryInputData,
    CreateTopicChannelCategoryUseCase,
    InitTopicChannelCategoryInputData,
    InitTopicChannelCategoryUseCase,
    RegisterTopicChannelInputData,
    RegisterTopicChannelUseCase,
    SetTopicInputData,
    SetTopicUseCase,
    UnregisterTopicChannelInputData,
    UnregisterTopicChannelUseCase,
    UnsetTopicInputData,
    UnsetTopicUseCase,
)
from nelchan.usecase.interactor import (
    AllocateInteractor,
    CreateTopicChannelCategoryInteractor,
    InitTopicChannelCategoryInteractor,
    RegisterTopicChannelInteractor,
    SetTopicInteractor,
    UnregisterTopicChannelInteractor,
    UnsetTopicInteractor,
)


class Topic(Cog):
    def __init__(
        self,
        bot: Bot,
        create_category_usecase: CreateTopicChannelCategoryUseCase,
        init_category_usecase: InitTopicChannelCategoryUseCase,
        register_channel_usecase: RegisterTopicChannelUseCase,
        unregister_channel_usecase: UnregisterTopicChannelUseCase,
        set_topic_usecase: SetTopicUseCase,
        unset_topic_usecase: UnsetTopicUseCase,
        allocate_usecase: AllocateUseCase,
    ) -> None:
        self.bot = bot
        self.create_category_usecase = create_category_usecase
        self.register_channel_usecase = register_channel_usecase
        self.unregister_channel_usecase = unregister_channel_usecase
        self.set_topic_usecase = set_topic_usecase
        self.unset_topic_usecase = unset_topic_usecase
        self.init_category_usecase = init_category_usecase
        self.allocate_usecase = allocate_usecase

    @group(name="world", aliases=["w"])
    async def topic(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("??????????????????????????????????????????????????????")

    @topic.command(name="new")
    async def new_world(self, ctx: Context, category_name: str) -> None:
        """??????????????????????????????????????????????????????"""
        input_data = CreateTopicChannelCategoryInputData(category_name, ctx, self.bot)
        await self.create_category_usecase.handle(input_data)

    @topic.command(name="init")
    async def init_world(self, ctx: Context, category_id: str) -> None:
        """??????????????????????????????????????????????????????"""
        input_data = InitTopicChannelCategoryInputData(category_id, ctx, self.bot)
        await self.init_category_usecase.handle(input_data)

    @topic.command(name="register")
    async def register_channel(self, ctx: Context):
        """???????????????????????????????????????????????????????????????"""
        input_data = RegisterTopicChannelInputData(ctx, self.bot)
        await self.register_channel_usecase.handle(input_data)

    @topic.command(name="unregister")
    async def unregister_channel(self, ctx: Context):
        """??????????????????????????????????????????????????????????????????"""
        input_data = UnregisterTopicChannelInputData(ctx, self.bot)
        await self.unregister_channel_usecase.handle(input_data)

    @topic.command(name="set", aliases=["s"])
    async def set_topic(self, ctx: Context, topic_title: str):
        """????????????????????????"""
        input_data = SetTopicInputData(topic_title, ctx, self.bot)
        await self.set_topic_usecase.handle(input_data)

    @topic.command(name="unset", aliases=["us"])
    async def unset_topic(self, ctx: Context):
        """??????????????????????????????"""
        input_data = UnsetTopicInputData(ctx, self.bot)
        await self.unset_topic_usecase.handle(input_data)

    @topic.command(name="alloc", allias=["al"])
    async def allocate(self, ctx: Context, category_name: str):
        """????????????????????????????????????????????????????????????????????????"""
        input_data = AllocateInputData(category_name, ctx, self.bot)
        await self.allocate_usecase.handle(input_data)


def setup(bot: Bot) -> None:
    guild_repository = GuildRepositoryImpl()
    channel_repository = TopicChannelRepositoryImpl()
    log_repository = TopicChannelLogRepositoryImpl()

    bot.add_cog(
        Topic(
            bot,
            create_category_usecase=CreateTopicChannelCategoryInteractor(
                outputport=CreateTopicChannelCategoryPresenter(),
                repository=guild_repository,
            ),
            register_channel_usecase=RegisterTopicChannelInteractor(
                outputport=RegisterTopicChannelPresneter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            unregister_channel_usecase=UnregisterTopicChannelInteractor(
                outputport=UnregisterTopicChannelPresneter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            set_topic_usecase=SetTopicInteractor(
                outputport=SetTopicPresenter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
                log_repository=log_repository,
            ),
            unset_topic_usecase=UnsetTopicInteractor(
                outputport=UnsetTopicPresenter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
                log_repository=log_repository,
            ),
            init_category_usecase=InitTopicChannelCategoryInteractor(
                outputport=InitTopicChannelCategoryPresenter(),
                repository=guild_repository,
            ),
            allocate_usecase=AllocateInteractor(
                outputport=AllocatePresenter(),
                guild_repository=guild_repository,
                channel_repository=channel_repository,
                log_repository=log_repository,
            ),
        )
    )
