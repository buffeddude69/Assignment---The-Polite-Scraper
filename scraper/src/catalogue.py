from urllib.parse import urljoin

from bs4 import BeautifulSoup

from cache import get_catalogue_cache_file
from config import (
    MAX_CATALOGUE_PAGES,
    START_URL,
)
from fetcher import fetch_url
from models import DiscoveredBook

from models import (
    DiscoveredBook,
    RunStats,
)


def parse_book_links(
    html: str,
    page_url: str,
) -> list[str]:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for book in soup.select(
        "article.product_pod h3 a"
    ):
        href = book.get("href")

        if href:
            absolute_url = urljoin(
                page_url,
                href
            )

            links.append(absolute_url)

    return links


def find_next_page(
    html: str,
    page_url: str,
) -> str | None:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    next_link = soup.select_one(
        "li.next a"
    )

    if not next_link:
        return None

    href = next_link.get("href")

    if not href:
        return None

    return urljoin(
        page_url,
        href
    )


def discover_books(
        stats: RunStats,
) -> list[DiscoveredBook]:

    current_url = START_URL

    catalogue_pages = 0

    discovered = []
    seen_urls = set()

    while catalogue_pages < MAX_CATALOGUE_PAGES:

        page_number = catalogue_pages + 1

        cache_file = get_catalogue_cache_file(
            page_number
        )

        result = fetch_url(
            current_url,
            cache_file,
        )

        if result is None:
            stats.failed_html += 1
            break

        if result.cache_hit:
            stats.cache_hits += 1
        else:
            stats.pages_html += 1

        html = result.html

        catalogue_pages += 1

        book_urls = parse_book_links(
            html,
            current_url
        )

        for product_url in book_urls:

            if product_url in seen_urls:
                continue

            seen_urls.add(product_url)

            discovered.append(
                DiscoveredBook(
                    product_url=product_url,
                    source_page=current_url,
                )
            )

        next_url = find_next_page(
            html,
            current_url
        )

        if not next_url:
            break

        current_url = next_url

    print(
        f"catalogue_pages={catalogue_pages}"
    )

    print(
        f"discovered={len(discovered)}"
    )

    print(
        f"unique_urls={len(seen_urls)}"
    )

    return discovered