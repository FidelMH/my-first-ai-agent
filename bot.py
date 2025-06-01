import discord
from ai_agents import crew
import asyncio

# ----- CONFIGURATION DU BOT DISCORD -----


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True   # <-- Essentiel !


class Bot(discord.Client):
    async def on_ready(self):
        print(f'Connecté en tant que {self.user}')

    async def on_message(self, message) :
        print("Message reçu:", message.content)
        if message.author == self.user :
            return
        if message.content.startswith('!ai '):
            prompt = message.content[4:]
            inputs = {
                "question": prompt,
            }
            print("Prompt envoyé à l'IA: ", prompt)
            await message.channel.typing()

            try:
                response = crew.kickoff_async(inputs=inputs)
            except Exception as e:
                print("Erreur lors de l'appel à l'IA:", e)
                await message.reply("Une erreur s'est produite lors de l'appel à l'IA.")
                return
            response = crew.kickoff(inputs=inputs)
            await message.reply(response)
    
