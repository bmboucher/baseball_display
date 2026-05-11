import json
import logging
import os
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)

SETTINGS_PATH_ENV = "BASEBALL_DISPLAY_SETTINGS"
MULTI_PROCESS_ENV = "BASEBALL_DISPLAY_MULTI_PROCESS"
FBDEV_ENV_PREFIX = "BASEBALL_DISPLAY_FBDEV_"
_DEFAULT_SETTINGS_PATH = Path("./settings.json")

# Imported here to avoid a circular import with constants.py
_DEFAULT_REFRESH_RATE = 10


class Settings(BaseModel):
    refresh_rate: int = _DEFAULT_REFRESH_RATE
    multi_process: bool = False
    # Per-screen framebuffer devices in multi-process mode, e.g.
    #   {"left": "/dev/fb1", "right": "/dev/fb2", "diamond": "/dev/fb3"}
    # Each render child will set SDL_VIDEODRIVER=fbcon + SDL_FBDEV=<path>
    # before initializing pygame. Env var overrides per screen via
    # BASEBALL_DISPLAY_FBDEV_LEFT / _RIGHT / _DIAMOND.
    screen_fbdevs: dict[str, str] = {}


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


def is_multi_process_enabled() -> bool:
    """Env var override; falls back to settings.json `multi_process` field."""
    env = os.environ.get(MULTI_PROCESS_ENV)
    if env is not None:
        return env.strip().lower() in {"1", "true", "yes", "on"}
    return _settings.multi_process


def resolve_fbdev(screen_name: str) -> str | None:
    """Return the framebuffer device path for *screen_name*, or None.

    Env var (e.g. ``BASEBALL_DISPLAY_FBDEV_LEFT``) overrides the setting.
    """
    env = os.environ.get(FBDEV_ENV_PREFIX + screen_name.upper())
    if env:
        return env
    return _settings.screen_fbdevs.get(screen_name)
