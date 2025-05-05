import logging

from sqlmodel import select
from aerosync.db.db import get_session
from aerosync.db.models import watched_directories
from aerosync.db.models.watched_directories import WatchedDirectory


def add_or_update_watched_directory(path, provider):
    from datetime import datetime

    with get_session() as session:
        existing = session.exec(
            select(WatchedDirectory).where(WatchedDirectory.path == path)
        ).first()

        now = datetime.now()

        if existing:
            existing.watched = True
            existing.updated_on = now
            session.add(existing)
            session.commit()
            logging.info(f"Updated existing record; path={path}")
            return existing
        else:
            new_dir = WatchedDirectory(
                cloud_provider=provider,
                path=path,
                watched=True,
                created_on=now,
                updated_on=now,
            )
            session.add(new_dir)
            logging.info(f"Created new record; path={path}")
            session.commit()
            return new_dir


def findAll(limit=None):
    with get_session() as session:
        statement = select(WatchedDirectory)
        if limit:
            statement = statement.limit(limit)
        result = session.exec(statement)
        return result.all()  # converts to list of ORM objects
