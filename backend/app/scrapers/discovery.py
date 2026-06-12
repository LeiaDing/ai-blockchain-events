import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.core.config import settings
from app.schemas import EventCreate
from app.scrapers.base import fetch_response
from app.scrapers.feeds import parse_ics_content, parse_rss_content
from app.scrapers.json_ld import parse_json_ld_soup

FEED_TYPES = {"application/rss+xml", "application/atom+xml"}
logger = logging.getLogger(__name__)


def normalize_url(page_url: str, value: str) -> str:
    url = urljoin(page_url, value)
    return f"https://{url.removeprefix('webcal://')}" if url.startswith("webcal://") else url


def response_format(url: str, content_type: str, content: bytes) -> str:
    normalized_type = content_type.lower().split(";", 1)[0]
    prefix = content.lstrip()[:100].upper()
    if normalized_type == "text/calendar" or url.lower().endswith(".ics") or prefix.startswith(b"BEGIN:VCALENDAR"):
        return "ics"
    if normalized_type in FEED_TYPES or b"<RSS" in prefix or b"<FEED" in prefix:
        return "rss"
    return "html"


def discover_linked_feeds(soup: BeautifulSoup, page_url: str) -> list[tuple[str, str]]:
    links: dict[str, str] = {}
    for link in soup.select("link[rel~='alternate'][href]"):
        content_type = link.get("type", "").lower()
        label = f"{link.get('href', '')} {link.get('title', '')}".lower()
        if content_type in FEED_TYPES and any(marker in label for marker in ("event", "calendar")):
            links[normalize_url(page_url, link["href"])] = "rss"
        elif content_type == "text/calendar":
            links[normalize_url(page_url, link["href"])] = "ics"
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        if href.startswith("webcal://") or href.lower().split("?", 1)[0].endswith(".ics"):
            links[normalize_url(page_url, href)] = "ics"
    return list(links.items())


async def scrape_discovered_sources() -> list[EventCreate]:
    events: dict[str, EventCreate] = {}
    for source_url in settings.sources:
        try:
            response = await fetch_response(source_url)
            kind = response_format(str(response.url), response.headers.get("content-type", ""), response.content)

            if kind == "ics":
                parsed = parse_ics_content(response.content, source_url, "discovered_ics")
            elif kind == "rss":
                parsed = parse_rss_content(response.content, source_url, "discovered_rss")
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                parsed = parse_json_ld_soup(soup, source_url, "discovered_json_ld")
                for linked_url, linked_kind in discover_linked_feeds(soup, source_url):
                    try:
                        linked_response = await fetch_response(linked_url)
                        if linked_kind == "ics":
                            parsed.extend(parse_ics_content(linked_response.content, linked_url, "discovered_ics"))
                        else:
                            parsed.extend(parse_rss_content(linked_response.content, linked_url, "discovered_rss"))
                    except Exception:
                        logger.exception("Linked feed failed: %s", linked_url)
        except Exception:
            logger.exception("Automatic source discovery failed: %s", source_url)
            continue

        for event in parsed:
            canonical_url = event.url.split("?", 1)[0].rstrip("/")
            existing = events.get(canonical_url)
            if not existing or (not existing.starts_at and event.starts_at):
                events[canonical_url] = event
    return list(events.values())
