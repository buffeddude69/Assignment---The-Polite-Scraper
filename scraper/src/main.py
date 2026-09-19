from datetime import datetime, timezone
from time import perf_counter

from dataclasses import asdict

from pydantic import ValidationError

from books import fetch_book
from catalogue import discover_books

from models import (
    DiscoveredBook,
    RunStats,
)

from normalizer import normalize_book
from output import (
    write_books,
    write_errors,
    write_run_report,
)

from schemas import BookRecord


FAKE_URL = (
    "https://books.toscrape.com/"
    "catalogue/this-book-does-not-exist_99999/"
    "index.html"
)


def current_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def main():

    started_at = datetime.now(timezone.utc)
    start_timer = perf_counter()

    stats = RunStats()

    errors = []
    records_by_url = {}

    try:

        discovered_books = discover_books(
            stats
        )

        for book in discovered_books:

            raw_book = fetch_book(book)

            if raw_book is None:

                stats.failed_pages += 1

                errors.append({
                    "product_url": book.product_url,
                    "reason": (
                        "Failed to fetch or parse "
                        "book page"
                    ),
                })

                continue

            try:

                normalized = normalize_book(
                    raw_book
                )

                validated = (
                    BookRecord.model_validate(
                        normalized
                    )
                )

            except (
                ValueError,
                ValidationError,
            ) as exc:

                stats.invalid_records += 1

                errors.append({
                    "product_url": (
                        raw_book.product_url
                    ),
                    "reason": str(exc),
                    "record": asdict(
                        raw_book
                    ),
                })

                continue

            records_by_url[
                validated.product_url
            ] = validated.model_dump(
                mode="json"
            )

        stats.valid_records = len(
            records_by_url
        )

        records = sorted(
            records_by_url.values(),
            key=lambda record:
                record["product_url"],
        )

        errors = sorted(
            errors,
            key=lambda error:
                error["product_url"],
        )

        write_books(records)
        write_errors(errors)

    finally:

        duration = (
            perf_counter() - start_timer
        )

        report = {
            "started_at": current_timestamp(),
            "duration_seconds": round(
                duration,
                3,
            ),
            "pages_fetched": (
                stats.pages_fetched
            ),
            "cache_hits": (
                stats.cache_hits
            ),
            "valid_records": (
                stats.valid_records
            ),
            "invalid_records": (
                stats.invalid_records
            ),
            "failed_pages": (
                stats.failed_pages
            ),
        }

        write_run_report(report)

        print("\nRUN REPORT")
        print(report)


if __name__ == "__main__":
    main()