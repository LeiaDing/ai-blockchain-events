from urllib.parse import quote_plus, urljoin

from app.scrapers.base import build_event, fetch_html, matches_keywords, parse_datetime
from app.schemas import EventCreate

LUMA_SEARCH_URL = "https://lu.ma/search?q={query}"


async def scrape_luma() -> list[EventCreate]:
    events: dict[str, EventCreate] = {}

    for keyword in ["ai blockchain", "artificial intelligence blockchain", "web3 ai"]:
        soup = await fetch_html(LUMA_SEARCH_URL.format(query=quote_plus(keyword)))
        for card in soup.select("a[href^='/'], a[href^='https://lu.ma/']"):
            title = card.get_text(" ", strip=True)
            href = card.get("href")
            if not title or not href or not matches_keywords(title):
                continue

            url = urljoin("https://lu.ma", href)
            if "/search" in url:
                continue

            starts_at = parse_datetime(card.find("time").get("datetime") if card.find("time") else None)
            event = build_event(
                source="luma",
                title=title,
                url=url,
                starts_at=starts_at,
            )
            events[event.source_id] = event

    return list(events.values())
