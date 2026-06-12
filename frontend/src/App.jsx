import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function formatDate(value) {
  if (!value) return "Date TBD";
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

export default function App() {
  const [events, setEvents] = useState([]);
  const [sources, setSources] = useState([]);
  const [lastRun, setLastRun] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [error, setError] = useState("");

  async function loadEvents() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE_URL}/api/events`);
      if (!response.ok) throw new Error("Unable to load events");
      setEvents(await response.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadSources() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sources`);
      if (!response.ok) throw new Error("Unable to load sources");
      setSources(await response.json());
    } catch (err) {
      setError(err.message);
    }
  }

  async function runScrape() {
    setScraping(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE_URL}/api/scrape`, { method: "POST" });
      if (!response.ok) throw new Error("Unable to run scraper");
      setLastRun(await response.json());
      await loadEvents();
    } catch (err) {
      setError(err.message);
    } finally {
      setScraping(false);
    }
  }

  useEffect(() => {
    loadEvents();
    loadSources();
  }, []);

  return (
    <main className="min-h-screen bg-zinc-50 text-ink">
      <section className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-5 px-6 py-8 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-signal">Event intelligence</p>
            <h1 className="mt-2 text-3xl font-semibold">AI Blockchain Events</h1>
            <p className="mt-2 max-w-2xl text-zinc-600">
              Local AI and blockchain events collected from configured APIs, calendars, feeds, and public sources.
            </p>
          </div>
          <button
            className="h-11 rounded-md bg-signal px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-zinc-400"
            onClick={runScrape}
            disabled={scraping}
          >
            {scraping ? "Scraping..." : "Run scraper"}
          </button>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-8">
        {error ? (
          <div className="mb-6 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        ) : null}

        <div className="mb-8 border-b border-zinc-200 pb-8">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">Sources</h2>
              <p className="mt-1 text-sm text-zinc-600">{sources.filter((source) => source.configured).length} of {sources.length} configured</p>
            </div>
            {lastRun ? <p className="text-sm text-zinc-600">Last run found {lastRun.scanned} events</p> : null}
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            {sources.map((source) => {
              const run = lastRun?.sources?.find((item) => item.name === source.name);
              return (
                <div key={source.name} className="rounded-md border border-zinc-200 bg-white p-4">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-semibold uppercase">{source.name.replace("_", " ")}</span>
                    <span className={`h-2.5 w-2.5 rounded-full ${source.configured ? "bg-emerald-500" : "bg-zinc-300"}`} />
                  </div>
                  <p className="mt-2 text-xs text-zinc-500">{source.method.replaceAll("_", " ")}</p>
                  {run ? <p className="mt-2 text-xs font-medium text-zinc-700">{run.status}: {run.events_found} found</p> : null}
                </div>
              );
            })}
          </div>
        </div>

        {loading ? (
          <div className="text-zinc-600">Loading events...</div>
        ) : events.length === 0 ? (
          <div className="rounded-md border border-dashed border-zinc-300 bg-white px-6 py-10 text-center text-zinc-600">
            No events yet. Run the scraper to populate the feed.
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {events.map((event) => (
              <article key={event.id} className="rounded-md border border-zinc-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between gap-3">
                  <span className="rounded bg-zinc-100 px-2 py-1 text-xs font-semibold uppercase text-zinc-600">
                    {event.source}
                  </span>
                  <time className="text-sm text-zinc-500">{formatDate(event.starts_at)}</time>
                </div>
                <h2 className="mt-4 text-lg font-semibold leading-snug">{event.title}</h2>
                {event.location ? <p className="mt-2 text-sm text-zinc-600">{event.location}</p> : null}
                {event.description ? <p className="mt-3 line-clamp-3 text-sm text-zinc-600">{event.description}</p> : null}
                <a
                  className="mt-4 inline-flex text-sm font-semibold text-signal hover:text-teal-800"
                  href={event.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  View event
                </a>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
