
from config import DISCORD_TOKEN
from bot import Bot, intents

# ----- FIN DE LA CONFIGURATION -----


if __name__ == "__main__":



    client = Bot(intents=intents)
    client.run(DISCORD_TOKEN)

    