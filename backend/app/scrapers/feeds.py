from datetime import datetime

import feedparser
from icalendar import Calendar

from app.core.config import settings
from app.schemas import EventCreate
from app.scrapers.base import build_event, fetch_response, matches_keywords, parse_datetime


def parse_ics_content(content: bytes, fallback_url: str, source: str = "ics") -> list[EventCreate]:
    events: dict[str, EventCreate] = {}
    calendar = Calendar.from_ical(content)
    for component in calendar.walk("VEVENT"):
        title = str(component.get("summary", "")).strip()
        description = str(component.get("description", "")).strip()
        if not title or not matches_keywords(f"{title} {description}"):
            continue
        event_url = str(component.get("url", "")).strip() or fallback_url
        event = build_event(
            source=source,
            title=title,
            url=event_url,
            location=str(component.get("location", "")).strip(),
            starts_at=parse_datetime(component.decoded("dtstart", None)),
            description=description,
        )
        uid = str(component.get("uid", "")).strip()
        event.source_id = uid or event.source_id
        events[event.source_id] = event
    return list(events.values())


def parse_rss_content(content: bytes, fallback_url: str, source: str = "rss") -> list[EventCreate]:
    events: dict[str, EventCreate] = {}
    feed = feedparser.parse(content)
    for item in feed.entries:
        title = item.get("title", "").strip()
        description = item.get("summary", "").strip()
        if not title or not matches_keywords(f"{title} {description}"):
            continue
        starts_at = None
        if item.get("published_parsed"):
            starts_at = datetime(*item.published_parsed[:6])
        event = build_event(
            source=source,
            title=title,
            url=item.get("link", fallback_url),
            starts_at=starts_at,
            description=description,
        )
        event.source_id = item.get("id", event.source_id)
        events[event.source_id] = event
    return list(events.values())


async def scrape_ics_feeds() -> list[EventCreate]:
    events = []
    for url in settings.ics_urls:
        events.extend(parse_ics_content((await fetch_response(url)).content, url))
    return events


async def scrape_rss_feeds() -> list[EventCreate]:
    events = []
    for url in settings.rss_urls:
        events.extend(parse_rss_content((await fetch_response(url)).content, url))
    return events
