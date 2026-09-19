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
    USER_AGENT,
)


def fetch_url(
    url: str,
    cache_file: Path,
    metadata_file: Path | None = None,
) -> tuple[str, str] | None:

    # -------------------------
    # CACHE
    # -------------------------
    if cache_exists(cache_file):
        html = read_cache(cache_file)

        if metadata_file and metadata_file.exists():
            fetched_at = read_cache(metadata_file).strip()
        else:
            fetched_at = ""

        print(
            f"CACHE HIT: {cache_file.name} "
            f"bytes={len(html.encode('utf-8'))}"
        )

        return html, fetched_at

    # -------------------------
    # REAL REQUEST
    # -------------------------
    sleep(REQUEST_DELAY)

    print(f"FETCH: {url}")

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=REQUEST_TIMEOUT,
        )

    except requests.RequestException as exc:
        print(f"FETCH FAILED: {exc}")
        return None

    # -------------------------
    # STATUS CHECK
    # -------------------------
    if response.status_code != 200:
        print(
            f"FETCH FAILED: HTTP {response.status_code}"
        )
        return None

    html = response.text

    fetched_at = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    # -------------------------
    # CACHE
    # -------------------------
    write_cache(cache_file, html)

    if metadata_file:
        write_cache(metadata_file, fetched_at)

    print(
        f"FETCHED: {cache_file.name} "
        f"bytes={len(response.content)}"
    )

    return html, fetched_at