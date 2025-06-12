# errors.py


class ConfigError(Exception):
    """Exception levée lorsqu'une erreur de configuration est détectée
    (token manquant, variable absente, etc.)."""

    pass


class LLMUnavailableError(Exception):
    """Exception levée lorsque le service LLM (Ollama/Mistral) n'est pas
    joignable."""

    pass


# Vous pouvez ajouter d'autres exceptions spécifiques ici si besoin.
