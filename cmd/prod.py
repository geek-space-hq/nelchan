import os
import sys

from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()


os.environ["ENV"] = "prod"

sys.path.append("/usr/src/app")

from nelchan import NelChan

DISCORD_BOT_TOKEN = client.get_secret(request={"name": "DISCORD_BOT_TOKEN"})

bot = NelChan()

bot.run(DISCORD_BOT_TOKEN)
