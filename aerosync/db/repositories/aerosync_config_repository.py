import datetime
import logging
from sqlmodel import select
from aerosync.db.db import get_session
from aerosync.db.models.aerosync_config import AerosyncConfig


def save_provider_config(config: AerosyncConfig):
    with get_session() as session:
        # Check if the cloud_provider already exists (only one allowed per provider)
        existing = session.exec(
            select(AerosyncConfig).where(
                AerosyncConfig.cloud_provider == config.cloud_provider
            )
        ).first()

        if existing:
            logging.info(
                f"Config for provider '{config.cloud_provider}' already exists with folder_id '{existing.folder_id}'. Skipping insert."
            )
            existing.folder_id = config.folder_id
            session.add(existing)
            return existing

        # Add new config
        config.updated_on = datetime.datetime.now()
        session.add(config)
        session.commit()
        session.refresh(config)
        logging.info(
            f"Saved new config for provider '{config.cloud_provider}' with folder_id '{config.folder_id}'."
        )
        return config


def findByProvider(provider: str) -> AerosyncConfig | None:
    with get_session() as session:
        result = session.exec(
            select(AerosyncConfig).where(provider == AerosyncConfig.cloud_provider)
        )
        return result.first()
