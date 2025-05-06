import logging
import os
import click

from aerosync.cloud_providers.google_drive import GoogleDriveProvider
from aerosync.db.models import watched_directories
from aerosync.db.repositories import watched_directories_repository
from aerosync.cloud_providers.providers import CloudProviders
from aerosync.utils import print_utils


@click.group()
def sync():
    """
    Manage which folders to sync
    """
    pass


@sync.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("provider", type=click.STRING)
def add(path, provider):
    """Add or update a directory in the sync list."""

    if not CloudProviders.exists(provider):
        click.echo("{provider} is not supported")
        return

    entry = watched_directories_repository.add_or_update_watched_directory(
        path, provider
    )
    logging.info(f"Added entry: {entry}")
    print_utils.print_sequences([entry], headers=watched_directories.headers)


# TODO: implement sync enable to enable sync daemon
@sync.command()
def enable():
    wds = watched_directories_repository.findAll()
    for wd in wds:
        provider = wd.cloud_provider
    pass


@sync.command()
def now():
    """Start syncing watched directories to their cloud providers."""
    wds = watched_directories_repository.findAll()

    if not wds:
        click.echo("No watched directories found in the database.")
        return

    for wd in wds:
        local_path = wd.path
        provider = wd.cloud_provider

        if not os.path.exists(local_path):
            click.echo(f"❌ Path does not exist: {local_path}")
            continue

        click.echo(f"🔄 Syncing {local_path} → {provider}")

        if provider == "gdrive":
            gdrive_provider = GoogleDriveProvider()
            gdrive_service = gdrive_provider.get_drive_service()

            wds = watched_directories_repository.findAll()
            for wd in wds:
                logging.info(
                    f"syncing for provider={provider}, enum val={CloudProviders.GDRIVE.value}"
                )
                if provider == CloudProviders.GDRIVE.value:
                    gdrive_provider.start_sync(wd, provider)

        else:
            click.echo(f"⚠️  Unsupported provider: {provider}")

    click.echo("✅ Sync complete.")
