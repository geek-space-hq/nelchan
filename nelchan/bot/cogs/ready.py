from discord.ext.commands import Bot, Cog


class Ready(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print("起動しました！")


def setup(bot: Bot) -> None:
    bot.add_cog(Ready(bot))
