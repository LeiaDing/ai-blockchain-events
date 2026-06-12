from urllib.parse import quote_plus

from app.scrapers.base import build_event, fetch_html, matches_keywords, parse_datetime
from app.schemas import EventCreate

EVENTBRITE_SEARCH_URL = "https://www.eventbrite.com/d/online/{query}/"


async def scrape_eventbrite() -> list[EventCreate]:
    events: dict[str, EventCreate] = {}

    for keyword in ["ai blockchain", "artificial intelligence blockchain", "web3 ai"]:
        soup = await fetch_html(EVENTBRITE_SEARCH_URL.format(query=quote_plus(keyword)))
        for card in soup.select("a[href*='/e/']"):
            title = card.get_text(" ", strip=True)
            url = card.get("href")
            if not title or not url or not matches_keywords(title):
                continue

            starts_at = parse_datetime(card.find("time").get("datetime") if card.find("time") else None)
            event = build_event(
                source="eventbrite",
                title=title,
                url=url,
                starts_at=starts_at,
            )
            events[event.source_id] = event

    return list(events.values())
