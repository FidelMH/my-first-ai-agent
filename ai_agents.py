"""Configuration et création des agents Crew.ai."""

from config import (
    OLLAMA_MISTRAL,
    OLLAMA_QWEN3,
    OLLAMA_DEEPSEEK_R1,
    LLM_API,
    SERPER_API_KEY
)
from crewai import Crew, Agent, Process, Task, LLM
from crewai_tools import ScrapeWebsiteTool,SerperDevTool




def create_llm(model: str, **config) -> LLM:
    """Return a configured LLM instance."""
    default_config = {
        "messages": [],
        "temperature": 0.7,
    }
    default_config.update(config)
    return LLM(model=model, base_url=LLM_API, config=default_config)


def create_agents() -> tuple[Agent, Agent, Agent]:
    """Create and return redact, search and scrape agents."""
    llm_mistral = create_llm(OLLAMA_MISTRAL)
    llm_qwen3 = create_llm(OLLAMA_QWEN3)
    llm_deepseek_r1 = LLM(model=OLLAMA_DEEPSEEK_R1, base_url=LLM_API)

    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

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
        role="Agent de Recherche sur {query}",
        goal="""Trouver des liens web pertinents sur un thème donné pour alimenter un agent scrapper""",
        backstory=(
            "Expert en recherche internet rapide et ciblée. Ne lit pas les pages, mais identifie les sources les plus pertinentes pour le sujet demandé.: {query}.   "
            "Tu utilises TOUJOURS l'outil Serper pour effectuer des recherches sur le web."
        ),
        llm=llm_qwen3,
        tools=[SerperDevTool(result_as_answer=True)],
        verbose=True,
    )

    scrape_agent = Agent(
        role="Scrapper web",
        goal="""Extraire proprement le contenu textuel des pages web fournies pour les transmettre à l'agent Rédacteur
        """,
        backstory=(
        "Spécialiste du scraping web. Son objectif est de récupérer rapidement le texte principal de chaque URL fournie, "
        "en nettoyant le contenu inutile comme les menus, pubs ou commentaires. Il ne fait aucune synthèse."
    ),
        llm=llm_qwen3,
        tools=[scrape_tool],
        verbose=True,
    )

    return redact_agent, search_agent, scrape_agent


def create_tasks(
    redact_agent: Agent, search_agent: Agent, scrape_agent: Agent
) -> tuple[Task, Task, Task]:
    """Create and return tasks for the crew."""

    search_task = Task(
        description=(
        "Fais une recherche web sur le thème suivant : '{query}'. "
        "Identifie les 5 à 10 liens les plus pertinents (articles, rapports, études, actualités), "
        "et retourne-les sous forme de liste avec le titre et l'URL. "
        "Ne lis pas les pages. N'analyse pas leur contenu. Ne fais pas de résumé."
    ),
        agent=search_agent,
        expected_output=(
        "Une liste des liens pertinents au format Markdown ou JSON :\n"
        "- [Titre de l'article 1](https://...)\n"
        "- [Titre de l'article 2](https://...)\n"
        "..." 
        ),
        output_file="results/links_output.txt"
    )

    scrape_task = Task(
        description=(
        "À partir de la liste suivante d'URLs : {query}, récupère le contenu principal de chaque page web. "
        "Ignore les menus, pubs, sidebars, commentaires ou balises inutiles. "
        "Rends un texte brut clair pour chaque page, structuré si possible par titre ou section."
    ),
        agent=scrape_agent,
        expected_output=(
        "Un dictionnaire ou JSON contenant pour chaque URL : son titre (si possible) et le texte brut extrait. "
        "Exemple :\n"
        "{\n  'https://...': {'title': 'Titre', 'content': 'Texte principal...'}, ...\n}"
    ),
        output_file="results/scraped_contents.json",
        context=[search_task]
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
        context=[scrape_task],
        output_file="results/final_article.txt",
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
