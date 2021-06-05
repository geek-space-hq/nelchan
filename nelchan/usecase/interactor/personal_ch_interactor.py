from discord import Forbidden
from nelchan.usecase.inputport import (
    CreateCategoryForPersonalChannelInputData,
    CreateCategoryForPersonalChannelUseCase,
)
from nelchan.usecase.outputport import (
    CreateCategoryForPersonalChannelOutputData,
    CreateCategoryForPersonalChannelOutputPort,
)


class CreateCategoryForPersonalChannelInteractor(
    CreateCategoryForPersonalChannelUseCase
):
    def __init__(self, presenter: CreateCategoryForPersonalChannelOutputPort):
        self.presenter = presenter

    async def handle(self, input_data: CreateCategoryForPersonalChannelInputData):
        try:
            await input_data.ctx.guild.create_category(
                input_data.category_name, position=100
            )
            output_data = CreateCategoryForPersonalChannelOutputData(input_data.ctx)
            await self.presenter.complete(output_data)
        except Forbidden as e:
            output_data = CreateCategoryForPersonalChannelOutputData(input_data.ctx, e)
            await self.presenter.forbidden(output_data)
        except Exception as e:
            output_data = CreateCategoryForPersonalChannelOutputData(input_data.ctx, e)
            await self.presenter.fail(output_data)
