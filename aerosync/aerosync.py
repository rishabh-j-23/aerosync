import logging
import sys
from aerosync.cli import cli
import config


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",  # Cyan
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def setup_logging():
    profile = config.PROFILE

    handler = logging.StreamHandler(sys.stdout)

    if profile and profile == "dev":
        formatter = ColorFormatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])
        logging.getLogger(__name__).info("Using 'dev' profile")
    elif profile and profile == "prod":
        logging.disable(level=100)
    else:
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logging.basicConfig(level=logging.WARNING, handlers=[handler])


def main():
    setup_logging()
    cli.cli()


if __name__ == "__main__":
    main()
