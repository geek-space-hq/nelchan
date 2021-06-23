from nelchan.usecase.outputport import (
    AddOutputData,
    AddOutputPort,
    DeleteOutputData,
    DeleteOutputPort,
    ResponseOutputData,
    ResponseOutputPort,
)


class AddPresenter(AddOutputPort):
    async def invalid_parameter(self, output_data: AddOutputData):
        await output_data.ctx.send("あ！今悪いことしようとしましたね！！！！")

    async def complete(self, output_data: AddOutputData):
        await output_data.ctx.send(
            f"「{output_data.key}」は「{output_data.value}」なんですね...なるほど......"
        )


class DeletePresenter(DeleteOutputPort):
    async def word_not_found(self, output_data: DeleteOutputData):
        await output_data.ctx.send(f"{output_data.key}...？知らない子ですね・・・")

    async def complete(self, output_data: DeleteOutputData):
        await output_data.ctx.send(f"{output_data.key}のことはもう忘れました！しーらない！")


class ResponsePresenter(ResponseOutputPort):
    async def complete(self, output_data: ResponseOutputData):
        await output_data.message.channel.send(output_data.response_text)
