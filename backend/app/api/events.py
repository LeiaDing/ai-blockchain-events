from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import EventRead, ScrapeResult, SourceDiagnostic, SourceInfo
from app.scrapers import list_sources
from app.scrapers.discovery import audit_discovered_sources
from app.services.events import list_events, run_scrapers

router = APIRouter()


@router.get("/sources", response_model=list[SourceInfo])
def get_sources():
    return list_sources()


@router.get("/source-diagnostics", response_model=list[SourceDiagnostic])
async def get_source_diagnostics():
    return await audit_discovered_sources()


@router.get("/events", response_model=list[EventRead])
def get_events(
    limit: int = Query(default=50, ge=1, le=200),
    source: str | None = None,
    db: Session = Depends(get_db),
):
    return list_events(db=db, limit=limit, source=source)


@router.post("/scrape", response_model=ScrapeResult)
async def scrape_events(db: Session = Depends(get_db)):
    return await run_scrapers(db=db)
