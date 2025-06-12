import logging
import sys
from logging.handlers import RotatingFileHandler

# ----- CONFIGURATION DU LOGGING -----


def setup_logging():
    """
    Configure le logging pour le bot Discord.
    Les messages de log seront écrits dans un fichier et affichés dans la
    console.
    """
    # Création du logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Formatage des logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler pour fichier
    file_handler = None
    try:
        file_handler = RotatingFileHandler(
            "bot.log",
            maxBytes=1024 * 1024,
            backupCount=5,
            encoding="utf-8",  # 1MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
    except OSError as e:
        # If the log file can't be created, continue with console logging
        logger.error(f"Impossible de créer le fichier de log : {e}")

    # Handler pour console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Ajout des handlers au logger
    logger.addHandler(console_handler)
    if file_handler:
        logger.addHandler(file_handler)

    # Évite la propagation des logs aux loggers parents
    logger.propagate = False

    return logger


# Création d'une instance du logger
logger = setup_logging()
