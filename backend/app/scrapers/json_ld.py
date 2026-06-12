import json
from urllib.parse import urljoin

from app.core.config import settings
from app.schemas import EventCreate
from app.scrapers.base import build_event, fetch_html, matches_keywords, parse_datetime


def iter_events(value):
    if isinstance(value, list):
        for item in value:
            yield from iter_events(item)
    elif isinstance(value, dict):
        if value.get("@type") == "Event" or "Event" in value.get("@type", []):
            yield value
        yield from iter_events(value.get("@graph", []))


def format_location(value) -> str | None:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        return None
    address = value.get("address", {})
    if isinstance(address, str):
        return ", ".join(part for part in [value.get("name"), address] if part)
    return ", ".join(
        part
        for part in [
            value.get("name"),
            address.get("streetAddress"),
            address.get("addressLocality"),
            address.get("addressRegion"),
        ]
        if part
    )


async def scrape_json_ld_pages() -> list[EventCreate]:
    events = []
    for page_url in settings.json_ld_urls:
        events.extend(parse_json_ld_soup(await fetch_html(page_url), page_url))
    return events


def parse_json_ld_soup(soup, page_url: str, source: str = "json_ld") -> list[EventCreate]:
    events: dict[str, EventCreate] = {}
    for script in soup.select("script[type='application/ld+json']"):
        try:
            payload = json.loads(script.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        for item in iter_events(payload):
            title = str(item.get("name", "")).strip()
            description = str(item.get("description", "")).strip()
            if not title or not matches_keywords(f"{title} {description}"):
                continue
            event_url = urljoin(page_url, item.get("url", page_url))
            event = build_event(
                source=source,
                title=title,
                url=event_url,
                location=format_location(item.get("location")),
                starts_at=parse_datetime(item.get("startDate")),
                description=description,
            )
            events[event.source_id] = event
    return list(events.values())
