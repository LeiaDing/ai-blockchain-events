from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas import EventCreate, ScrapeResult
from app.scrapers import scrape_all_with_status


def list_events(db: Session, limit: int = 50, source: str | None = None) -> list[Event]:
    statement = select(Event).order_by(Event.starts_at.asc().nulls_last(), Event.created_at.desc()).limit(limit)
    if source:
        statement = statement.where(Event.source == source)
    return list(db.scalars(statement))


def upsert_events(db: Session, events: list[EventCreate], sources=None) -> ScrapeResult:
    created = 0
    updated = 0

    for event in events:
        payload = event.model_dump()
        existing = db.scalar(
            select(Event).where(Event.source == event.source, Event.source_id == event.source_id)
        )
        if existing:
            updated += 1
        else:
            created += 1

        statement = insert(Event).values(**payload)
        statement = statement.on_conflict_do_update(
            index_elements=["source", "source_id"],
            set_={
                "title": statement.excluded.title,
                "url": statement.excluded.url,
                "location": statement.excluded.location,
                "starts_at": statement.excluded.starts_at,
                "description": statement.excluded.description,
            },
        )
        db.execute(statement)

    db.commit()
    return ScrapeResult(scanned=len(events), created=created, updated=updated, sources=sources or [])


async def run_scrapers(db: Session) -> ScrapeResult:
    scraped_events, sources = await scrape_all_with_status()
    return upsert_events(db, scraped_events, sources)
