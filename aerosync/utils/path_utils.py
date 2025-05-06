import logging
import zipfile
import os

import config


def create_app_dir():
    app_dir = os.path.expanduser(config.APP_PATH)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
        logging.info(f"{app_dir} created")

    return app_dir


def zip_directory(dir_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dir_path)
                zipf.write(file_path, arcname)
