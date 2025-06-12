import os
import sys
import importlib
import types
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)


def reload_config(monkeypatch):
    if 'config' in sys.modules:
        del sys.modules['config']
    return importlib.import_module('config')


def test_config_load_success(monkeypatch):
    monkeypatch.setenv('DISCORD_TOKEN', 'token')
    monkeypatch.setenv('OLLAMA_MISTRAL', 'model1')
    monkeypatch.setenv('OLLAMA_QWEN3', 'model2')
    monkeypatch.setenv('OLLAMA_DEEPSEEK_R1', 'model3')
    monkeypatch.setenv('LLM_API', 'http://url')
    monkeypatch.setenv('GOOGLE_CSE_ID', 'cseid')
    monkeypatch.setenv('GOOGLE_API_KEY', 'apikey')
    cfg = reload_config(monkeypatch)
    assert cfg.DISCORD_TOKEN == 'token'
    assert cfg.OLLAMA_MISTRAL == 'model1'
    assert cfg.OLLAMA_QWEN3 == 'model2'
    assert cfg.OLLAMA_DEEPSEEK_R1 == 'model3'
    assert cfg.LLM_API == 'http://url'
    assert cfg.GOOGLE_CSE_ID == 'cseid'
    assert cfg.GOOGLE_API_KEY == 'apikey'


def test_config_missing_token(monkeypatch):
    monkeypatch.delenv('DISCORD_TOKEN', raising=False)
    monkeypatch.setenv('OLLAMA_MISTRAL', 'model1')
    monkeypatch.setenv('OLLAMA_QWEN3', 'model2')
    monkeypatch.setenv('OLLAMA_DEEPSEEK_R1', 'model3')
    monkeypatch.setenv('LLM_API', 'http://url')
    monkeypatch.setenv('GOOGLE_CSE_ID', 'cseid')
    monkeypatch.setenv('GOOGLE_API_KEY', 'apikey')
    with pytest.raises(Exception):
        reload_config(monkeypatch)
