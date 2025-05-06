import logging
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from requests import Request

from aerosync.cloud_providers.base import BaseCloudProvider
from aerosync.cloud_providers.providers import CloudProviders
from aerosync.db.models.aerosync_config import AerosyncConfig
from aerosync.db.models.watched_directories import WatchedDirectory
from aerosync.db.repositories import aerosync_config_repository
from aerosync.utils import path_utils
import config

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveProvider(BaseCloudProvider):
    def __init__(self):
        self.creds = None
        self.service = None
        self.token_path = config.GDRIVE_TOKEN_PATH

    def authenticate(self, client_id: str, client_secret: str, email: str) -> None:
        self.creds = self.get_creds()

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                logging.info(f"Tokesn refreshed for {email}")
            else:
                logging.info(f"Starting InstalledAppFlow for {email}")
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost"],
                        }
                    },
                    SCOPES,
                )
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, "wb") as token:
                logging.debug(f"Dumped tokens into pickle file for email {email}")
                pickle.dump(self.creds, token)
        self.create_folder()

    def get_creds(self):
        token_path = os.path.expanduser(config.GDRIVE_TOKEN_PATH)
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.creds = pickle.load(token)
                return self.creds
        return None

    def get_drive_service(self):
        self.service = build("drive", "v3", credentials=self.get_creds())
        return self.service

    def upload_zip_to_gdrive(self, local_zip_path, folder_id):
        file_metadata = {
            "name": os.path.basename(local_zip_path),
            "parents": [folder_id],
            "mimeType": "application/zip",
        }
        media = MediaFileUpload(local_zip_path, mimetype="application/zip")
        file = (
            self.get_drive_service()
            .files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        logging.info(f"Uploaded ZIP to Google Drive: {file.get('id')}")
        return file.get("id")

    def start_sync(self, watched_dir: WatchedDirectory, provider: str):
        logging.info(f"Sync start for {watched_dir.path}")
        zip_path = f"{os.path.abspath(watched_dir.path).split(os.path.sep)[-1]}.zip"

        temp_backup_dir = config.TEMP_BACKUP_DIR
        os.makedirs(temp_backup_dir, exist_ok=True)
        zip_name = f"{os.path.basename(watched_dir.path)}.zip"
        zip_path = os.path.join(temp_backup_dir, zip_name)

        path_utils.zip_directory(watched_dir.path, zip_path)

        provider_config = aerosync_config_repository.findByProvider(provider)

        if not provider_config:
            self.create_folder()

        if provider_config and provider_config.folder_id:
            self.upload_zip_to_gdrive(zip_path, provider_config.folder_id)
            logging.info(f"Sync complete for {watched_dir.path}")

    def create_folder(self, name=None):
        file_metadata = {
            "name": name or config.APP_NAME,
            "mimeType": "application/vnd.google-apps.folder",
        }

        folder = (
            self.get_drive_service()
            .files()
            .create(body=file_metadata, fields="id")
            .execute()
        )

        folder_id = folder.get("id")
        logging.info(
            f"Folder '{file_metadata['name']}' created on {CloudProviders.GDRIVE}: id={folder_id}"
        )
        gdrive_config = AerosyncConfig(
            cloud_provider=CloudProviders.GDRIVE.value,
            folder_id=folder_id,
        )
        aerosync_config_repository.save_provider_config(gdrive_config)
        return folder_id
