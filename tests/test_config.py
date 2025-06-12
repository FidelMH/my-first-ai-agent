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
    monkeypatch.setenv('OLLAMA_MODEL', 'model')
    monkeypatch.setenv('LLM_API', 'http://url')
    cfg = reload_config(monkeypatch)
    assert cfg.DISCORD_TOKEN == 'token'
    assert cfg.OLLAMA_MODEL == 'model'
    assert cfg.LLM_API == 'http://url'


def test_config_missing_token(monkeypatch):
    monkeypatch.delenv('DISCORD_TOKEN', raising=False)
    monkeypatch.setenv('OLLAMA_MODEL', 'model')
    monkeypatch.setenv('LLM_API', 'http://url')
    with pytest.raises(Exception):
        reload_config(monkeypatch)