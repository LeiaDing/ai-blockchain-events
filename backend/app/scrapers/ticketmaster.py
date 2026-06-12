from app.core.config import settings
from app.schemas import EventCreate
from app.scrapers.base import build_event, fetch_response, matches_keywords, parse_datetime

DISCOVERY_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


async def scrape_ticketmaster() -> list[EventCreate]:
    if not settings.ticketmaster_api_key:
        return []

    events: dict[str, EventCreate] = {}
    for keyword in settings.keywords:
        response = await fetch_response(
            DISCOVERY_URL,
            params={
                "apikey": settings.ticketmaster_api_key,
                "city": settings.ticketmaster_city,
                "countryCode": settings.ticketmaster_country_code,
                "keyword": keyword,
                "size": 100,
                "sort": "date,asc",
            },
        )
        for item in response.json().get("_embedded", {}).get("events", []):
            title = item.get("name", "")
            if not title or not matches_keywords(title):
                continue
            venue = item.get("_embedded", {}).get("venues", [{}])[0]
            location = ", ".join(
                value
                for value in [
                    venue.get("name"),
                    venue.get("city", {}).get("name"),
                    venue.get("state", {}).get("stateCode"),
                ]
                if value
            )
            event = build_event(
                source="ticketmaster",
                title=title,
                url=item.get("url", ""),
                location=location,
                starts_at=parse_datetime(item.get("dates", {}).get("start", {}).get("dateTime")),
                description=item.get("info"),
            )
            event.source_id = item.get("id", event.source_id)
            events[event.source_id] = event
    return list(events.values())
