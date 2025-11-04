"""Background task scheduler using APScheduler."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone
import logging

from app.database import SessionLocal
from app.crud.notification import notification_crud

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


def cleanup_old_notifications():
    """Clean up old read notifications (>30 days)."""
    try:
        db = SessionLocal()
        count = notification_crud.delete_old_notifications(db, days=30)
        logger.info(f"Cleaned up {count} old notifications")
        db.close()
    except Exception as e:
        logger.error(f"Error cleaning notifications: {e}")


def start_scheduler():
    """Start background task scheduler."""
    # Run cleanup daily at 2 AM
    scheduler.add_job(
        cleanup_old_notifications,
        trigger=CronTrigger(hour=2, minute=0),
        id='cleanup_notifications',
        name='Cleanup old notifications',
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started")


def shutdown_scheduler():
    """Shutdown scheduler."""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
