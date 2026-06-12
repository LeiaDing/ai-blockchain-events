# Source Catalog

Last reviewed: June 11, 2026

| Source | URL | Result | Active |
|---|---|---|---|
| Vector Institute | https://vectorinstitute.ai/events/ | Event JSON-LD and public ICS discovered | Yes |
| MaRS Discovery District | https://www.marsdd.com/events/ | Public RSS and limited structured data discovered | Yes |
| TechTO | https://www.techto.org/events | No supported structured format found; safely skipped | Yes |
| TorontoAI | https://toronto-ai.org/events | No supported structured format found; safely skipped | Yes |
| Schwartz Reisman Institute | https://srinstitute.utoronto.ca/events | No supported structured format found; safely skipped | Yes |
| University of Toronto | https://www.utoronto.ca/events | No supported structured format found; safely skipped | Yes |
| DMZ | https://dmz.torontomu.ca/events/ | Candidate URL returned 404 | No |
| Microsoft Reactor | https://reactor.microsoft.com/en-us/reactor/events/ | Candidate URL returned 404 | No |
| York University | https://www.yorku.ca/events/ | TLS certificate validation failed during audit | No |

The active source list is stored in `backend/.env` under `SOURCE_URLS`. Unsupported pages remain in the list so they can begin working automatically if the organizer later adds JSON-LD, ICS, or RSS/Atom.

## Latest Real Run

On June 11, 2026, automatic discovery returned 6 clean Vector Institute events. Duplicate Vector events exposed through both JSON-LD and ICS were merged. MaRS's general article RSS feed was detected but intentionally ignored because it was not event-specific.
