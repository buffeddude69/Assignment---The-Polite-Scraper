from datetime import datetime, timezone
from pathlib import Path
from time import sleep

import requests

from cache import (
    cache_exists,
    read_cache,
    write_cache,
)

from config import (
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
    USER_AGENT,
)

from models import FetchResult


def current_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def fetch_url(
    url: str,
    cache_file: Path,
    metadata_file: Path | None = None,
) -> FetchResult | None:

    # -------------------------
    # CACHE
    # -------------------------
    if cache_exists(cache_file):

        html = read_cache(cache_file)

        if metadata_file and metadata_file.exists():
            fetched_at = read_cache(
                metadata_file
            ).strip()
        else:
            fetched_at = ""

        print(
            f"CACHE HIT: {cache_file.name} "
            f"bytes={len(html.encode('utf-8'))}"
        )

        return FetchResult(
            html=html,
            fetched_at=fetched_at,
            cache_hit=True,
        )

    # -------------------------
    # REAL REQUEST
    # -------------------------

    sleep(REQUEST_DELAY)

    attempts = 0

    while attempts < 2:

        attempts += 1

        try:
            response = requests.get(
                url,
                headers={
                    "User-Agent": USER_AGENT
                },
                timeout=REQUEST_TIMEOUT,
            )

        except requests.Timeout:

            print(
                f"TIMEOUT attempt={attempts}: {url}"
            )

            if attempts == 1:
                print("Retrying after timeout...")
                sleep(RETRY_DELAY)
                continue

            print("FETCH FAILED after retry")
            return None

        except requests.RequestException as exc:

            # Other network errors are not retryable
            # under this assignment's rules.
            print(
                f"FETCH FAILED: {exc}"
            )

            return None

        # -------------------------
        # SUCCESS
        # -------------------------

        if response.status_code == 200:

            html = response.text

            fetched_at = current_timestamp()

            write_cache(
                cache_file,
                html,
            )

            if metadata_file:
                write_cache(
                    metadata_file,
                    fetched_at,
                )

            print(
                f"FETCHED: {cache_file.name} "
                f"bytes={len(response.content)}"
            )

            return FetchResult(
                html=html,
                fetched_at=fetched_at,
                cache_hit=False,
            )

        # -------------------------
        # SERVER ERROR
        # -------------------------

        if 500 <= response.status_code <= 599:

            print(
                f"SERVER ERROR "
                f"HTTP {response.status_code} "
                f"attempt={attempts}"
            )

            if attempts == 1:
                print(
                    "Retrying server error..."
                )
                sleep(RETRY_DELAY)
                continue

            print("FETCH FAILED after retry")
            return None

        # -------------------------
        # 403 / 404 / OTHER 4xx
        # -------------------------

        print(
            f"FETCH FAILED: "
            f"HTTP {response.status_code}"
        )

        # No retry.
        return None

    return None