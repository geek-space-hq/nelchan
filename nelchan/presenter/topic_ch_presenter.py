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


class CreateTopicChannelCategoryPresenter(CreateTopicChannelCategoryOutputPort):
    async def already_exist(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("ワールド用のカテゴリは既に存在します")

    async def forbidden(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: CreateTopicChannelCategoryOutputData):
        await output_data.ctx.send("カテゴリーを作成しました")


class InitTopicChannelCategoryPresenter(InitTopicChannelCategoryOutputPort):
    async def already_exist(self, output_data: InitTopicChannelCategoryOutputData):
        await output_data.ctx.send("ワールド用のカテゴリは既に存在します")

    async def forbidden(self, output_data: InitTopicChannelCategoryOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: InitTopicChannelCategoryOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: InitTopicChannelCategoryOutputData):
        await output_data.ctx.send("ワールド用カテゴリを設定しました")


class RegisterTopicChannelPresneter(RegisterTopicChannelOutputPort):
    async def category_is_not_exist(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("ワールドカテゴリが存在しません")

    async def not_world_category(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルはワールドカテゴリに属していません")

    async def already_registered(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルは既にワールドとして登録済みです")

    async def forbidden(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルをワールドとして登録しました！")


class UnregisterTopicChannelPresneter(UnregisterTopicChannelOutputPort):
    async def category_is_not_exist(self, output_data: RegisterTopicChannelOutputData):
        await output_data.ctx.send("ワールドカテゴリが存在しません")

    async def not_world_category(self, output_data: UnregisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルはワールドカテゴリに属していません")

    async def not_registered(self, output_data: UnregisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルはワールドとして登録されていません")

    async def forbidden(self, output_data: UnregisterTopicChannelOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: UnregisterTopicChannelOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: UnregisterTopicChannelOutputData):
        await output_data.ctx.send("このチャンネルのワールド登録を解除しました")


class SetTopicPresenter(SetTopicOutputPort):
    async def invalid_parameter(self, output_data: SetTopicOutputData):
        await output_data.ctx.send("あ！今悪いことしようとしましたね！！！！")

    async def topic_already_allocated(self, output_data: SetTopicOutputData):
        await output_data.ctx.send("既に話題は設定されています")

    async def forbidden(self, output_data: SetTopicOutputData):
        await output_data.ctx.send(f"許可されていない操作です `{output_data.error}`")

    async def fail(self, output_data: SetTopicOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: SetTopicOutputData):
        await output_data.ctx.send("トピックを設定しました")


class UnsetTopicPresenter(UnsetTopicOutputPort):
    async def topic_not_allocated(self, output_data: UnsetTopicOutputData):
        await output_data.ctx.send("話題は設定されていません")

    async def forbidden(self, output_data: UnsetTopicOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: UnsetTopicOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: UnsetTopicOutputData):
        await output_data.ctx.send("トピックを削除しました")


class AllocatePresenter(AllocateOutputPort):
    async def invalid_parameter(self, output_data: AllocateOutputData):
        await output_data.ctx.send("あ！今悪いことしようとしましたね！！！！")

    async def forbidden(self, output_data: AllocateOutputData):
        await output_data.ctx.send("許可されていない操作です")

    async def fail(self, output_data: AllocateOutputData):
        await output_data.ctx.send(f"エラーが発生しました `{output_data.error}`")

    async def complete(self, output_data: AllocateOutputData):
        await output_data.ctx.send(
            f"話題を空いていたチャンネルに設定しました {output_data.channel_mention}"
        )

    async def complete_with_create_channel(self, output_data: AllocateOutputData):
        await output_data.ctx.send(
            f"空いていたチャンネルが無かったため、新しくチャンネルを作成し、そこに話題を設定しました {output_data.channel_mention}"
        )
