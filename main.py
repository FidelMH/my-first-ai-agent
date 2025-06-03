from ai_agents import crew
from config import DISCORD_TOKEN
from bot import Bot, intents

# ----- FIN DE LA CONFIGURATION -----


if __name__ == "__main__":


    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN manquant dans .env")
    client = Bot(crew,intents=intents)
    client.run(DISCORD_TOKEN)

    