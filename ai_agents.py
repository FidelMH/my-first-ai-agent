from config import  OLLAMA_MODEL, LLM_API
from crewai import Crew, Agent, Task, LLM

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
    name="Assistant IA Crew",
    verbose=True
)