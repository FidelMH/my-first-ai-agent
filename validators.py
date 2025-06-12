"""Validation utilities for search and scraping results."""
from __future__ import annotations

from typing import Any, Dict, List

from logging_config import logger

validator_logger = logger.getChild("validators")


def validate_search_results(results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Return only well formatted search results.

    Each result must contain non-empty ``title``, ``description`` and ``url``.
    Invalid entries are ignored.
    """
    valid_entries: List[Dict[str, str]] = []
    for entry in results:
        title = entry.get("title", "").strip()
        snippet = entry.get("snippet", "").strip()
        link = entry.get("link", "").strip()
        if title and snippet and link:
            valid_entries.append({"title": title, "description": snippet, "url": link})
        else:
            validator_logger.warning("Entr\u00e9e de recherche invalide ignor\u00e9e: %s", entry)
    return valid_entries


def validate_scrape_content(content: str) -> bool:
    """Check scraped content is not empty or too short."""
    if not isinstance(content, str) or len(content.strip()) < 20:
        validator_logger.warning("Contenu de scraping insuffisant ou invalide")
        return False
    return True
