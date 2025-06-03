# tests/test_handlers.py
import sys
sys.path.append('../')
# tests/test_handlers.py

import pytest
import asyncio
from types import SimpleNamespace

from handlers import on_message_handler

# --- Doubles Discord (Bot / Message / Channel) ---

class FakeChannel:
    """
    Simule un channel Discord avec :
    - typing() pour simuler l'indicateur "typing"
    - reply() pour capturer la réponse dans last_reply
    """
    def __init__(self):
        self.last_reply = None

    async def typing(self):
        # On ne fait rien, c'est juste un placeholder
        pass

    async def reply(self, text):
        self.last_reply = text


class FakeMessage:
    """
    Simule un discord.Message minimal :
    - content : texte exact renvoyé
    - author  : objet avec au moins .id
    - channel : instance de FakeChannel
    """
    def __init__(self, content, author, channel):
        self.content = content
        self.author = author
        self.channel = channel

    async def reply(self, text):
        # Délègue à channel.reply pour stocker le texte
        await self.channel.reply(text)


class FakeBot:
    """
    Simule un Bot Discord :
    - .user.id pour comparer avec message.author
    - .crew.kickoff_async() représentant l'appel à l'IA
    """
    def __init__(self, crew, user_id=12345):
        self.crew = crew
        self.user = SimpleNamespace(id=user_id)


# --- Fixtures créant différents comportements de kickoff_async ---

@pytest.fixture
def fake_crew_raw():
    """
    kickoff_async renvoie un objet possédant .raw
    """
    class RawResponse:
        def __init__(self, text):
            self.raw = text

    class Crew:
        async def kickoff_async(self, inputs):
            # Retourne un objet avec attribut .raw
            return RawResponse("Réponse brute IA")

    return Crew()


@pytest.fixture
def fake_crew_timeout_error():
    """
    kickoff_async lève TimeoutError
    """
    class Crew:
        async def kickoff_async(self, inputs):
            raise TimeoutError("Le service a mis trop de temps à répondre")

    return Crew()


@pytest.fixture
def fake_crew_connection_error():
    """
    kickoff_async lève ConnectionError
    """
    class Crew:
        async def kickoff_async(self, inputs):
            raise ConnectionError("Impossible de joindre l'API LLM")

    return Crew()


@pytest.fixture
def fake_crew_generic_exception():
    """
    kickoff_async lève une autre Exception imprévue
    """
    class Crew:
        async def kickoff_async(self, inputs):
            raise RuntimeError("Erreur inattendue")

    return Crew()


# --- Tests unitaires ---

@pytest.mark.asyncio
async def test_ignore_message_from_bot(fake_crew_raw):
    """
    Si message.author == bot.user, on ne fait rien : kickoff_async n'est pas appelé
    et channel.last_reply reste None.
    """
    bot = FakeBot(fake_crew_raw, user_id=1)
    author = SimpleNamespace(id=1)  # même ID que bot.user.id
    channel = FakeChannel()
    message = FakeMessage("!ai Salut", author=author, channel=channel)

    # On remplace kickoff_async par un stub qui lève si jamais appelé
    async def fake_kickoff(inputs):
        raise AssertionError("kickoff_async ne doit pas être appelé")
    bot.crew.kickoff_async = fake_kickoff

    await on_message_handler(bot, message)
    assert channel.last_reply is None


@pytest.mark.asyncio
async def test_ignore_non_ai_prefix(fake_crew_raw):
    """
    Si le message ne commence pas par "!ai ", on ne fait rien (pas de reply).
    """
    bot = FakeBot(fake_crew_raw)
    author = SimpleNamespace(id=2)
    channel = FakeChannel()
    message = FakeMessage("Bonjour tout le monde", author=author, channel=channel)

    # Même stub pour kickoff_async
    async def fake_kickoff(inputs):
        raise AssertionError("kickoff_async ne doit pas être appelé")
    bot.crew.kickoff_async = fake_kickoff

    await on_message_handler(bot, message)
    assert channel.last_reply is None


@pytest.mark.asyncio
async def test_prompt_too_long(fake_crew_raw):
    """
    Si prompt > 500 caractères (par ex. 501 'a'), on renvoie 
    'Votre question est trop longue (500 caractères max).' et on n'appelle pas kickoff_async.
    """
    long_prompt = "a" * 501
    bot = FakeBot(fake_crew_raw)
    author = SimpleNamespace(id=3)
    channel = FakeChannel()
    message = FakeMessage(f"!ai {long_prompt}", author=author, channel=channel)

    async def fake_kickoff(inputs):
        raise AssertionError("kickoff_async ne doit pas être appelé pour un prompt trop long")
    bot.crew.kickoff_async = fake_kickoff

    await on_message_handler(bot, message)
    assert channel.last_reply == "Votre question est trop longue (500 caractères max)."


@pytest.mark.asyncio
async def test_valid_prompt_returns_raw_response(fake_crew_raw):
    """
    Pour un prompt valide (ex. 'Hello'), kickoff_async renvoie un objet .raw,
    on doit envoyer response.raw dans le canal.
    """
    bot = FakeBot(fake_crew_raw)
    author = SimpleNamespace(id=4)
    channel = FakeChannel()
    message = FakeMessage("!ai Hello", author=author, channel=channel)

    # Pas besoin de stub, on utilise la fixture fake_crew_raw telle quelle
    # qui renvoie un objet avec .raw = "Réponse brute IA"
    await on_message_handler(bot, message)
    assert channel.last_reply == "Réponse brute IA"


@pytest.mark.asyncio
async def test_timeout_error_from_kickoff(fake_crew_timeout_error):
    """
    Si kickoff_async lève TimeoutError, on doit renvoyer
    'Une erreur s\'est produite lors de l\'appel à l\'IA.'
    """
    bot = FakeBot(fake_crew_timeout_error)
    author = SimpleNamespace(id=5)
    channel = FakeChannel()
    message = FakeMessage("!ai test timeout", author=author, channel=channel)

    await on_message_handler(bot, message)
    assert channel.last_reply == "Une erreur s'est produite lors de l'appel à l'IA."


@pytest.mark.asyncio
async def test_connection_error_from_kickoff(fake_crew_connection_error):
    """
    Si kickoff_async lève ConnectionError, on doit renvoyer
    'Service IA indisponible, veuillez réessayer plus tard.'
    """
    bot = FakeBot(fake_crew_connection_error)
    author = SimpleNamespace(id=6)
    channel = FakeChannel()
    message = FakeMessage("!ai test connection", author=author, channel=channel)

    await on_message_handler(bot, message)
    assert channel.last_reply == "Service IA indisponible, veuillez réessayer plus tard."


@pytest.mark.asyncio
async def test_generic_exception_from_kickoff(fake_crew_generic_exception):
    """
    Si kickoff_async lève une exception imprévue, on doit renvoyer
    'Une erreur inattendue s'est produite.'
    """
    bot = FakeBot(fake_crew_generic_exception)
    author = SimpleNamespace(id=7)
    channel = FakeChannel()
    message = FakeMessage("!ai test erreur", author=author, channel=channel)

    await on_message_handler(bot, message)
    assert channel.last_reply == "Une erreur inattendue s'est produite."
