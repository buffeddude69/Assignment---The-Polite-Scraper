from pydantic import BaseModel, Field, field_validator


class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float = Field(ge=0)
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str
    fetched_at: str

    @field_validator("product_url", "source_page")
    @classmethod
    def validate_https_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError(
                "URL must start with https://"
            )

        return value