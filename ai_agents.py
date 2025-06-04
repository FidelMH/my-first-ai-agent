from config import  OLLAMA_MODEL, LLM_API
from crewai import Crew, Agent, Task, LLM
from utils import GoogleSearchTool  # Assurez-vous que cet outil est défini dans utils.py

# ----- CONFIGURATION DE CREW.AI -----
# Assurez-vous d'avoir installé la bibliothèque crewai avec `pip install crewai`
llm = LLM(
    model=OLLAMA_MODEL,
    base_url=LLM_API,  # Assurez-vous que l'API Ollama est en cours d'exécution
)

web_search_tool = GoogleSearchTool()
mon_agent = Agent(
    role="Assistant IA",
    goal="Répondre aux questions factuelles avec des explications claires et concises.",
    backstory="Je suis un assistant qui connaît tout sur l'histoire, la science et la culture générale.",
    llm=llm,
)
agent_search = Agent(
    role="Agent de recherche",
    goal="Répondre à toute question grâce à la recherche internet.",
    backstory="Agent IA moderne, utilise DuckDuckGo pour répondre de façon fiable et gratuite.",
    tools=[web_search_tool],  # Assurez-vous que l'outil WebSearchTool est importé
    llm=llm
)


web_search = Task(
    description="Effectuer une recherche sur le web pour trouver des informations pertinentes avec ce mot clé {question}. donnes des liens et fais un résumé",
    agent=agent_search,
    expected_output="le résultat de la recherche",
    
)

# question_task = Task(
#     description="{question}",
#     agent=mon_agent,
#     expected_output="la réponse à la question"
# )

crew = Crew(
    agents=[agent_search],
    tasks=[web_search],
    name="Assistant IA Crew",
    verbose=True
)