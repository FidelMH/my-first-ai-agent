import logging

# ----- CONFIGURATION DU LOGGING -----
def setup_logging():
    """
    Configure le logging pour le bot Discord.
    Les messages de log seront écrits dans un fichier et affichés dans la console.
    """
    # Configure le niveau de log à INFO et le format des messages
    # Les messages seront écrits dans le fichier bot.log et affichés dans la console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
    )
logger = logging.getLogger("discord_bot")
# ----- CONFIGURATION DU LOGGING -----
# Configure le niveau de log à INFO et le format des messages
# Les messages seront écrits dans le fichier bot.log et affichés dans la console
# Crée un logger spécifique pour le bot Discord