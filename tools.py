from pydantic import Field
from crewai.tools import BaseTool
from langchain_google_community import GoogleSearchAPIWrapper
from config import GOOGLE_CSE_ID, GOOGLE_API_KEY
from typing import Optional
from logging_config import logger
from urllib.parse import urlparse
from typing import List, Dict, Optional

# Configure tool-specific logger
tool_logger = logger.getChild('tools')

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Recherche et synthétise des informations du web"
    search: Optional[GoogleSearchAPIWrapper] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search = GoogleSearchAPIWrapper(
            google_cse_id=GOOGLE_CSE_ID,
            google_api_key=GOOGLE_API_KEY,
        )
    
    def validate_url(self, url: str) -> bool:
        """Vérifie si l'URL est valide et sécurisée."""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https'] and len(parsed.netloc) > 3
        except:
            return False

    def _run(self, query: str) -> str:
        try:
            # Recherche sans restriction de domaine
            tool_logger.info(f"Recherche pour la requête : {query}")
            # Add num_results parameter here
            results = self.search.results(query, num_results=5)
            
            if not results:
                return "Aucun résultat trouvé pour cette recherche."
            
            valid_results = []
            for result in results:
                title = result.get("title", "").strip()
                snippet = result.get("snippet", "").strip()
                link = result.get("link", "").strip()
                
                if self.validate_url(link):
                    valid_results.append({
                        "title": title,
                        "description": snippet,
                        "url": link
                    })
            
            if not valid_results:
                return "Aucun résultat valide trouvé."
            
            # Format structuré des résultats
            response = "Résultats de recherche :\n\n"
            for result in valid_results[:3]:
                response += f"- Source : {result['title']}\n"
                response += f"  Résumé : {result['description']}\n"
                response += f"  Lien : {result['url']}\n\n"
            
            return response

        except Exception as e:
            tool_logger.error(f"Erreur lors de la recherche : {e}", exc_info=True)
            return f"Une erreur s'est produite lors de la recherche : {str(e)}"
