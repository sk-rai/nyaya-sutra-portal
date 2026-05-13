"""AFT Delhi scraper implementation.

Thin subclass of AftGenericScraper that registers under the 'aft_delhi' key.
This ensures courts with scraper_key='aft_delhi' in the DB resolve correctly.
The actual logic is identical to the generic AFT scraper since all AFT benches
use the same PDF format — URLs come from the courts table.
"""

import logging

from .aft_generic import AftGenericScraper
from .registry import register_scraper

logger = logging.getLogger(__name__)


@register_scraper
class AftDelhiScraper(AftGenericScraper):
    """AFT Principal Bench (Delhi) — registered as 'aft_delhi'.

    Inherits all logic from AftGenericScraper. Exists only so that
    courts with scraper_key='aft_delhi' get an exact match in the registry.
    """

    SCRAPER_KEY = "aft_delhi"
