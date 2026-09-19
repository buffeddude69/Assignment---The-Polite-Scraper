from dataclasses import dataclass


@dataclass
class DiscoveredBook:
    product_url: str
    source_page: str


@dataclass
class RawBook:
    title: str | None
    product_url: str
    price_text: str | None
    availability_text: str | None
    rating_text: str | None
    description: str | None
    source_page: str
    fetched_at: str


@dataclass
class FetchResult:
    html: str
    fetched_at: str
    cache_hit: bool

@dataclass
class RunStats:
    pages_fetched: int = 0
    cache_hits: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    failed_pages: int = 0