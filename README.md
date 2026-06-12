# ai-blockchain-events

Full-stack event discovery app for AI and blockchain events.

- Backend: Python FastAPI with SQLite
- Frontend: React, Vite, and Tailwind CSS
- Collection: Ticketmaster API, public ICS/RSS feeds, and permitted JSON-LD event pages
- Scheduler: APScheduler daily scraper run at 2:00 AM

## Project Structure

```text
ai-blockchain-events/
  backend/
    app/
      api/
      core/
      db/
      models/
      scrapers/
      services/
      main.py
    requirements.txt
    .env.example
  frontend/
    src/
    index.html
    package.json
    tailwind.config.js
    postcss.config.js
    vite.config.js
  README.md
```

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

Useful endpoints:

- `GET /health`
- `GET /api/events`
- `GET /api/sources`
- `GET /api/source-diagnostics`
- `POST /api/scrape`

The SQLite database is created automatically at `backend/events.db`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

Set `VITE_API_BASE_URL` if your backend is not running on `http://localhost:8000`.

## Scraper Schedule

APScheduler starts with the FastAPI app and runs the scraper every day at 2:00 AM server time. You can also trigger a scrape manually with:

```bash
curl -X POST http://localhost:8000/api/scrape
```

## Collection Sources

Copy `.env.example` to `.env`, then configure the source URLs and API keys you want to use.

For the simplest setup, place organizer event pages, public calendars, and feed URLs together in `SOURCE_URLS`. The backend automatically detects ICS, RSS/Atom, linked feeds, and Schema.org Event JSON-LD.

The active collectors run independently, so one failed source does not stop the others. Eventbrite and Luma HTML adapters remain as inactive prototypes because their platform terms require a supported API or permission.

See `SOURCE_STRATEGIES.md` for supported collection methods and source policy.

Additional project references:

- `SOURCE_CATALOG.md`: reviewed organizer sources and latest results
- `SCRAPING_COMPLIANCE_NOTES.md`: scraping permissions and compliance notes
- `TROUBLESHOOTING.md`: problems encountered during development and their solutions
- `PROJECT_NOTES.md`: current progress and suggested next steps

## Tests

```bash
cd backend
.venv\Scripts\activate
pytest
```
