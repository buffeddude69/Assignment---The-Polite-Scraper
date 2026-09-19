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