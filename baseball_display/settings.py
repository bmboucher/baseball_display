import json
import logging
import os
from pathlib import Path

from pydantic import BaseModel, Field

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
    # 16 MHz is the highest reliable clock on our 3-panel fanout. Above ~20
    # MHz the shared MOSI line shows bit errors with breadboard / jumper-wire
    # wiring and the panels render noise instead of solid color.
    spi_hz: int = 16_000_000
    # ST7796S is natively portrait (320x480). Our buffers are 480x320 landscape,
    # so MADCTL.MV (rotation 90 or 270) is required. Use 270 if the image
    # comes out upside-down.
    rotation: int = 90
    bgr: bool = True


_DEFAULT_PANELS: dict[str, PanelSettings] = {
    "left":    PanelSettings(cs_pin=8, led_pin=25),
    "right":   PanelSettings(cs_pin=7),
    "diamond": PanelSettings(cs_pin=0),
}


class WiFiSettings(BaseModel):
    ssid: str = ""
    password: str = ""


class Settings(BaseModel):
    refresh_rate: int = _DEFAULT_REFRESH_RATE
    multi_process: bool = False
    # Team abbreviation used by initialize_startup_mode() to pick the initial
    # game/mode at boot (LIVE if that team has a live game, else PREVIEW of
    # their next upcoming game, else MAIN_MENU).
    startup_team: str = "NYM"
    # Per-screen ST7796S panel configs. Override any field in settings.json,
    # e.g. {"panels": {"left": {"rotation": 180}}}.
    panels: dict[str, PanelSettings] = _DEFAULT_PANELS
    # WiFi credentials, entered via the WiFi Settings subscreen. Applied via
    # nmcli on Pi; persisted here too so the UI can pre-fill the editor.
    wifi: WiFiSettings = Field(default_factory=WiFiSettings)


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


def set_wifi_credentials(ssid: str, password: str) -> None:
    _settings.wifi = WiFiSettings(ssid=ssid, password=password)
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
