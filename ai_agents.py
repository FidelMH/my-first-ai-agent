"""Configuration et création des agents Crew.ai."""

from config import (
    OLLAMA_MISTRAL,
    OLLAMA_QWEN3,
    OLLAMA_DEEPSEEK_R1,
    LLM_API,
)
from crewai import Crew, Agent, Process, Task, LLM
from crewai_tools import SeleniumScrapingTool

from tools import SearchTool, SafeSeleniumScrapingTool


def create_llm(model: str, **config) -> LLM:
    """Return a configured LLM instance."""
    default_config = {
        "messages": [],
        "temperature": 0.7,
        "context_length": 4096,
    }
    default_config.update(config)
    return LLM(model=model, base_url=LLM_API, config=default_config)


def create_agents() -> tuple[Agent, Agent, Agent]:
    """Create and return redact, search and scrape agents."""
    llm_mistral = create_llm(OLLAMA_MISTRAL)
    llm_qwen3 = create_llm(OLLAMA_QWEN3)
    llm_deepseek_r1 = LLM(model=OLLAMA_DEEPSEEK_R1, base_url=LLM_API)

    search_tool = SearchTool()
    scrape_tool = SafeSeleniumScrapingTool()

    redact_agent = Agent(
        role="Rédacteur de Synthèse",
        goal="""Tu es un expert en synthèse d'informations.
        Ta mission :
        1. Analyser les informations extraites
        2. Identifier les points clés et tendances
        3. Structurer l'information de manière logique
        4. Produire un résumé clair et concis
        5. Respecter la limite de 2000 caractères""",
        backstory=(
            "Je suis un expert en synthèse qui transforme des informations "
            "complexes en résumés clairs"
        ),
        llm=llm_qwen3,
        verbose=True,
    )

    search_agent = Agent(
        role="Agent de Recherche",
        goal="""Tu es un expert en recherche d'information.
        Ta mission exacte :
        1. Analyser la requête pour identifier les mots-clés
        2. Rechercher des sources fiables et pertinentes
        3. Évaluer la qualité et la crédibilité des sources
        4. Sélectionner les 3 meilleures URLs
        5. Fournir un contexte pour chaque source""",
        backstory=(
            "Je suis un expert en recherche qui sait identifier les sources "
            "les plus pertinentes"
        ),
        llm=llm_qwen3,
        tools=[search_tool],
        verbose=True,
    )

    scrape_agent = Agent(
        role="Agent d'Extraction Web",
        goal="""Tu es un agent spécialisé dans l'extraction de contenu web.
        Ta mission est d'analyser les URLs fournies et d'en extraire les
        informations pertinentes.
        Pour chaque page web :
        1. Extraire le contenu principal
        2. Identifier les dates, titres et informations clés
        3. Ignorer les publicités et contenus non pertinents
        4. Structurer les informations extraites de manière claire
        5. Vérifier la pertinence du contenu par rapport à la requête
        """,
        backstory="""Je suis un expert en extraction de données web qui transforme
        les pages web en informations structurées et exploitables.""",
        llm=llm_deepseek_r1,
        tools=[scrape_tool],
        verbose=True,
    )

    return redact_agent, search_agent, scrape_agent


def create_tasks(
    redact_agent: Agent, search_agent: Agent, scrape_agent: Agent
) -> tuple[Task, Task, Task]:
    """Create and return tasks for the crew."""

    search_task = Task(
        description="""Recherche pour : "{query}"

        Exigences précises :
        1. Maximum 3 URLs pertinentes
        2. Sources de moins de 2 ans si possible
        3. Éviter les sites promotionnels
        4. Format de retour strict et obligatoire:
        {
            "task_status": "completed",
            "urls": ["url1", "url2", "url3"],
            "contexte": {
                "url1": "description et pertinence",
                "url2": "description et pertinence",
                "url3": "description et pertinence"
            }
        }""",
        agent=search_agent,
        expected_output="Dict avec urls et contexte",
    )

    scrape_task = Task(
        description="""Analyse et extrait le contenu de la recherche précédente.

        Instructions :
        1. Utilise l'outil de scraping pour chaque URL trouvée
        2. Extrait uniquement le contenu pertinent
        3. Structure les informations par source
        4. Fournis un résumé pour chaque page
        5. Indique la date de publication si disponible

        Format de retour obligatoire:
        {
            "task_status": "completed",
            "content": {
                "url1": {"summary": "...", "date": "..."},
                "url2": {"summary": "...", "date": "..."},
                "url3": {"summary": "...", "date": "..."}
            }
        }""",
        agent=scrape_agent,
        expected_output="Dict avec contenu structuré par source",
    )

    redact_task = Task(
        description="""Rédige un article structuré en Markdown à partir des
            informations extraites.

        Instructions :
        1. Analyse le contenu extrait et les sources fournies
        2. Rédige directement en Markdown avec cette structure :

        # [Titre accrocheur en rapport avec le sujet]

        ## Introduction
        [Introduction qui présente le contexte et les points clés]

        ## [Premier thème principal]
        [Développement du premier aspect important...]

        ## [Second thème principal]
        [Développement du second aspect important...]

        ## Conclusion
        [Synthèse des points clés et ouverture]

        ## Sources
        - [Titre de la source 1](url1)
        - [Titre de la source 2](url2)
        - [Titre de la source 3](url3)

        Exigences :
        1. Texte direct sans formatage JSON/code
        2. Structure hiérarchique avec #, ##
        3. Style journalistique clair
        4. Maximum 2000 caractères
        5. Sources citées en bas avec liens
        6. Le message doit être en Markdown, pas en JSON ou autre format, et pas
            de code block.
        7. ne pas inclure les informations non disponibles ou les erreurs de
            scraping dans l'article.
        8. ne pas inclure les penssées du modele, juste l'article final.""",
        agent=redact_agent,
        expected_output="Article en Markdown",
        output_file="article.md",
    )

    return search_task, scrape_task, redact_task


def create_crew() -> Crew:
    """Assemble agents and tasks into a Crew instance."""
    redact_agent, search_agent, scrape_agent = create_agents()
    search_task, scrape_task, redact_task = create_tasks(
        redact_agent, search_agent, scrape_agent
    )

    return Crew(
        agents=[search_agent, scrape_agent, redact_agent],
        tasks=[search_task, scrape_task, redact_task],
        name="Assistant IA Crew",
        verbose=True,
        process=Process.sequential,
    )


crew = create_crew()
