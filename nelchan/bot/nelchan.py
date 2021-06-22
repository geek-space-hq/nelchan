from discord.ext.commands import Bot, when_mentioned_or

COGS = ["ready", "topic_ch", "dictionary"]


class NelChan(Bot):
    def __init__(
        self,
        commands_prefix: tuple[str, ...] = ("nel,", "Nel,", "nel, ", "Nel, ", "ねる、"),
    ):
        super().__init__(command_prefix=when_mentioned_or(*commands_prefix))

        for cog in COGS:
            self.load_extension("nelchan.bot.cogs." + cog)
