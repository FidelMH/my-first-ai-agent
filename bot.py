import discord

from handlers import on_message_handler, on_ready_handler
# ----- CONFIGURATION DU BOT DISCORD -----


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True   # <-- Essentiel !


class Bot(discord.Client):
    def __init__(self, crew_instance, intents=intents):
        super().__init__(intents=intents)
        self.crew = crew_instance  # Initialisation de crew à None
        
    async def on_ready(self):
        await on_ready_handler(self)

    async def on_message(self, message) :
        await on_message_handler(self, message)
    
