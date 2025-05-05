import os
from dotenv import load_dotenv

load_dotenv()

PROFILE = os.getenv("PROFILE", "prod")

# Base app directory (expand ~ to full path)
APP_PATH = os.path.expanduser("~/.aerosync")

# Google Drive
GDRIVE_TOKEN_FILE = "aerosync_gdrive_token.pickle"
GDRIVE_TOKEN_PATH = os.path.join(APP_PATH, GDRIVE_TOKEN_FILE)

# SQLite DB
DB_NAME = "aerosync.db"
DB_PATH = os.path.join(APP_PATH, DB_NAME)
DATABASE_URL = f"sqlite:///{DB_PATH}"
