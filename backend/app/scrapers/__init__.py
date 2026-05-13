# Scraper modules — import to trigger registration via @register_scraper
from .base import BaseScraper, ScrapeResult  # noqa: F401
from .registry import ScraperFactory, register_scraper  # noqa: F401
