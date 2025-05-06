import click
import getpass

from aerosync.cloud_providers.google_drive import GoogleDriveProvider


@click.group()
def gdrive():
    """Google Drive related commands"""
    pass


@gdrive.command()
def login():
    google_provider = GoogleDriveProvider()
    print("Visit <this> page to learn how to generate Client ID and Client Secret")
    email = input("Email Address: ")
    client_id = getpass.getpass(prompt="Google Client ID: ")
    client_secret = getpass.getpass(prompt="Google Client Secret: ")
    google_provider.authenticate(
        client_id=client_id, client_secret=client_secret, email=email
    )
    if google_provider.creds is not None and google_provider.creds.valid:
        google_provider.create_folder()
        click.echo(f"Logged in successfully using '{email}'")


@gdrive.command()
def init():
    provider = GoogleDriveProvider()
    folder_id = provider.create_folder()
