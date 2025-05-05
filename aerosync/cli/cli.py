import click
import logging

from aerosync.cli.commands.google_drive import gdrive
from aerosync.cli.commands.list_entries import ls
from aerosync.cli.commands.sync import sync
from aerosync.db.db import init_db
from aerosync.utils.path_utils import create_app_dir


@click.group()
def cli():
    """AeroSync CLI — Sync your files to the cloud easily."""
    logging.info("cli initialized")
    create_app_dir()
    init_db()


@cli.command()
def test():
    click.echo("test command")


cli.add_command(gdrive)
cli.add_command(sync)
cli.add_command(ls)
