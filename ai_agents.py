from config import  OLLAMA_MODEL, LLM_API
from crewai import Crew, Agent, Task, LLM
from tools import SearchTool

# ----- CONFIGURATION DE CREW.AI -----
# Assurez-vous d'avoir installé la bibliothèque crewai avec `pip install crewai`
llm = LLM(
    model=OLLAMA_MODEL,
    base_url=LLM_API,  # Assurez-vous que l'API Ollama est en cours d'exécution
)

search_tool = SearchTool()

mon_agent = Agent(
    role="Assistant IA",
    goal="""Tu es un assistant IA expert en histoire, science et culture générale. 
        Ton objectif est de répondre aux questions factuelles avec des explications claires, concises et exactes. Si un sujet prête à débat ou à interprétation, mentionne-le brièvement. Ne spécule jamais et indique si une information est incertaine ou non disponible.
        """,
    backstory="Je suis un assistant qui connaît tout sur l'histoire, la science et la culture générale.",
    llm=llm,
)

search_agent = Agent(
    role="Recherche Web",
    goal="Utiliser les outils de recherche pour trouver des informations sur Internet.",
    backstory="Je suis un agent qui utilise des outils de recherche pour trouver des informations.",
    llm=llm,
    tools=[search_tool],
)


question_task = Task(
    description="{question}",
    agent=mon_agent,
    expected_output="la réponse à la question"
)



crew = Crew(
    agents=[search_agent],
    tasks=[search_tool],
    name="Assistant IA Crew",
    verbose=True
)

