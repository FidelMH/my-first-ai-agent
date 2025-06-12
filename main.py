import sys
from errors import ConfigError

# Remove setup_logging import, just import logger
from logging_config import logger
from ai_agents import crew
from config import DISCORD_TOKEN
from bot import Bot, intents

if __name__ == "__main__":
    # Remove setup_logging() call since it's already done in logging_config.py
    logger.debug("Test debug message")
    logger.info("Test info message")
    logger.warning("Test warning message")
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN manquant dans .env. Arrêt du programme.")
        raise RuntimeError("DISCORD_TOKEN manquant dans .env")

    logger.info("Démarrage du bot Discord...")
    try:
        client = Bot(crew, intents=intents)
        client.run(DISCORD_TOKEN)

    except ConfigError as ce:
        logger.error(f"Erreur de configuration : {ce}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erreur lors du démarrage du bot: {e}")
        raise RuntimeError("Erreur lors du démarrage du bot Discord") from e
