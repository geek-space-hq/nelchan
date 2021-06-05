from nelchan.usecase.outputport import (
    CreateCategoryForPersonalChannelOutputData,
    CreateCategoryForPersonalChannelOutputPort,
)


class CreateCategoryForPersonalChannelPresenter(
    CreateCategoryForPersonalChannelOutputPort
):
    async def forbidden(self, output_data: CreateCategoryForPersonalChannelOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: CreateCategoryForPersonalChannelOutputData):
        await output_data.ctx.send("エラーが発生しました")

    async def complete(self, output_data: CreateCategoryForPersonalChannelOutputData):
        await output_data.ctx.send("カテゴリーを作成しました")
