import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

import errors


def test_config_error_is_exception():
    assert issubclass(errors.ConfigError, Exception)


def test_llm_unavailable_error_is_exception():
    assert issubclass(errors.LLMUnavailableError, Exception)
