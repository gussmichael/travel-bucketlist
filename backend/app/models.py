import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel


class Destination(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)  # "city" or "landmark"
    country: str = Field(index=True)
    country_code: Optional[str] = None
    region: Optional[str] = None
    latitude: float
    longitude: float
    population: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class BucketListItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    destination_id: int = Field(foreign_key="destination.id", index=True, unique=True)
    visited: bool = False
    visited_date: Optional[dt.date] = None
    notes: Optional[str] = None
    created_at: dt.datetime = Field(default_factory=dt.datetime.utcnow)
