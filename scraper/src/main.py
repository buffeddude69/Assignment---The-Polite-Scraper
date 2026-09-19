from pathlib import Path
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


START_URL = "https://books.toscrape.com/catalogue/page-1.html"

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/buffeddude69/Assignment---The-Polite-Scraper)"
)

TIMEOUT = 5
REQUEST_DELAY = 0.6


def cache_file_for_page(page_number: int) -> Path:
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def fetch_page(url: str, page_number: int) -> str | None:
    cache_file = cache_file_for_page(page_number)

    # Use cache first
    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")
        print(f"CACHE HIT page={page_number} bytes={len(html.encode('utf-8'))}")
        return html

    sleep(REQUEST_DELAY)

    print(f"FETCH page={page_number}: {url}")

    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        print(f"FETCH FAILED page={page_number}: {exc}")
        return None

    # Failed response, never parse
    if response.status_code != 200:
        print(
            f"FETCH FAILED page={page_number}: "
            f"HTTP {response.status_code}"
        )
        return None

    html = response.text

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(html, encoding="utf-8")

    print(
        f"FETCHED page={page_number} "
        f"bytes={len(response.content)}"
    )

    return html


def parse_book_links(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for book in soup.select("article.product_pod h3 a"):
        href = book.get("href")

        if href:
            absolute_url = urljoin(page_url, href)
            links.append(absolute_url)

    return links


def find_next_page(html: str, page_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")

    next_link = soup.select_one("li.next a")

    if not next_link:
        return None

    href = next_link.get("href")

    if not href:
        return None

    return urljoin(page_url, href)


def discover_catalogue():
    current_url = START_URL
    all_book_urls = set()

    catalogue_pages = 0
    discovered_urls =[]

    while catalogue_pages < 3:
        page_number = catalogue_pages + 1

        html = fetch_page(current_url, page_number)

        if html is None:
            break

        catalogue_pages += 1

        book_urls = parse_book_links(
            html,
            current_url
        )

        discovered_urls.extend(book_urls)
        all_book_urls.update(book_urls)

        next_url = find_next_page(
            html,
            current_url
        )

        if not next_url:
            break

        current_url = next_url


    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={discovered_urls}")
    print(f"unique_urls={len(set(discovered_urls))}")


def main():
    discover_catalogue()


if __name__ == "__main__":
    main()