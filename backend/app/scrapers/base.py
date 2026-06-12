from datetime import date, datetime, time
from html import unescape
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.schemas import EventCreate

USER_AGENT = "ai-blockchain-events/0.1 (+https://localhost)"


async def fetch_html(url: str) -> BeautifulSoup:
    response = await fetch_response(url)
    return BeautifulSoup(response.text, "html.parser")


async def fetch_response(url: str, params: dict | None = None) -> httpx.Response:
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=20,
    ) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
    return response


def matches_keywords(text: str) -> bool:
    normalized = text.lower()
    return any(keyword.lower() in normalized for keyword in settings.keywords)


def source_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".strip("/")


def parse_datetime(value: str | datetime | date | None) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def build_event(
    source: str,
    title: str,
    url: str,
    location: str | None = None,
    starts_at: datetime | None = None,
    description: str | None = None,
) -> EventCreate:
    return EventCreate(
        source=source,
        source_id=source_id_from_url(url),
        title=unescape(title.strip()),
        url=url,
        location=unescape(location.strip()) if location else None,
        starts_at=starts_at,
        description=unescape(description.strip()) if description else None,
    )
