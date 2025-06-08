from dotenv import load_dotenv
import os

from errors import ConfigError

# ----- UNE SEULE FOIS -----
load_dotenv()  # Charge le .env dans l'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
LLM_API = os.getenv("LLM_API")
# ----- FIN DE LA CONFIGURATION -----
# Vérification des variables d'environnement
if not DISCORD_TOKEN:
    raise ConfigError("Le token Discord n'est pas défini dans le fichier .env")
if not OLLAMA_MODEL:
    raise ConfigError("Le modèle OLLAMA n'est pas défini dans le fichier .env")
if not LLM_API:
    raise ConfigError("L'URL de l'API LLM n'est pas définie dans le fichier .env")

