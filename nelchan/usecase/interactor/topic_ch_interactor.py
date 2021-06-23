from datetime import datetime

import discord
from discord import CategoryChannel, Forbidden
from nelchan.domain.model.guild import Guild
from nelchan.domain.repository import (
    GuildRepository,
    TopicChannelLogRepository,
    TopicChannelRepository,
)
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
from nelchan.usecase.outputport import (
    AllocateOutputData,
    AllocateOutputPort,
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
        log_repository: TopicChannelLogRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository
        self.log_repository = log_repository

    async def handle(self, input_data: SetTopicInputData):
        if input_data.title == "":
            output_data = SetTopicOutputData(input_data.ctx)
            await self.presenter.invalid_parameter(output_data)
            return

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
            await self.log_repository.create(
                action="topic_set",
                channel_id=input_data.ctx.channel.id,
                message_id=input_data.ctx.message.id,
                executed_user_id=input_data.ctx.message.author.id,
                created_at=datetime.now(),
                topic_title=input_data.title,
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
        log_repository: TopicChannelLogRepository,
    ):
        self.presenter = presenter
        self.channel_repository = channel_repository
        self.guild_repository = guild_repository
        self.log_repository = log_repository

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
            await self.log_repository.create(
                action="topic_unset",
                channel_id=input_data.ctx.channel.id,
                message_id=input_data.ctx.message.id,
                executed_user_id=input_data.ctx.message.author.id,
                created_at=datetime.now(),
                topic_title=None,
            )
            output_data = UnsetTopicOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = UnsetTopicOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = (input_data.ctx, error)
            await self.presenter.fail(output_data)


class AllocateInteractor(AllocateUseCase):
    def __init__(
        self,
        presenter: AllocateOutputPort,
        guild_repository: GuildRepository,
        channel_repository: TopicChannelRepository,
        log_repository: TopicChannelLogRepository,
    ):
        self.presenter = presenter
        self.guild_repository = guild_repository
        self.channel_repository = channel_repository
        self.log_repository = log_repository

    async def handle(self, input_data: AllocateInputData):
        if input_data.title == "":
            output_data = AllocateOutputData(input_data.ctx)
            await self.presenter.invalid_parameter(output_data)
            return
        # ワールド用カテゴリが登録されてない
        if (
            guild := await self.guild_repository.get_by_id(input_data.ctx.guild.id)
        ) is None:
            return

        guild: Guild = guild  # type: ignore
        discord_guild: discord.Guild = input_data.ctx.guild

        # 空いているチャンネルを探す
        if (
            channel := await self.channel_repository.get_vacant_channel(guild.guild_id)
        ) is None:
            # 無かったら新規作成
            try:
                created_channel = await discord_guild.create_text_channel(
                    input_data.topic_title,
                    category=discord.utils.get(
                        discord_guild.categories, id=int(guild.topic_category_id)
                    ),
                )
            except Forbidden:
                output_data = AllocateOutputData(input_data.ctx)
                await self.presenter.forbidden(output_data)
                return

            await self.channel_repository.create(
                channel_id=created_channel.id,
                guild_id=guild.guild_id,
                topic_allocated=True,
            )
            await self.log_repository.create(
                action="topic_set",
                channel_id=input_data.ctx.channel.id,
                message_id=input_data.ctx.message.id,
                executed_user_id=input_data.ctx.message.author.id,
                created_at=datetime.now(),
                topic_title=input_data.topic_title,
            )
            output_data = AllocateOutputData(
                input_data.ctx, channel_mention=created_channel.mention
            )
            await self.presenter.complete_with_create_channel(output_data)
        else:
            # 有るならそこに話題設定
            discord_channel: discord.TextChannel = discord.utils.get(
                discord_guild.channels, id=int(channel.channel_id)
            )
            try:
                await discord_channel.edit(name=input_data.topic_title)
            except Forbidden:
                output_data = AllocateOutputData(input_data.ctx)
                await self.presenter.forbidden(output_data)
                return

            await self.channel_repository.update(
                channel_id=channel.channel_id,
                guild_id=channel.guild_id,
                topic_allocated=True,
            )
            output_data = AllocateOutputData(
                input_data.ctx, channel_mention=discord_channel.mention
            )
            await self.presenter.complete(output_data)
