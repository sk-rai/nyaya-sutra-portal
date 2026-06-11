"""AFT Delhi (Principal Bench) scraper.

Thin subclass of AftGenericScraper registered as 'aft_delhi'.
The actual parsing logic is identical — all AFT benches use the same
text-based cause list format.
"""

from .aft_generic import AftGenericScraper
from .registry import register_scraper


@register_scraper
class AftDelhiScraper(AftGenericScraper):
    """AFT Principal Bench (Delhi) — registered as 'aft_delhi'.

    Inherits all logic from AftGenericScraper.
    URL: https://aftdelhi.nic.in/index.php/case-mgmt/daily-cause-list
    """

    SCRAPER_KEY = "aft_delhi"
