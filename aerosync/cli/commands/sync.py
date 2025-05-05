import click

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
    print_utils.print_table(list(entry))
