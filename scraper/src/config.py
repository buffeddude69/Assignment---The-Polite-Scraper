from pathlib import Path


START_URL = "https://books.toscrape.com/catalogue/page-1.html"

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE_DIR = BASE_DIR / "cache"
DETAIL_CACHE_DIR = CACHE_DIR / "details"

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/buffeddude69/Assignment---The-Polite-Scraper)"
)

REQUEST_TIMEOUT = 5
REQUEST_DELAY = 0.6

MAX_CATALOGUE_PAGES = 3