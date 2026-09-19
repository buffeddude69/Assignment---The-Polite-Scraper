import json

from pathlib import Path

from config import (
    BOOKS_FILE,
    ERRORS_FILE,
    OUTPUT_DIR,
    RUN_REPORT_FILE,
)


def write_json(
    path: Path,
    data,
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def write_books(
    records: list[dict],
) -> None:

    write_json(
        BOOKS_FILE,
        records,
    )


def write_errors(
    errors: list[dict],
) -> None:

    write_json(
        ERRORS_FILE,
        errors,
    )


def write_run_report(
    report: dict,
) -> None:

    write_json(
        RUN_REPORT_FILE,
        report,
    )