from urllib.parse import urljoin

from app.core.config import settings
from app.schemas import EventCreate
from app.scrapers.base import build_event, fetch_html, matches_keywords, parse_datetime


async def scrape_html_pages() -> list[EventCreate]:
    events: dict[str, EventCreate] = {}
    for page_url in settings.html_urls:
        soup = await fetch_html(page_url)
        for anchor in soup.select("a[href]"):
            title = anchor.get_text(" ", strip=True)
            href = anchor.get("href", "").strip()
            if not title or not href or not matches_keywords(title):
                continue

            container = anchor.find_parent(["article", "li", "section", "div"])
            time_element = container.find("time") if container else None
            starts_at = parse_datetime(time_element.get("datetime") if time_element else None)
            event = build_event(
                source="html",
                title=title,
                url=urljoin(page_url, href),
                starts_at=starts_at,
            )
            events[event.source_id] = event
    return list(events.values())
