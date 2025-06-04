from googleapiclient.discovery import build
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Type

GOOGLE_API_KEY = "VOTRE_API_KEY"
GOOGLE_CSE_ID = "VOTRE_ID_CSE"

class GoogleToolInput(BaseModel):
    query: str = Field(..., description="Termes de recherche")

class GoogleSearchTool(BaseTool):
    name: str = "GoogleWebSearch"
    description: str = "Search the web with Google Custom Search"
    args_schema: Type[BaseModel] = GoogleToolInput

    def _run(self, query: str) -> str:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=5).execute()
        results = res.get("items", [])
        return "\n".join(f"{item['title']} : {item['snippet']}" for item in results)

