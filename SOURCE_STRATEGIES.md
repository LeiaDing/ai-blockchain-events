# Event Data Collection Strategies

## Supported Strategies

### Automatic Structured-Source Discovery

For a small, curated list of organizer URLs, use one configuration field:

```env
SOURCE_URLS=https://example.com/events,https://example.org/calendar
```

For each URL, the collector automatically:

1. Detects whether the URL itself is an ICS or RSS/Atom feed.
2. Parses Schema.org Event JSON-LD embedded in an HTML page.
3. Follows public ICS and RSS/Atom links declared by that page.
4. Skips the URL when no supported structured event format is found.

Automatic discovery does not fall back to generic visual HTML parsing.

### 1. Official JSON API

Best option when available. APIs return structured, stable data and usually define rate limits and permitted usage.

Current implementation:

- Ticketmaster Discovery API

Configuration:

```env
TICKETMASTER_API_KEY=your_key
TICKETMASTER_CITY=Toronto
TICKETMASTER_COUNTRY_CODE=CA
```

### 2. Public ICS / iCalendar Feeds

Many organizers and public Google Calendars expose an ICS URL. ICS is designed for calendar synchronization and contains structured event dates, locations, descriptions, and links.

Configuration:

```env
ICS_FEED_URLS=https://example.com/events.ics,https://example.org/calendar.ics
```

### 3. RSS / Atom Feeds

Some organizers publish event announcements through RSS or Atom. Feeds are stable and intended for automated subscription.

Configuration:

```env
RSS_FEED_URLS=https://example.com/events.xml,https://example.org/feed
```

### 4. Schema.org Event JSON-LD

Many event pages embed structured `Event` data inside:

```html
<script type="application/ld+json">
```

This is more stable than parsing visual HTML cards. Only add sites whose terms permit automated access or where permission has been obtained.

Configuration:

```env
JSON_LD_EVENT_URLS=https://open.toronto.ca/,https://example.com/events
```

### 5. Visual HTML Parsing

HTML parsing selects visual page elements such as event cards, headings, dates, and links. It is fragile because site layouts change frequently.

Use only when:

- The site's terms permit automated access or written permission exists.
- `robots.txt` allows the relevant paths.
- Requests are low frequency and rate limited.
- No login, CAPTCHA, access restriction, or anti-bot control is bypassed.

Configuration for explicitly permitted pages:

```env
HTML_EVENT_URLS=https://example.com/events,https://example.org/calendar
```

The previous Eventbrite and Luma HTML adapters remain in the source tree as prototypes but are not included in the active scraper registry.

### 6. Browser Automation

Tools such as Playwright can render JavaScript-heavy pages and interact with user interfaces. This is the most expensive and fragile method and should not be used to bypass access controls.

Use only for permitted sources that cannot expose data through API, feeds, JSON-LD, or static HTML.

### 7. Manual or Organizer Submission

For restricted platforms such as Partiful, Xiaohongshu, or other social networks, users and organizers can submit an event URL and necessary metadata manually. This provides broad coverage without automated platform scraping.

## Active Source Policy

The active scraper registry currently runs:

- Automatic structured-source discovery for URLs configured in `SOURCE_URLS`
- Ticketmaster API, when an API key is configured
- Public ICS feeds configured by URL
- Public RSS/Atom feeds configured by URL
- Permitted JSON-LD event pages configured by URL
- Permitted public HTML event pages explicitly configured by URL

Each source runs independently. A failure in one source is logged and does not stop the other sources.

## Adding a New Source

Before enabling a source, record:

- Source name and URL
- Collection method
- Terms or licence URL
- Permission status
- Required attribution
- Rate limit
- Allowed fields
- Date last reviewed
