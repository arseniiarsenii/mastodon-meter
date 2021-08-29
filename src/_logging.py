import sys

# set up logging configurations
BASE_LOGGING_CONFIG = {
    "colorize": True,
    "backtrace": True,
    "diagnose": True,
    "catch": True,
}

# logging settings for the console logs
CONSOLE_LOGGING_CONFIG = {
    **BASE_LOGGING_CONFIG,  # type: ignore
    "level": "INFO",
    "sink": sys.stdout,
}

# logging settings for the log file
FILE_LOGGING_CONFIG = {
    **BASE_LOGGING_CONFIG,  # type: ignore
    "level": "DEBUG",
    "sink": "mastodon-meter.log",
    "rotation": "10 MB",
    "compression": "zip",
}
