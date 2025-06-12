import os
import sys
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from logging_config import setup_logging, logger


def test_setup_logging_configures_logger(tmp_path):
    setup_logging()
    root_logger = logging.getLogger()
    assert root_logger.handlers
