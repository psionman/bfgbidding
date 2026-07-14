# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import appdirs
import structlog

from bfgbidding.constants import APP_NAME

LOG_FILE_NAME = "bidding.log"
MAX_BYTES = 5_000_000
BACKUP_COUNT = 5


def app_logger(level=logging.INFO):
    """
    Creates and configures a logger for the application.

    Args:
        level (int): The logging level (default is logging.INFO).

    Returns:
        Logger: A configured logger for the application.

    Examples:
        logger = logger(logging.DEBUG)
    """

    log_file = _log_file(APP_NAME)
    console_handler = _console_handler(level)
    file_handler = _file_handler(log_file, level)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    structlog.configure(
        processors=_processors(),
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def _log_file(app_name: str) -> Path:
    """Return the path to the application log file.

    Priority:
    1. BFG_LOG_DIR env var, if set
    2. A `logs/` directory next to the installed package
    3. Falls back to appdirs.user_data_dir() as a last resort
    """
    override = os.environ.get("BFG_LOG_DIR")
    if override:
        log_dir = Path(override)
    else:
        log_dir = Path(__file__).resolve().parent.parent / "logs"

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        log_dir = Path(appdirs.user_data_dir(app_name))
        log_dir.mkdir(parents=True, exist_ok=True)

    return Path(log_dir, LOG_FILE_NAME)


def _console_handler(level=logging.INFO) -> logging.StreamHandler:
    """Return the console handler for the logger."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(),
            foreign_pre_chain=[structlog.processors.TimeStamper(fmt="iso")],
        )
    )
    return console_handler


def _file_handler(log_file: Path, level=logging.INFO) -> RotatingFileHandler:
    """Return the console handler for the logger."""
    file_handler = RotatingFileHandler(
        str(log_file), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=[structlog.processors.TimeStamper(fmt="iso")],
        )
    )
    return file_handler


def _processors() -> list:
    return [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]
