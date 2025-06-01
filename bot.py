import discord

import asyncio
import logging
# ----- CONFIGURATION DU LOGGING -----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger("discord_bot")
# ----- CONFIGURATION DU BOT DISCORD -----


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True   # <-- Essentiel !


class Bot(discord.Client):
    def __init__(self, crew_instance, intents=intents):
        super().__init__(intents=intents)
        self.crew = crew_instance  # Initialisation de crew à None
    async def on_ready(self):
        print(f'Connecté en tant que {self.user}')

    async def on_message(self, message) :
        logger.info(f"Message reçu de {message.author}: {message.content}")
        if message.author == self.user :
            return
        if message.content.startswith('!ai '):
            prompt = message.content[4:]

            if len(prompt) > 500:
                await message.reply("Votre question est trop longue (500 caractères max).")
                return
            inputs = {
                "message": prompt,
            }
            logger.debug(f"Prompt envoyé à l'IA: {prompt}")
            await message.channel.typing()
            # Appel asynchrone à crew.kickoff
            try:
                response = await self.crew.kickoff_async(inputs=inputs)
            
            except TimeoutError:
                logger.error("Timeout lors de l'appel au LLM")
                await message.reply("Une erreur s'est produite lors de l'appel à l'IA.")
                return
            
            except ConnectionError:
                logger.error("Impossible de joindre l'API LLM (ConnectionRefused)")
                await message.reply("Service IA indisponible, veuillez réessayer plus tard.")
                return
            
            except Exception as e:
                logger.exception(f"Erreur inattendue dans crew.kickoff: {e}")
                await message.reply("Une erreur inattendue s'est produite.")
                return
            
            await message.reply(response.raw)
    
