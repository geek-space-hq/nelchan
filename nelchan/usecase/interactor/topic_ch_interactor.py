import discord
from discord import CategoryChannel, Forbidden
from nelchan.domain.repository.guild import GuildRepository
from nelchan.domain.repository.topic_ch import TopicChannelRepository
from nelchan.usecase.inputport import (
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
from nelchan.usecase.outputport import (
    CreateTopicChannelCategoryOutputData,
    CreateTopicChannelCategoryOutputPort,
    InitTopicChannelCategoryOutputData,
    InitTopicChannelCategoryOutputPort,
    RegisterTopicChannelOutputData,
    RegisterTopicChannelOutputPort,
    SetTopicOutputData,
    SetTopicOutputPort,
    UnregisterTopicChannelOutputData,
    UnregisterTopicChannelOutputPort,
    UnsetTopicOutputData,
    UnsetTopicOutputPort,
)


class CreateTopicChannelCategoryInteractor(CreateTopicChannelCategoryUseCase):
    def __init__(
        self,
        presenter: CreateTopicChannelCategoryOutputPort,
        repository: GuildRepository,
    ):
        self.presenter = presenter
        self.repository = repository

    async def handle(self, input_data: CreateTopicChannelCategoryInputData):
        try:
            # 既にカテゴリが存在する場合
            if await self.repository.get_by_id(input_data.ctx.guild.id):
                output_data = InitTopicChannelCategoryOutputData(input_data.ctx)
                await self.presenter.already_exist(output_data)
                return
            category = await input_data.ctx.guild.create_category(
                input_data.category_name, position=100
            )
            await self.repository.create(
                guild_id=input_data.ctx.guild.id, topic_category_id=category.id
            )
            output_data = InitTopicChannelCategoryOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = InitTopicChannelCategoryOutputData(input_data.ctx)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = InitTopicChannelCategoryOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)


class InitTopicChannelCategoryInteractor(InitTopicChannelCategoryUseCase):
    def __init__(
        self,
        presenter: InitTopicChannelCategoryOutputPort,
        repository: GuildRepository,
    ):
        self.presenter = presenter
        self.repository = repository

    async def handle(self, input_data: InitTopicChannelCategoryInputData):
        try:
            # 既にカテゴリが存在する場合
            if await self.repository.get_by_id(input_data.ctx.guild.id):
                output_data = CreateTopicChannelCategoryOutputData(input_data.ctx)
                await self.presenter.already_exist(output_data)
                return
            category = discord.utils.get(
                input_data.ctx.guild.categories, id=int(input_data.category_id)
            )
            if not isinstance(category, CategoryChannel):
                print(input_data.category_id)
                return
            await self.repository.create(
                guild_id=input_data.ctx.guild.id, topic_category_id=category.id
            )
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)


class RegisterTopicChannelInteractor(RegisterTopicChannelUseCase):
    def __init__(
        self,
        presenter: RegisterTopicChannelOutputPort,
        channel_repository: TopicChannelRepository,
        guild_repository: GuildRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository

    async def handle(self, input_data: RegisterTopicChannelInputData):
        channel_id = input_data.ctx.channel.id
        # ワールドカテゴリが存在しない場合
        if (
            guild := await self.guild_repository.get_by_id(input_data.ctx.guild.id)
        ) is None:
            output_data = RegisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.category_is_not_exist(output_data)
            return

        # ワールドカテゴリ内にチャンネルが存在しない場合
        elif guild.topic_category_id != input_data.ctx.channel.category.id:
            output_data = RegisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.not_world_category(output_data)
            return

        # 既に登録されている場合
        if await self.channel_repository.get_by_id(channel_id):
            output_data = RegisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.already_registered(output_data)
            return
        try:
            await self.channel_repository.create(
                channel_id=channel_id, guild_id=input_data.ctx.guild.id
            )
            output_data = RegisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = RegisterTopicChannelOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = RegisterTopicChannelOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)


class UnregisterTopicChannelInteractor(UnregisterTopicChannelUseCase):
    def __init__(
        self,
        presenter: UnregisterTopicChannelOutputPort,
        channel_repository: TopicChannelRepository,
        guild_repository: GuildRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository

    async def handle(self, input_data: UnregisterTopicChannelInputData):
        channel_id = input_data.ctx.channel.id
        # ワールドカテゴリが存在しない場合
        if (
            guild := await self.guild_repository.get_by_id(input_data.ctx.guild.id)
        ) is None:
            output_data = UnregisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.category_is_not_exist(output_data)
            return

        # ワールドカテゴリ内にチャンネルが存在しない場合
        elif guild.topic_category_id != input_data.ctx.channel.category.id:
            output_data = UnregisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.not_world_category(output_data)
            return

        # そもそも登録されていない場合
        if await self.channel_repository.get_by_id(channel_id) is None:
            output_data = UnregisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.not_registered(output_data)
            return
        try:
            await self.channel_repository.delete(channel_id)
            output_data = UnregisterTopicChannelOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = UnregisterTopicChannelOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = UnregisterTopicChannelOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)


class SetTopicInteractor(SetTopicUseCase):
    def __init__(
        self,
        presenter: SetTopicOutputPort,
        channel_repository: TopicChannelRepository,
        guild_repository: GuildRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository

    async def handle(self, input_data: SetTopicInputData):
        # ワールド用カテゴリが登録されていない、またはチャンネルが登録されていない場合
        if (
            await self.guild_repository.get_by_id(input_data.ctx.guild.id) is None
            or (
                channel := await self.channel_repository.get_by_id(
                    input_data.ctx.channel.id
                )
            )
            is None
        ):
            return

        # 既に話題設定されている場合
        if channel.topic_allocated:
            output_data = SetTopicOutputData(input_data.ctx)
            await self.presenter.topic_already_allocated(output_data)
            return

        try:
            await input_data.ctx.channel.edit(name=input_data.title)
            await self.channel_repository.update(
                input_data.ctx.channel.id,
                guild_id=input_data.ctx.guild.id,
                topic_allocated=True,
            )
            output_data = SetTopicOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = SetTopicOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = SetTopicOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)


class UnsetTopicInteractor(UnsetTopicUseCase):
    def __init__(
        self,
        presenter: UnsetTopicOutputPort,
        channel_repository: TopicChannelRepository,
        guild_repository: GuildRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository

    async def handle(self, input_data: UnsetTopicInputData):
        # ワールド用カテゴリが登録されていない、またはチャンネルが登録されていない場合
        if (
            await self.guild_repository.get_by_id(input_data.ctx.guild.id) is None
            or (
                channel := await self.channel_repository.get_by_id(
                    input_data.ctx.channel.id
                )
            )
            is None
        ):
            return

        # 話題設定されていない場合
        if not channel.topic_allocated:
            output_data = UnsetTopicOutputData(input_data.ctx)
            await self.presenter.topic_not_allocated(output_data)
            return

        try:
            await input_data.ctx.channel.edit(name="_")
            await self.channel_repository.update(
                input_data.ctx.channel.id,
                guild_id=input_data.ctx.guild.id,
                topic_allocated=False,
            )
            output_data = UnsetTopicOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = UnsetTopicOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = (input_data.ctx, error)
            await self.presenter.fail(output_data)
