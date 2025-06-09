from dotenv import load_dotenv
import os

from errors import ConfigError

# ----- UNE SEULE FOIS -----
load_dotenv()  # Charge le .env dans l'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
LLM_API = os.getenv("LLM_API")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# ----- FIN DE LA CONFIGURATION -----
# Vérification des variables d'environnement
if not DISCORD_TOKEN:
    raise ConfigError("Le token Discord n'est pas défini dans le fichier .env")
if not OLLAMA_MODEL:
    raise ConfigError("Le modèle OLLAMA n'est pas défini dans le fichier .env")
if not LLM_API:
    raise ConfigError("L'URL de l'API LLM n'est pas définie dans le fichier .env")
if not GOOGLE_CSE_ID:
    raise ConfigError("L'ID de la recherche personnalisée Google n'est pas défini dans le fichier .env")
if not GOOGLE_API_KEY:
    raise ConfigError("La clé API Google n'est pas définie dans le fichier .env")

