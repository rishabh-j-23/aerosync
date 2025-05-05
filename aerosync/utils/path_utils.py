import logging
import os

import config


def create_app_dir():
    app_dir = os.path.expanduser(config.APP_PATH)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
        logging.info(f"{app_dir} created")

    return app_dir
