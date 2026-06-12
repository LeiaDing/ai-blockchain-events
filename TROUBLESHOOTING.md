# Problems and Solutions

This file summarizes the main issues encountered while building `ai-blockchain-events` and how they were resolved.

## Environment and Setup

1. **System `python` command was unavailable**
   - Problem: Windows redirected `python` to the Microsoft Store.
   - Solution: Used the Codex bundled Python runtime to create `backend/.venv`, then ran the project through the virtual environment.

2. **Backend and frontend dependencies were missing**
   - Problem: FastAPI imports failed and the frontend could not build.
   - Solution: Installed Python packages from `backend/requirements.txt` and ran `npm install` in `frontend`.

3. **Real `.env` values failed to parse**
   - Problem: `CORS_ORIGINS=http://localhost:5173` was treated as a JSON array by Pydantic Settings.
   - Solution: Marked the setting with `NoDecode` and added a comma-separated string validator.

## Scraping and Source Access

4. **Eventbrite HTML scraping conflicts with its terms**
   - Problem: Eventbrite terms prohibit automated HTML scraping.
   - Solution: Disabled Eventbrite HTML scraping by default and documented official API or permission as the supported path.

5. **Luma search URL stopped working**
   - Problem: The old `lu.ma/search` route redirected to a `luma.com/search` page returning 404.
   - Solution: Disabled the Luma HTML prototype by default and limited active collection to supported or explicitly permitted sources.

6. **Ticketmaster developer account email flow failed**
   - Problem: Password reset instructions did not arrive, preventing API key access.
   - Solution: Left Ticketmaster unconfigured and continued with sources that do not require developer credentials.

7. **One failed source stopped the entire scrape**
   - Problem: Sequential scraping raised an exception when one provider failed.
   - Solution: Added concurrent source execution, per-source failure isolation, and status reporting.

8. **One failed URL could stop automatic source discovery**
   - Problem: A network or parsing failure inside the unified URL list could interrupt the group.
   - Solution: Isolated every configured URL and linked feed so failures are logged and other URLs continue.

## Source Discovery and Data Quality

9. **Manually classifying every URL was inefficient**
   - Problem: Each organizer URL would need to be checked and configured as ICS, RSS, or JSON-LD.
   - Solution: Added unified `SOURCE_URLS` automatic discovery for direct ICS, RSS/Atom, Event JSON-LD, and publicly declared feeds.

10. **Generic website RSS introduced articles instead of events**
    - Problem: The MaRS events page linked to a general site RSS feed, producing news and article records.
    - Solution: Automatically follow RSS links only when their URL or title indicates events or calendars.

11. **The same Vector event appeared through JSON-LD and ICS**
    - Problem: Multiple structured formats exposed duplicate copies of the same activity.
    - Solution: Deduplicated automatic discovery results by canonical event URL.

12. **HTML entities appeared in titles**
    - Problem: Titles contained values such as `&#8211;`.
    - Solution: Decode HTML entities when creating event records.

13. **Several organizer pages expose no supported structured events**
    - Problem: TechTO, TorontoAI, Schwartz Reisman Institute, MaRS, and University of Toronto pages did not currently expose usable structured event records.
    - Solution: Keep them in `SOURCE_URLS`, report them as safely skipped, and allow future automatic detection if their pages change.

14. **It was unclear why a source returned no events**
    - Problem: The original API only reported the total scrape count.
    - Solution: Added `GET /api/sources`, `GET /api/source-diagnostics`, per-source scrape results, and a frontend diagnostics panel.

## Testing, Git, and Local Development

15. **Generated Python cache files were tracked by Git**
    - Problem: Running tests modified committed `__pycache__` files.
    - Solution: Expanded `.gitignore` to ignore all backend `__pycache__` folders and removed tracked `.pyc` files.

16. **Sensitive and generated local files must not reach GitHub**
    - Problem: `.env`, SQLite data, virtual environments, `node_modules`, and frontend builds should remain local.
    - Solution: Added ignore rules and verified them with `git check-ignore`.

17. **Browser screenshot verification was unavailable**
    - Problem: The bundled browser automation environment was missing `playwright-core`.
    - Solution: Verified frontend and backend availability through HTTP requests, production builds, and API tests.

18. **Existing localhost ports could conflict with new servers**
    - Problem: Earlier local services could still be using ports 8000 and 5173.
    - Solution: Used alternate ports 8001 and 5174 for the latest local integration test.

## Current Verification

- Backend automated tests: `5 passed`
- Frontend production build: passed
- Real source diagnostics:
  - Vector Institute: active, structured events discovered
  - Other configured organizer pages: safely skipped when no supported structured data was found
- Local `.env`, SQLite database, virtual environment, `node_modules`, and frontend build output are ignored by Git
