import asyncio
from logging_config import logger

MAX_PROMPT_LENGTH = 500

# Configure handler-specific logger
handler_logger = logger.getChild("handlers")


async def on_ready_handler(bot):
    handler_logger.info(f"Connecté en tant que {bot.user}")


async def send_long_message(message, content):
    """Split and send long messages respecting Discord's 2000 char limit."""
    try:
        if len(content) <= 2000:
            await message.reply(content)
            return
        # Split content into chunks of max 2000 chars
        chunks = []
        current_chunk = ""

        for line in content.split("\n"):
            if (
                len(current_chunk) + len(line) + 1 <= 1900
            ):  # Leave room for chunk indicators
                current_chunk += line + "\n"
            else:
                chunks.append(current_chunk)
                current_chunk = line + "\n"

        if current_chunk:
            chunks.append(current_chunk)

        # Send chunks with indicators
        for i, chunk in enumerate(chunks, 1):
            header = f"Part {i}/{len(chunks)}:\n"
            await message.reply(f"{header}{chunk}")
    except Exception as e:
        handler_logger.error(f"Erreur lors de l'envoi du message : {e}", exc_info=True)


async def on_message_handler(bot, message):
    handler_logger.info(f"Message reçu de {message.author}: {message.content}")
    if message.author == bot.user or not message.content.startswith("!ai "):
        return

    prompt = message.content[4:].strip()
    if not prompt:
        await message.reply("Votre question est vide.")
        return

    if len(prompt) > MAX_PROMPT_LENGTH:
        await message.reply(
            "Votre question est trop longue (500 caractères max)."
        )
        return

    inputs = {"query": prompt}
    handler_logger.debug("Prompt envoyé à l'IA")
    await message.channel.typing()

    try:
        response = await bot.crew.kickoff_async(inputs=inputs)
        handler_logger.debug("Réponse de l'IA reçue")

    except asyncio.TimeoutError as te:
        handler_logger.error(
            f"Timeout lors de l'appel au LLM : {te}", exc_info=True
        )
        await message.reply(
            "Une erreur s'est produite lors de l'appel à l'IA."
        )
        return

    except ConnectionError as ce:
        handler_logger.error(
            f"Impossible de joindre l'API LLM (ConnectionRefused) : {ce}",
            exc_info=True,
        )
        await message.reply(
            "Service IA indisponible, veuillez réessayer plus tard."
        )
        return

    except Exception as e:
        handler_logger.exception(
            f"Erreur inattendue dans crew.kickoff: {e}"
        )
        await message.reply("Une erreur inattendue s'est produite.")
        return

    await send_long_message(message, response.raw)
