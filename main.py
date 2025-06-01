from crewai import Crew, Agent, Task, LLM
import discord
from dotenv import load_dotenv
import os



llm = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
)

mon_agent = Agent(
    role="Assistant IA",
    goal="Répondre aux questions factuelles avec des explications claires et concises.",
    backstory="Je suis un assistant qui connaît tout sur l'histoire, la science et la culture générale.",
    llm=llm,
)

question_task = Task(
    description="{question}",
    agent=mon_agent,
    expected_output="la réponse à la question"
)

crew = Crew(
    agents=[mon_agent],
    tasks=[question_task],
)

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
    # ----- UNE SEULE FOIS -----
    load_dotenv()  # Charge le .env dans l'environnement

    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True   # <-- Essentiel !

    client = MyClient(intents=intents)
    client.run(TOKEN)