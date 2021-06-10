from nelchan.usecase.outputport import (
    CreateTopicChannelCategoryOutputData,
    CreateTopicChannelCategoryOutputPort,
    RegisterTopicChannelOutputData,
    RegisterTopicChannelOutputPort,
)


class CreateTopicChannelCategoryPresenter(CreateTopicChannelCategoryOutputPort):
    async def already_exist(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("ワールド用のカテゴリは既に存在します")

    async def forbidden(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("カテゴリーを作成しました")


class RegisterTopicChannelPresneter(RegisterTopicChannelOutputPort):
    async def not_world_category(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルはワールドに属していません")

    async def already_registered(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルは既にワールドとして登録済みです")

    async def forbidden(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルをワールドとして登録しました！")
