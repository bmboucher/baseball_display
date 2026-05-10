import json
import logging
import os
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)

SETTINGS_PATH_ENV = "BASEBALL_DISPLAY_SETTINGS"
_DEFAULT_SETTINGS_PATH = Path("./settings.json")

# Imported here to avoid a circular import with constants.py
_DEFAULT_REFRESH_RATE = 10


class Settings(BaseModel):
    refresh_rate: int = _DEFAULT_REFRESH_RATE


_settings: Settings = Settings()


def _get_path() -> Path:
    env_val = os.environ.get(SETTINGS_PATH_ENV)
    return Path(env_val) if env_val else _DEFAULT_SETTINGS_PATH


def load_settings() -> None:
    """Load settings from the JSON file.  Silently uses defaults on any failure."""
    global _settings
    path = _get_path()
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            _settings = Settings.model_validate(data)
            logger.info("Loaded settings from %s", path)
    except Exception:
        logger.exception("Failed to load settings from %s — using defaults", path)
        _settings = Settings()


def save_settings() -> None:
    """Persist the current settings to the JSON file."""
    path = _get_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_settings.model_dump_json(indent=2), encoding="utf-8")
        logger.info("Saved settings to %s", path)
    except Exception:
        logger.exception("Failed to save settings to %s", path)


def get_settings() -> Settings:
    return _settings


def set_refresh_rate(value: int) -> None:
    _settings.refresh_rate = value
    save_settings()
