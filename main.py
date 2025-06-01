from crewai import Crew, Agent, Task, LLM
import discord
from config import DISCORD_TOKEN, OLLAMA_MODEL, LLM_API



# ----- CONFIGURATION DE CREW.AI -----
# Assurez-vous d'avoir installé la bibliothèque crewai avec `pip install crewai`
llm = LLM(
    model=OLLAMA_MODEL,
    base_url=LLM_API,  # Assurez-vous que l'API Ollama est en cours d'exécution
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

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True   # <-- Essentiel !

    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)

    