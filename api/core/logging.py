"""Centralized structured logging configuration."""

import logging
import sys


def setup_logging(debug: bool = False) -> logging.Logger:
    """Configure and return the application root logger."""
    log_level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger("urban_air")
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()
