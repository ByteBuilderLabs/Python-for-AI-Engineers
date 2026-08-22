from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    price: float = Field(strict=True)
    currency: str = Field(strict=True)
    in_stock: bool = Field(strict=True)
    updated_at: datetime

    @field_validator("updated_at")
    @classmethod
    def must_be_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("timestamp must be UTC")
        return v
