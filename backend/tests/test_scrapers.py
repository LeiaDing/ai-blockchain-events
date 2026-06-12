import asyncio

from app.schemas import EventCreate
from app.scrapers import SCRAPERS, scrape_all_with_status


def test_scrapers_isolate_source_failures(monkeypatch):
    async def successful_scraper():
        return [
            EventCreate(
                source="test",
                source_id="event-1",
                title="Toronto AI Event",
                url="https://example.com/event-1",
            )
        ]

    async def failed_scraper():
        raise RuntimeError("source unavailable")

    monkeypatch.setitem(SCRAPERS, "ticketmaster", successful_scraper)
    monkeypatch.setitem(SCRAPERS, "ics", failed_scraper)

    events, runs = asyncio.run(scrape_all_with_status())

    assert any(event.source_id == "event-1" for event in events)
    assert next(run for run in runs if run.name == "ticketmaster").events_found == 1
    assert next(run for run in runs if run.name == "ics").status == "failed"
