import os
import sys
import importlib
import types
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)


def reload_utils(monkeypatch):
    if 'utils' in sys.modules:
        del sys.modules['utils']

    # Create dummy crewai BaseTool module
    crewai_mod = types.ModuleType("crewai")
    tools_mod = types.ModuleType("crewai.tools")

    class DummyBaseTool:
        pass

    tools_mod.BaseTool = DummyBaseTool
    crewai_mod.tools = tools_mod
    sys.modules['crewai'] = crewai_mod
    sys.modules['crewai.tools'] = tools_mod

    # Dummy SeleniumScrapingTool
    crewai_tools_mod = types.ModuleType("crewai_tools")

    class DummySeleniumScrapingTool:
        def _run(self, url: str) -> str:
            return "content"

    crewai_tools_mod.SeleniumScrapingTool = DummySeleniumScrapingTool
    sys.modules['crewai_tools'] = crewai_tools_mod

    # Dummy GoogleSearchAPIWrapper
    langchain_mod = types.ModuleType("langchain_google_community")

    class DummyGoogleSearchAPIWrapper:
        def __init__(self, **kwargs):
            pass

        def results(self, query: str, num_results: int = 5):
            return []

    langchain_mod.GoogleSearchAPIWrapper = DummyGoogleSearchAPIWrapper
    sys.modules['langchain_google_community'] = langchain_mod

    return importlib.import_module('utils')


class DummySearch:
    def results(self, query, num_results=5):
        return []


class DummySearchWithResults:
    def __init__(self, results):
        self._results = results

    def results(self, query, num_results=5):
        return self._results


def set_env(monkeypatch):
    monkeypatch.setenv('DISCORD_TOKEN', 'token')
    monkeypatch.setenv('OLLAMA_MISTRAL', 'model1')
    monkeypatch.setenv('OLLAMA_QWEN3', 'model2')
    monkeypatch.setenv('OLLAMA_DEEPSEEK_R1', 'model3')
    monkeypatch.setenv('LLM_API', 'http://url')
    monkeypatch.setenv('GOOGLE_CSE_ID', 'cseid')
    monkeypatch.setenv('GOOGLE_API_KEY', 'apikey')


def test_validate_url(monkeypatch):
    set_env(monkeypatch)
    utils = reload_utils(monkeypatch)
    monkeypatch.setattr(utils, 'GoogleSearchAPIWrapper', lambda **kw: DummySearch())
    tool = utils.SearchTool()
    assert tool.validate_url('http://example.com')
    assert tool.validate_url('https://example.com')
    assert not tool.validate_url('ftp://example.com')
    assert not tool.validate_url('http://')


def test_search_tool_run_no_results(monkeypatch):
    set_env(monkeypatch)
    utils = reload_utils(monkeypatch)
    monkeypatch.setattr(utils, 'GoogleSearchAPIWrapper', lambda **kw: DummySearch())
    tool = utils.SearchTool()
    result = tool._run('query')
    assert 'Aucun résultat trouvé' in result


def test_search_tool_run_with_results(monkeypatch):
    set_env(monkeypatch)
    utils = reload_utils(monkeypatch)
    dummy_results = [
        {'title': 'Title', 'snippet': 'Snippet', 'link': 'http://example.com'}
    ]
    monkeypatch.setattr(utils, 'GoogleSearchAPIWrapper', lambda **kw: DummySearchWithResults(dummy_results))
    monkeypatch.setattr(utils, 'validate_search_results', lambda results: results)
    tool = utils.SearchTool()
    response = tool._run('query')
    assert '- Source : Title' in response
    assert 'http://example.com' in response

