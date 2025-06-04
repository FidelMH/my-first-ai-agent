from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Type

   

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "WebsearchTool"
    description: str = "Search the web using DuckDuckGo."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:

        try:
            self.search(f"{argument}",5)
        except Exception as e:
            return f"An error occurred while searching: {e}"
        return 
    
    def search(self, query, max_results=5):
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        
        return "\n".join([f"{r['title']} : {r['href']}" for r in results])

