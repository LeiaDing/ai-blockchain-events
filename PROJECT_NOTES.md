# Project Notes

## Conversation Context

User prefers language matching:

- If the user asks in Chinese, answer in Chinese.
- If the user asks in English, answer in English.

## Project

Project name: `ai-blockchain-events`

Location:

```text
C:\Users\Admin\Documents\Codex\2026-06-05\create-a-full-stack-project-called-2\outputs\ai-blockchain-events
```

## What Has Been Created

- Backend: Python FastAPI
- Database: SQLite
- Frontend: React + Vite + Tailwind CSS
- Scraper modules:
  - Eventbrite
  - Luma
- Scheduler:
  - APScheduler
  - Runs scraper daily at 2:00 AM server time
- README with setup instructions
- `.env.example`
- `.gitignore`

## Important Backend Endpoints

- `GET /health`
- `GET /api/events`
- `POST /api/scrape`

## Verification Already Done

- Backend Python files passed syntax compilation using bundled Python.
- Frontend `package.json`, Vite config, and Tailwind config passed parse checks.

## Not Yet Done

- Backend and frontend dependencies have been installed.
- Backend server has not been started.
- Frontend server has not been started.
- Backend health and events API tests passed.
- Frontend production build passed.
- Real scraping was tested:
  - Eventbrite HTML scraping returned events, but its terms prohibit direct scraping.
  - Luma's old search URL returned 404.
- Scraping compliance findings are saved in `SCRAPING_COMPLIANCE_NOTES.md`.
- Active collection framework now supports:
  - Ticketmaster Discovery API
  - Public ICS feeds
  - RSS/Atom feeds
  - Permitted Schema.org Event JSON-LD pages
- Active sources run concurrently with failure isolation.
- Eventbrite and Luma HTML prototypes are no longer active by default.
- Collection strategy documentation is saved in `SOURCE_STRATEGIES.md`.
- Added `GET /api/sources` to report configured collection methods.
- `POST /api/scrape` now returns per-source success, failure, and event counts.
- Frontend now displays configured source status and the latest scrape result.
- Added backend tests for API health and source failure isolation.
- Added unified `SOURCE_URLS` automatic discovery:
  - Detects direct ICS and RSS/Atom feeds
  - Parses Event JSON-LD
  - Follows publicly declared ICS and RSS/Atom links
  - Skips unsupported pages without generic HTML fallback
- Ticketmaster was intentionally skipped because the developer account email/reset flow did not work.
- Added and audited initial Toronto/GTA organizer URLs in `SOURCE_CATALOG.md`.
- Automatic discovery now isolates failures per source URL and per linked feed.
- Real-source quality fixes completed:
  - Deduplicates the same activity found through JSON-LD and ICS by canonical URL.
  - Only follows page-linked RSS feeds whose URL/title indicates events or calendars.
  - Decodes HTML entities in event titles, locations, and descriptions.
- Real scrape on June 11, 2026 returned and stored 6 clean Vector Institute events.
- Backend tests: 5 passed.
- Added per-URL diagnostics through `GET /api/source-diagnostics`.
- Frontend can inspect configured URLs and display detected format, linked feeds, status, errors, and event count.
- Latest real diagnostic on June 12, 2026:
  - Vector Institute: success, 5 events, 2 linked calendar feeds
  - MaRS, TechTO, TorontoAI, Schwartz Reisman Institute, and University of Toronto: safely skipped because no supported structured events were found
- Development problems and solutions are summarized in `TROUBLESHOOTING.md`.
- Next major phase: deploy the application and scheduler to the cloud.

## Next Suggested Steps

1. Decide the five event sources.
2. Verify each source's terms and supported APIs.
3. Replace Eventbrite HTML scraping with an authorized API or disable it.
4. Replace Luma HTML scraping with an officially supported API, RSS, ICS, or authorized method.
5. Add rate limiting, source failure isolation, and compliance configuration.
6. Start and visually test the frontend and backend.
