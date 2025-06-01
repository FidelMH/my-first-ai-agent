from crewai import Crew, Agent, Task, LLM
import discord
from dotenv import load_dotenv
import os

# ----- UNE SEULE FOIS -----
load_dotenv()  # Charge le .env dans l'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
llm_api = os.getenv("LLM_API")
# ----- FIN DE LA CONFIGURATION -----
# Vérification des variables d'environnement
if not DISCORD_TOKEN:
    raise ValueError("Le token Discord n'est pas défini dans le fichier .env")
if not OLLAMA_MODEL:
    raise ValueError("Le modèle OLLAMA n'est pas défini dans le fichier .env")
if not llm_api:
    raise ValueError("L'URL de l'API LLM n'est pas définie dans le fichier .env")

# ----- CONFIGURATION DE CREW.AI -----
# Assurez-vous d'avoir installé la bibliothèque crewai avec `pip install crewai`
llm = LLM(
    model=OLLAMA_MODEL,
    base_url=llm_api
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

    