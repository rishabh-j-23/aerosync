import logging
import config

from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(config.DATABASE_URL, echo=True)


def init_db():
    # Initialize the table
    from aerosync.db.models.watched_directories import WatchedDirectory  # noqa: F401
    from aerosync.db.models.aerosync_config import AerosyncConfig  # noqa: F401

    SQLModel.metadata.create_all(engine)
    logging.info(f"Database initialized at {config.DB_PATH}")


def get_session():
    return Session(engine)
