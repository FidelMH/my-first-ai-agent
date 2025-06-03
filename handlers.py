import asyncio
from logging_config import logger


async def on_ready_handler(bot):
        logger.info(f"Connecté en tant que {bot.user}")

async def on_message_handler(bot, message) :
        logger.info(f"Message reçu de {message.author}: {message.content}")
        if message.author == bot.user :
            return
        if message.content.startswith('!ai '):
            prompt = message.content[4:]

            if len(prompt) > 500:
                await message.reply("Votre question est trop longue (500 caractères max).")
                return
            inputs = {
                "question": prompt,
            }
            logger.debug(f"Prompt envoyé à l'IA: {prompt}")
            await message.channel.typing()
            # Appel asynchrone à crew.kickoff
            try:
                response = await bot.crew.kickoff_async(inputs=inputs)
            
            except asyncio.TimeoutError as te:
                logger.error(f"Timeout lors de l'appel au LLM : {te}")
                await message.reply("Une erreur s'est produite lors de l'appel à l'IA.")
                return
            
            except ConnectionError as ce:
                logger.error("Impossible de joindre l'API LLM (ConnectionRefused) : {ce}")
                await message.reply("Service IA indisponible, veuillez réessayer plus tard.")
                return
            
            except Exception as e:
                logger.exception(f"Erreur inattendue dans crew.kickoff: {e}")
                await message.reply("Une erreur inattendue s'est produite.")
                return
            
            
            await message.reply(response.raw)
    