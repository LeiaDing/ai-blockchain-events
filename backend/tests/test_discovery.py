import asyncio

import httpx

from app.core.config import settings
from app.scrapers.discovery import scrape_discovered_sources

PAGE_URL = "https://example.com/events"
ICS_URL = "https://example.com/events.ics"

HTML = """
<html>
  <head>
    <link rel="alternate" type="text/calendar" href="/events.ics">
    <link rel="alternate" type="application/rss+xml" href="/feed/" title="Site feed">
    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": "Toronto AI Builders",
        "startDate": "2026-07-01T18:00:00-04:00",
        "url": "/ai-builders"
      }
    </script>
  </head>
</html>
"""

ICS = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:blockchain-night-1
SUMMARY:Toronto Blockchain Night
DTSTART:20260702T220000Z
URL:https://example.com/blockchain-night
END:VEVENT
END:VCALENDAR
"""


def make_response(url: str, content: str, content_type: str) -> httpx.Response:
    request = httpx.Request("GET", url)
    return httpx.Response(
        200,
        content=content.encode(),
        headers={"content-type": content_type},
        request=request,
    )


def test_auto_discovery_finds_json_ld_and_linked_ics(monkeypatch):
    async def fake_fetch(url, params=None):
        if url == PAGE_URL:
            return make_response(url, HTML, "text/html")
        if url == ICS_URL:
            return make_response(url, ICS, "text/calendar")
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(settings, "source_urls", PAGE_URL)
    monkeypatch.setattr("app.scrapers.discovery.fetch_response", fake_fetch)

    events = asyncio.run(scrape_discovered_sources())

    assert {event.title for event in events} == {
        "Toronto AI Builders",
        "Toronto Blockchain Night",
    }


def test_auto_discovery_deduplicates_same_event_url(monkeypatch):
    duplicate_ics = ICS.replace(
        "https://example.com/blockchain-night",
        "https://example.com/ai-builders",
    ).replace("Toronto Blockchain Night", "Toronto AI Builders")

    async def fake_fetch(url, params=None):
        if url == PAGE_URL:
            return make_response(url, HTML, "text/html")
        if url == ICS_URL:
            return make_response(url, duplicate_ics, "text/calendar")
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(settings, "source_urls", PAGE_URL)
    monkeypatch.setattr("app.scrapers.discovery.fetch_response", fake_fetch)

    events = asyncio.run(scrape_discovered_sources())

    assert [event.title for event in events] == ["Toronto AI Builders"]
