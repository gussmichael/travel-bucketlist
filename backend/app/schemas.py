import datetime as dt
from typing import Optional

from pydantic import BaseModel


class DestinationRead(BaseModel):
    id: int
    name: str
    category: str
    country: str
    country_code: Optional[str] = None
    region: Optional[str] = None
    latitude: float
    longitude: float
    population: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    in_bucketlist: bool = False
    bucket_item_id: Optional[int] = None


class BucketListCreate(BaseModel):
    destination_id: int
    notes: Optional[str] = None


class BucketListUpdate(BaseModel):
    visited: Optional[bool] = None
    visited_date: Optional[dt.date] = None
    notes: Optional[str] = None


class BucketListRead(BaseModel):
    id: int
    destination_id: int
    visited: bool
    visited_date: Optional[dt.date] = None
    notes: Optional[str] = None
    created_at: dt.datetime
    destination_name: str
    destination_category: str
    destination_country: str
    destination_latitude: float
    destination_longitude: float
    destination_image_url: Optional[str] = None


class MapMarkerRead(BaseModel):
    bucket_item_id: int
    destination_id: int
    name: str
    category: str
    country: str
    latitude: float
    longitude: float
    visited: bool
