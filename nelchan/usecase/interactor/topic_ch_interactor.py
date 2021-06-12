from discord import Forbidden
from nelchan.domain.repository.guild import GuildRepository
from nelchan.domain.repository.topic_ch import TopicChannelRepository
from nelchan.usecase.inputport import (
    CreateTopicChannelCategoryInputData,
    CreateTopicChannelCategoryUseCase,
    RegisterTopicChannelInputData,
    RegisterTopicChannelUseCase,
)
from nelchan.usecase.outputport import (
    CreateTopicChannelCategoryOutputData,
    CreateTopicChannelCategoryOutputPort,
    RegisterTopicChannelOutputData,
    RegisterTopicChannelOutputPort,
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
                output_data = CreateTopicChannelCategoryOutputData(input_data.ctx)
                await self.presenter.already_exist(output_data)
                return
            category = await input_data.ctx.guild.create_category(
                input_data.category_name, position=100
            )
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
        try:
            # 既に登録されている場合
            if await self.channel_repository.get_by_id(channel_id):
                output_data = RegisterTopicChannelOutputData(input_data.ctx)
                self.presenter.already_registered(output_data)
                return
            # ワールドカテゴリに属したチャンネルでない場合
            elif (
                await self.guild_repository.get_by_id()
            ).topic_category_id == input_data.ctx.category.id:
                output_data = RegisterTopicChannelOutputData(input_data.ctx)
                self.presenter.not_world_category(output_data)
                return
            await self.channel_repository.create(
                channel_id=channel_id, guild_id=input_data.ctx.guild.id
            )
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as error:
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx, error)
            await self.presenter.forbidden(output_data)
        except Exception as error:
            output_data = CreateTopicChannelCategoryOutputData(input_data.ctx, error)
            await self.presenter.fail(output_data)
