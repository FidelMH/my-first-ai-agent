import discord
from config import DISCORD_TOKEN
from ai_agents import crew

# ----- FIN DE LA CONFIGURATION -----
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Connecté en tant que {self.user}')

    async def on_message(self, message):
        # print("Message reçu:", message.content)
        if message.author == self.user:
            return
        if message.content.startswith('!ai '):
            prompt = message.content[4:]
            inputs = {
                "question": prompt,
            }
            # print("Prompt envoyé à l'IA:", prompt)
            await message.channel.typing()
            response = crew.kickoff(inputs=inputs)
            await message.reply(response)

if __name__ == "__main__":

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True   # <-- Essentiel !

    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)

    