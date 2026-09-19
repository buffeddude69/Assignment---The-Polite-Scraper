import re

from models import RawBook


PRICE_PATTERN = re.compile(
    r"£\s*([0-9]+(?:\.[0-9]+)?)"
)


def parse_price(price_text: str) -> float:
    match = PRICE_PATTERN.search(price_text)

    if not match:
        raise ValueError(
            f"Could not parse price: {price_text!r}"
        )

    return float(match.group(1))


def normalize_book(book: RawBook) -> dict:
    if not book.price_text:
        raise ValueError(
            "Missing price_text"
        )

    price_gbp = parse_price(
        book.price_text
    )

    return {
        "title": book.title,
        "product_url": book.product_url,
        "price_text": book.price_text,
        "price_gbp": price_gbp,
        "availability_text": book.availability_text,
        "rating_text": book.rating_text,
        "description": book.description,
        "source_page": book.source_page,
        "fetched_at": book.fetched_at,
    }