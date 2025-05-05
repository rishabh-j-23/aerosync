import click

from aerosync.db.models import watched_directories
from aerosync.db.models.watched_directories import WatchedDirectory
from aerosync.db.repositories import watched_directories_repository
from aerosync.utils.print_utils import print_sequences


@click.command()
@click.option(
    "-l", "--limit", type=click.INT, default=None, help="Limit number of results"
)
def ls(limit):
    """List watched directories."""
    watched_directories_list = watched_directories_repository.findAll(limit=limit)
    print_sequences(list(watched_directories_list), watched_directories.headers)
