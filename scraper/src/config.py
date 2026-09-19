from pathlib import Path


START_URL = (
    "https://books.toscrape.com/"
    "catalogue/page-1.html"
)

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE_DIR = BASE_DIR / "cache"
DETAIL_CACHE_DIR = CACHE_DIR / "details"

OUTPUT_DIR = BASE_DIR / "output"

BOOKS_FILE = OUTPUT_DIR / "books.json"
ERRORS_FILE = OUTPUT_DIR / "errors.json"
RUN_REPORT_FILE = OUTPUT_DIR / "run-report.json"

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/buffeddude69/Assignment---The-Polite-Scraper)"
)

REQUEST_TIMEOUT = 5

# Delay between real requests.
REQUEST_DELAY = 0.6

# Delay before retrying a timeout / 5xx.
RETRY_DELAY = 1.0

MAX_CATALOGUE_PAGES = 3