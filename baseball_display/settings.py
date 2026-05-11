import json
import logging
import os
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)

SETTINGS_PATH_ENV = "BASEBALL_DISPLAY_SETTINGS"
MULTI_PROCESS_ENV = "BASEBALL_DISPLAY_MULTI_PROCESS"
_DEFAULT_SETTINGS_PATH = Path("./settings.json")

# Imported here to avoid a circular import with constants.py
_DEFAULT_REFRESH_RATE = 10


class PanelSettings(BaseModel):
    """Per-screen ST7796S panel wiring + bus settings.

    Defaults below match the wiring documented in PI_SETUP.md:
    SPI0 shared MOSI/MISO/SCLK, CS pins on GPIO8/7/0 (left/right/diamond),
    shared DC=GPIO1, shared RST=GPIO5, backlight on GPIO25 (declared only
    on the "left" panel).
    """

    cs_pin: int
    dc_pin: int = 1
    rst_pin: int = 5
    led_pin: int | None = None
    spi_bus: int = 0
    spi_device: int = 0
    spi_hz: int = 40_000_000
    rotation: int = 0
    bgr: bool = True


_DEFAULT_PANELS: dict[str, PanelSettings] = {
    "left":    PanelSettings(cs_pin=8, led_pin=25),
    "right":   PanelSettings(cs_pin=7),
    "diamond": PanelSettings(cs_pin=0),
}


class Settings(BaseModel):
    refresh_rate: int = _DEFAULT_REFRESH_RATE
    multi_process: bool = False
    # Per-screen ST7796S panel configs. Override any field in settings.json,
    # e.g. {"panels": {"left": {"rotation": 180}}}.
    panels: dict[str, PanelSettings] = _DEFAULT_PANELS


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


def resolve_panel(screen_name: str) -> PanelSettings | None:
    """Return the PanelSettings for *screen_name*, or None if unconfigured."""
    return _settings.panels.get(screen_name)
