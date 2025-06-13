from dotenv import load_dotenv
import os

from errors import ConfigError

# ----- UNE SEULE FOIS -----
try:
    load_dotenv()
except Exception as e:
    raise ConfigError(f"Impossible de charger le fichier .env : {e}")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OLLAMA_MISTRAL = os.getenv("OLLAMA_MISTRAL")
OLLAMA_QWEN3 = os.getenv("OLLAMA_QWEN3")
OLLAMA_DEEPSEEK_R1 = os.getenv("OLLAMA_DEEPSEEK_R1")
LLM_API = os.getenv("LLM_API")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
# ----- FIN DE LA CONFIGURATION -----
# Vérification des variables d'environnement
if not DISCORD_TOKEN:
    raise ConfigError("Le token Discord n'est pas défini dans le fichier .env")
if not OLLAMA_MISTRAL:
    raise ConfigError(
        "Le modèle OLLAMA_MISTRAL n'est pas défini dans le fichier .env"
    )
if not OLLAMA_QWEN3:
    raise ConfigError(
        "Le modèle OLLAMA_QWEN3 n'est pas défini dans le fichier .env"
    )
if not OLLAMA_DEEPSEEK_R1:
    raise ConfigError(
        "Le modèle OLLAMA_DEEPSEEK_R1 n'est pas défini dans le fichier .env"
    )
if not LLM_API:
    raise ConfigError(
        "L'URL de l'API LLM n'est pas définie dans le fichier .env"
    )
if not GOOGLE_CSE_ID:
    raise ConfigError(
        "L'ID de la recherche personnalisée Google n'est pas défini dans le "
        "fichier .env"
    )
if not GOOGLE_API_KEY:
    raise ConfigError(
        "La clé API Google n'est pas définie dans le fichier .env"
    )
if not SERPER_API_KEY:
    raise ConfigError("La clé SERPER n'est pas définie dans le fichier .env")