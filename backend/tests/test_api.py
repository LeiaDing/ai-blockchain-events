from fastapi.testclient import TestClient

from app.main import app


def test_health_and_sources_endpoints():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

        response = client.get("/api/sources")
        assert response.status_code == 200
        assert {source["name"] for source in response.json()} == {
            "auto_discovery",
            "ticketmaster",
            "ics",
            "rss",
            "json_ld",
            "html",
        }
