import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, select

from app.database import get_session
from app.models import BucketListItem, Destination
from app.schemas import (
    BucketListCreate,
    BucketListRead,
    BucketListUpdate,
    MapMarkerRead,
)

router = APIRouter(prefix="/bucketlist", tags=["bucketlist"])


def _to_read(item: BucketListItem, dest: Destination) -> BucketListRead:
    return BucketListRead(
        id=item.id,
        destination_id=item.destination_id,
        visited=item.visited,
        visited_date=item.visited_date,
        notes=item.notes,
        created_at=item.created_at,
        destination_name=dest.name,
        destination_category=dest.category,
        destination_country=dest.country,
        destination_latitude=dest.latitude,
        destination_longitude=dest.longitude,
        destination_image_url=dest.image_url,
    )


@router.get("", response_model=list[BucketListRead])
def list_bucketlist(
    visited: Optional[bool] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session),
):
    stmt = (
        select(BucketListItem, Destination)
        .join(Destination, BucketListItem.destination_id == Destination.id)
    )

    if visited is not None:
        stmt = stmt.where(BucketListItem.visited == visited)
    if category:
        stmt = stmt.where(Destination.category == category)

    stmt = stmt.order_by(col(BucketListItem.created_at).desc())
    rows = session.exec(stmt).all()
    return [_to_read(item, dest) for item, dest in rows]


@router.post("", response_model=BucketListRead, status_code=201)
def add_to_bucketlist(
    data: BucketListCreate,
    session: Session = Depends(get_session),
):
    dest = session.get(Destination, data.destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")

    existing = session.exec(
        select(BucketListItem).where(
            BucketListItem.destination_id == data.destination_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Already in bucket list")

    item = BucketListItem(
        destination_id=data.destination_id,
        notes=data.notes,
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return _to_read(item, dest)


@router.patch("/{item_id}", response_model=BucketListRead)
def update_bucketlist_item(
    item_id: int,
    data: BucketListUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(BucketListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Bucket list item not found")

    if data.visited is not None:
        item.visited = data.visited
        if data.visited and not item.visited_date and data.visited_date is None:
            item.visited_date = dt.date.today()
        elif not data.visited:
            item.visited_date = None

    if data.visited_date is not None:
        item.visited_date = data.visited_date

    if data.notes is not None:
        item.notes = data.notes

    session.add(item)
    session.commit()
    session.refresh(item)

    dest = session.get(Destination, item.destination_id)
    return _to_read(item, dest)


@router.delete("/{item_id}", status_code=204)
def remove_from_bucketlist(
    item_id: int,
    session: Session = Depends(get_session),
):
    item = session.get(BucketListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Bucket list item not found")

    session.delete(item)
    session.commit()


@router.get("/map", response_model=list[MapMarkerRead])
def get_map_markers(
    visited_only: bool = False,
    session: Session = Depends(get_session),
):
    stmt = (
        select(BucketListItem, Destination)
        .join(Destination, BucketListItem.destination_id == Destination.id)
    )

    if visited_only:
        stmt = stmt.where(BucketListItem.visited == True)  # noqa: E712

    rows = session.exec(stmt).all()
    return [
        MapMarkerRead(
            bucket_item_id=item.id,
            destination_id=dest.id,
            name=dest.name,
            category=dest.category,
            country=dest.country,
            latitude=dest.latitude,
            longitude=dest.longitude,
            visited=item.visited,
        )
        for item, dest in rows
    ]
