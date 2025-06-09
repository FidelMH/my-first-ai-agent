import sys
from errors import ConfigError
from logging_config import setup_logging, logger
from ai_agents import crew
from config import DISCORD_TOKEN
from bot import Bot, intents

# ----- FIN DE LA CONFIGURATION -----


if __name__ == "__main__":

    setup_logging()  # Assurez-vous que cette fonction est définie dans logging_config.py

    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN manquant dans .env. Arrêt du programme.")
        raise RuntimeError("DISCORD_TOKEN manquant dans .env")
    
    logger.info("Démarrage du bot Discord...")
    try:

        client = Bot(crew,intents=intents)
        client.run(DISCORD_TOKEN)

    except ConfigError as ce:
        logger.error(f"Erreur de configuration : {ce}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erreur lors du démarrage du bot: {e}")
        raise RuntimeError("Erreur lors du démarrage du bot Discord") from e    
    