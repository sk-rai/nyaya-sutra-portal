"""Scraper registry and factory for the Nyaya Sutra Backend.

Maps scraper_key values to scraper classes and provides a factory method
to instantiate the correct scraper for a given court.
"""

import logging
from typing import Dict, Optional, Type

from .base import BaseScraper

logger = logging.getLogger(__name__)

# Registry mapping scraper_key → scraper class
# Populated by register_scraper() or manually
_SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {}


def register_scraper(scraper_class: Type[BaseScraper]) -> Type[BaseScraper]:
    """Register a scraper class in the global registry.

    Can be used as a decorator:
        @register_scraper
        class AftDelhiScraper(BaseScraper):
            SCRAPER_KEY = "aft_delhi"
            ...

    Args:
        scraper_class: The scraper class to register.

    Returns:
        The same class (for decorator use).
    """
    key = scraper_class.SCRAPER_KEY
    _SCRAPER_REGISTRY[key] = scraper_class
    logger.debug(f"Registered scraper: {key} -> {scraper_class.__name__}")
    return scraper_class


class ScraperFactory:
    """Factory for creating scraper instances based on scraper_key.

    Usage:
        factory = ScraperFactory()
        scraper = factory.get_scraper("aft_delhi")
        result = scraper.scrape("aft_del", "OA-123/2024")
    """

    def __init__(self):
        """Initialize factory and ensure all scrapers are loaded."""
        self._ensure_scrapers_loaded()

    def _ensure_scrapers_loaded(self):
        """Import all scraper modules to trigger registration."""
        try:
            from . import aft_delhi  # noqa: F401
        except ImportError:
            pass
        try:
            from . import aft_generic  # noqa: F401
        except ImportError:
            pass
        try:
            from . import cat_delhi  # noqa: F401
        except ImportError:
            pass
        try:
            from . import cat_generic  # noqa: F401
        except ImportError:
            pass
        try:
            from . import fallback  # noqa: F401
        except ImportError:
            pass

    def get_scraper(self, scraper_key: str) -> Optional[BaseScraper]:
        """Get a scraper instance for the given scraper_key.

        Falls back to the generic/fallback parser if no specific scraper exists.

        Args:
            scraper_key: The scraper key from the courts table (e.g., "aft_delhi").

        Returns:
            A BaseScraper instance, or None if no scraper is available.
        """
        if not scraper_key:
            return self._get_fallback()

        # Exact match
        if scraper_key in _SCRAPER_REGISTRY:
            return _SCRAPER_REGISTRY[scraper_key]()

        # Try prefix match (e.g., "aft_mumbai" → "aft_generic")
        prefix = scraper_key.split("_")[0] if "_" in scraper_key else scraper_key
        generic_key = f"{prefix}_generic"
        if generic_key in _SCRAPER_REGISTRY:
            logger.info(
                f"No specific scraper for '{scraper_key}', "
                f"using generic: '{generic_key}'"
            )
            return _SCRAPER_REGISTRY[generic_key]()

        # Fallback
        return self._get_fallback()

    def _get_fallback(self) -> Optional[BaseScraper]:
        """Get the fallback generic parser."""
        if "fallback" in _SCRAPER_REGISTRY:
            return _SCRAPER_REGISTRY["fallback"]()
        logger.warning("No fallback scraper registered.")
        return None

    def list_scrapers(self) -> Dict[str, str]:
        """List all registered scrapers.

        Returns:
            Dict mapping scraper_key to class name.
        """
        return {key: cls.__name__ for key, cls in _SCRAPER_REGISTRY.items()}

    def has_scraper(self, scraper_key: str) -> bool:
        """Check if a specific scraper is registered.

        Args:
            scraper_key: The scraper key to check.

        Returns:
            True if a scraper (exact or generic fallback) is available.
        """
        if scraper_key in _SCRAPER_REGISTRY:
            return True
        prefix = scraper_key.split("_")[0] if "_" in scraper_key else scraper_key
        return f"{prefix}_generic" in _SCRAPER_REGISTRY or "fallback" in _SCRAPER_REGISTRY
