from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Type

class WebSearchTool:
    """Outil de recherche web gratuit avec DuckDuckGo"""
    def search(self, query, max_results=5):
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        return "\n".join([f"{r['title']} : {r['href']}" for r in results])

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "WebsearchTool"
    description: str = "Search the web using DuckDuckGo."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(argument, max_results=5)]
        return "\n".join([f"{r['title']} : {r['href']}" for r in results])
