from dataclasses import asdict

from pydantic import ValidationError

from books import fetch_book
from catalogue import discover_books
from normalizer import normalize_book
from output import write_books, write_errors
from schemas import BookRecord


def main():

    discovered_books = discover_books()

    records_by_url = {}
    errors = []

    for book in discovered_books:

        raw_book = fetch_book(book)

        if raw_book is None:
            errors.append({
                "product_url": book.product_url,
                "reason": "Failed to fetch or parse book page",
            })
            continue

        try:
            normalized = normalize_book(
                raw_book
            )

            validated = BookRecord.model_validate(
                normalized
            )

        except (ValueError, ValidationError) as exc:

            errors.append({
                "product_url": raw_book.product_url,
                "reason": str(exc),
                "record": asdict(raw_book),
            })

            continue

        # URL is the identity of the book.
        # Assigning by URL automatically removes duplicates.
        records_by_url[
            validated.product_url
        ] = validated.model_dump(
            mode="json"
        )

    # Sort for deterministic output.
    records = sorted(
        records_by_url.values(),
        key=lambda record: record["product_url"],
    )

    errors = sorted(
        errors,
        key=lambda error: error["product_url"],
    )

    write_books(records)
    write_errors(errors)

    print(f"valid_records={len(records)}")
    print(f"errors={len(errors)}")


if __name__ == "__main__":
    main()