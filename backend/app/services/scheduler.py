import asyncio
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import SessionLocal
from app.services.events import run_scrapers

logger = logging.getLogger(__name__)


def scheduled_scrape() -> None:
    db = SessionLocal()
    try:
        result = asyncio.run(run_scrapers(db))
        logger.info("Scheduled scrape complete: %s", result.model_dump())
    except Exception:
        logger.exception("Scheduled scrape failed")
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_scrape,
    CronTrigger(hour=2, minute=0),
    id="daily-event-scrape",
    replace_existing=True,
)
