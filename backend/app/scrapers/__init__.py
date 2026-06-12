import asyncio
import logging

from app.core.config import settings
from app.schemas import SourceInfo, SourceRun
from app.scrapers.discovery import scrape_discovered_sources
from app.scrapers.feeds import scrape_ics_feeds, scrape_rss_feeds
from app.scrapers.html import scrape_html_pages
from app.scrapers.json_ld import scrape_json_ld_pages
from app.scrapers.ticketmaster import scrape_ticketmaster

logger = logging.getLogger(__name__)

SCRAPERS = {
    "auto_discovery": scrape_discovered_sources,
    "ticketmaster": scrape_ticketmaster,
    "ics": scrape_ics_feeds,
    "rss": scrape_rss_feeds,
    "json_ld": scrape_json_ld_pages,
    "html": scrape_html_pages,
}

SOURCE_INFO = {
    "auto_discovery": SourceInfo(
        name="auto_discovery",
        method="structured_format_detection",
        configured=bool(settings.sources),
        description="Detects ICS, RSS/Atom, linked feeds, and Event JSON-LD from configured URLs.",
    ),
    "ticketmaster": SourceInfo(
        name="ticketmaster",
        method="official_api",
        configured=bool(settings.ticketmaster_api_key),
        description="Ticketmaster Discovery API for local keyword searches.",
    ),
    "ics": SourceInfo(
        name="ics",
        method="calendar_feed",
        configured=bool(settings.ics_urls),
        description="Public iCalendar feeds from organizers and calendars.",
    ),
    "rss": SourceInfo(
        name="rss",
        method="syndication_feed",
        configured=bool(settings.rss_urls),
        description="Public RSS or Atom announcement feeds.",
    ),
    "json_ld": SourceInfo(
        name="json_ld",
        method="structured_web_data",
        configured=bool(settings.json_ld_urls),
        description="Schema.org Event data embedded in permitted web pages.",
    ),
    "html": SourceInfo(
        name="html",
        method="public_html",
        configured=bool(settings.html_urls),
        description="Explicitly configured public pages that permit HTML collection.",
    ),
}


def list_sources() -> list[SourceInfo]:
    return list(SOURCE_INFO.values())


async def scrape_all():
    events, _ = await scrape_all_with_status()
    return events


async def scrape_all_with_status():
    names = list(SCRAPERS)
    results = await asyncio.gather(*(SCRAPERS[name]() for name in names), return_exceptions=True)
    events = []
    runs = []

    for name, result in zip(names, results, strict=True):
        source = SOURCE_INFO[name]
        if isinstance(result, Exception):
            logger.exception("Scraper failed: %s", name, exc_info=result)
            runs.append(
                SourceRun(
                    name=name,
                    method=source.method,
                    configured=source.configured,
                    status="failed",
                    error=str(result),
                )
            )
            continue
        logger.info("Scraper %s returned %d events", name, len(result))
        events.extend(result)
        runs.append(
            SourceRun(
                name=name,
                method=source.method,
                configured=source.configured,
                status="success" if source.configured else "not_configured",
                events_found=len(result),
            )
        )

    return events, runs
