from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, col, select

from app.database import get_session
from app.models import BucketListItem, Destination
from app.schemas import DestinationRead

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("/countries", response_model=list[str])
def list_countries(
    category: Optional[str] = None,
    session: Session = Depends(get_session),
):
    stmt = select(Destination.country).distinct().order_by(Destination.country)
    if category:
        stmt = stmt.where(Destination.category == category)
    return session.exec(stmt).all()


@router.get("", response_model=list[DestinationRead])
def list_destinations(
    q: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = select(Destination)

    if q:
        stmt = stmt.where(col(Destination.name).ilike(f"%{q}%"))
    if category:
        stmt = stmt.where(Destination.category == category)
    if country:
        stmt = stmt.where(Destination.country == country)

    stmt = stmt.order_by(
        col(Destination.population).desc().nulls_last(),
        Destination.name,
    )
    stmt = stmt.offset(offset).limit(limit)

    destinations = session.exec(stmt).all()

    # Check which destinations are in the bucket list
    dest_ids = [d.id for d in destinations]
    bucket_items = {}
    if dest_ids:
        bucket_stmt = select(BucketListItem).where(
            col(BucketListItem.destination_id).in_(dest_ids)
        )
        for item in session.exec(bucket_stmt).all():
            bucket_items[item.destination_id] = item.id

    result = []
    for d in destinations:
        read = DestinationRead(
            id=d.id,
            name=d.name,
            category=d.category,
            country=d.country,
            country_code=d.country_code,
            region=d.region,
            latitude=d.latitude,
            longitude=d.longitude,
            population=d.population,
            description=d.description,
            image_url=d.image_url,
            in_bucketlist=d.id in bucket_items,
            bucket_item_id=bucket_items.get(d.id),
        )
        result.append(read)

    return result


@router.get("/{destination_id}", response_model=DestinationRead)
def get_destination(
    destination_id: int,
    session: Session = Depends(get_session),
):
    dest = session.get(Destination, destination_id)
    if not dest:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Destination not found")

    bucket = session.exec(
        select(BucketListItem).where(
            BucketListItem.destination_id == destination_id
        )
    ).first()

    return DestinationRead(
        id=dest.id,
        name=dest.name,
        category=dest.category,
        country=dest.country,
        country_code=dest.country_code,
        region=dest.region,
        latitude=dest.latitude,
        longitude=dest.longitude,
        population=dest.population,
        description=dest.description,
        image_url=dest.image_url,
        in_bucketlist=bucket is not None,
        bucket_item_id=bucket.id if bucket else None,
    )
