import pytest
from unittest.mock import patch

import utils

# We mock DDGS to avoid external HTTP requests
class FakeDDGS:
    def __init__(self, results):
        self._results = results
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass
    def text(self, query, max_results=5):
        return self._results

def _mock_ddgs(results):
    return lambda: FakeDDGS(results)

def test_websearchtool_search(monkeypatch):
    fake_results = [
        {"title": "Python", "href": "https://python.org"},
        {"title": "PyTest", "href": "https://pytest.org"},
    ]
    monkeypatch.setattr(utils, "DDGS", _mock_ddgs(fake_results))
    tool = utils.WebSearchTool()
    output = tool.search("python")
    expected = "\n".join([f"{r['title']} : {r['href']}" for r in fake_results])
    assert output == expected

def test_mycustomtool_run(monkeypatch):
    fake_results = [
        {"title": "Python", "href": "https://python.org"},
    ]
    monkeypatch.setattr(utils, "DDGS", _mock_ddgs(fake_results))
    tool = utils.MyCustomTool()
    output = tool._run("python")
    expected = "\n".join([f"{r['title']} : {r['href']}" for r in fake_results])
    assert output == expected
