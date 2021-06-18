import os
import sys

os.environ["ENV"] = "dev"

sys.path.append("/usr/src/app")

from nelchan import NelChan

DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

bot = NelChan(commands_prefix="test,")

bot.run(DISCORD_BOT_TOKEN)
