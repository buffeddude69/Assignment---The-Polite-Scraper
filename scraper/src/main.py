from pathlib import Path

import requests


URL = "https://books.toscrape.com/catalogue/page-1.html"

# scraper
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/buffeddude69/Assignment---The-Polite-Scraper)"
)

TIMEOUT = 5


def get_page():
    # Use cached HTML if it already exists
    if CACHE_FILE.exists():
        html = CACHE_FILE.read_text(encoding="utf-8")
        print(f"CACHE HIT: {len(html.encode('utf-8'))} bytes")
        return html

    print(f"FETCH: {URL}")

    try:
        response = requests.get(
            URL,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        print(f"FETCH FAILED: {exc}")
        return None

    # Check status before treating the response as HTML
    if response.status_code != 200:
        print(f"FETCH FAILED: HTTP {response.status_code}")
        return None

    html = response.text

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(html, encoding="utf-8")

    print(f"FETCH: {len(response.content)} bytes")
    print(f"Saved to: {CACHE_FILE}")

    return html


def main():
    get_page()


if __name__ == "__main__":
    main()