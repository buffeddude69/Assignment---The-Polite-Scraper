from pathlib import Path
import hashlib

from config import CACHE_DIR, DETAIL_CACHE_DIR


def get_catalogue_cache_file(page_number: int) -> Path:
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def get_detail_cache_file(product_url: str) -> Path:
    url_hash = hashlib.sha256(
        product_url.encode("utf-8")
    ).hexdigest()[:16]

    return DETAIL_CACHE_DIR / f"{url_hash}.html"


def get_detail_metadata_file(product_url: str) -> Path:
    url_hash = hashlib.sha256(
        product_url.encode("utf-8")
    ).hexdigest()[:16]

    return DETAIL_CACHE_DIR / f"{url_hash}.meta"


def read_cache(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_cache(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def cache_exists(path: Path) -> bool:
    return path.exists()