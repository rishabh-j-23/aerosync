import logging
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import Request

from aerosync.cloud_providers.base import BaseCloudProvider
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

    def get_creds(self):
        token_path = os.path.expanduser(config.GDRIVE_TOKEN_PATH)
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.creds = pickle.load(token)
                return self.creds
        return None

    def get_drive_service(self):
        self.service = build("drive", "v3", credentials=self.creds)
        return self.service

    def sync_files(self, local_path, remote_path):
        # TODO: implement sync logic (upload, check existing, etc.)
        print(f"Syncing {local_path} → Google Drive:{remote_path}")
