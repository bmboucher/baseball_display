from logging.config import dictConfig


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "loggers": {
                "baseball_display": {
                    "handlers": ["console"],
                    "level": "INFO",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "simple",
                },
            },
            "formatters": {
                "simple": {
                    "format": "[%(asctime)s] %(levelname)s - %(message)s",
                },
            },
        }
    )
