from pydantic import Field
from crewai.tools import BaseTool
from langchain_google_community import GoogleSearchAPIWrapper
from config import GOOGLE_CSE_ID, GOOGLE_API_KEY

search_api = GoogleSearchAPIWrapper(
    google_cse_id=GOOGLE_CSE_ID,
    google_api_key=GOOGLE_API_KEY
)

class SearchTool(BaseTool):
    """A tool for searching the web using Google Search API."""

    name: str = "Search"
    description: str = "Use this tool to search the web for information."
    search: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)
    def _run(self, query: str) -> str:
        """Run the search with the given query."""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"An error occurred while searching: {str(e)}"
