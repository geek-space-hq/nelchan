import os
import sys

from google.cloud import secretmanager


def access_secret(project_id, secret_id, version):
    """
    Access a secret- API token, etc- stored in Secret Manager

    Code from https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#secretmanager-access-secret-version-python
    """
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = client.secret_version_path(project_id, secret_id, version)

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the secret payload
    payload = response.payload.data.decode("UTF-8")

    return payload


os.environ["ENV"] = "prod"

sys.path.append("/usr/src/app")

from nelchan import NelChan

DISCORD_BOT_TOKEN = access_secret("nelchan", "DISCORD_BOT_TOKEN", "1")

bot = NelChan()

bot.run(DISCORD_BOT_TOKEN)
