from urllib.parse import urlparse

from bs4 import BeautifulSoup

from cache import (
    get_detail_cache_file,
    get_detail_metadata_file,
)
from fetcher import fetch_url
from models import DiscoveredBook, RawBook


def get_book_slug(product_url: str) -> str:

    path_parts = (
        urlparse(product_url)
        .path
        .rstrip("/")
        .split("/")
    )

    return path_parts[-1].replace(
        ".html",
        ""
    )


def extract_description(
    product_area,
) -> str | None:

    heading = product_area.select_one(
        "#product_description"
    )

    if not heading:
        return None

    paragraph = heading.find_next_sibling(
        "p"
    )

    if not paragraph:
        return None

    text = paragraph.get_text(
        " ",
        strip=True
    )

    return text if text else None


def parse_book(
    html: str,
    book: DiscoveredBook,
    fetched_at: str,
) -> RawBook:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    product_area = soup.select_one(
        "div.product_main"
    )

    if not product_area:
        raise ValueError(
            f"Product area not found: "
            f"{book.product_url}"
        )

    title_element = product_area.select_one(
        "h1"
    )

    price_element = product_area.select_one(
        "p.price_color"
    )

    availability_element = (
        product_area.select_one(
            "p.instock.availability"
        )
    )

    rating_element = product_area.select_one(
        "p.star-rating"
    )

    title = (
        title_element.get_text(
            " ",
            strip=True
        )
        if title_element
        else None
    )

    price_text = (
        price_element.get_text(
            " ",
            strip=True
        )
        if price_element
        else None
    )

    availability_text = (
        availability_element.get_text(
            " ",
            strip=True
        )
        if availability_element
        else None
    )

    rating_text = None

    if rating_element:

        classes = rating_element.get(
            "class",
            []
        )

        for class_name in classes:

            if class_name != "star-rating":
                rating_text = class_name
                break

    description = extract_description(
        product_area
    )

    return RawBook(
        title=title,
        product_url=book.product_url,
        price_text=price_text,
        availability_text=availability_text,
        rating_text=rating_text,
        description=description,
        source_page=book.source_page,
        fetched_at=fetched_at,
    )


def fetch_book(
    book: DiscoveredBook,
) -> RawBook | None:

    slug = get_book_slug(
        book.product_url
    )

    cache_file = get_detail_cache_file(
        slug
    )

    metadata_file = get_detail_metadata_file(
        slug
    )

    result = fetch_url(
        book.product_url,
        cache_file,
        metadata_file,
    )

    if result is None:
        return None

    html, fetched_at = result

    try:
        return parse_book(
            html,
            book,
            fetched_at,
        )

    except ValueError as exc:
        print(
            f"PARSE FAILED: {exc}"
        )

        return None