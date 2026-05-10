import logging
import os
import urllib.request
from pathlib import Path
from typing import Optional

import pygame

from baseball_display.constants import MLB_PLAYER_PHOTO_URL, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

_cache_dir: Path = Path(os.environ.get("CACHE_DIR", "./cache"))
_surfaces: dict[tuple[int, int, int], pygame.Surface] = {}


def get_player_photo(mlb_id: int, width: int, height: int) -> Optional[pygame.Surface]:
    """Return a Surface for the player headshot scaled to (width, height).

    Downloads and caches the PNG on first call; returns None on error.
    Subsequent calls for the same (mlb_id, width, height) return the cached surface.
    """
    key = (mlb_id, width, height)
    if key in _surfaces:
        return _surfaces[key]

    try:
        photo_dir = _cache_dir / "player_photos"
        photo_dir.mkdir(parents=True, exist_ok=True)
        photo_path = photo_dir / f"{mlb_id}.png"

        if not photo_path.exists():
            url = MLB_PLAYER_PHOTO_URL.format(mlb_id=mlb_id)
            logger.info("Downloading player photo for mlb_id %d from %s", mlb_id, url)
            req = urllib.request.Request(
                url, headers={"User-Agent": "baseball-display/1.0"}
            )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                photo_path.write_bytes(resp.read())

        surface = pygame.image.load(str(photo_path)).convert_alpha()
        # Scale to fit within (width, height) while preserving aspect ratio
        orig_w, orig_h = surface.get_size()
        scale = min(width / orig_w, height / orig_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))
        surface = pygame.transform.smoothscale(surface, (new_w, new_h))
        _surfaces[key] = surface
        logger.debug(
            "Player photo loaded for mlb_id %d at %dx%d", mlb_id, width, height
        )
        return surface
    except Exception:
        logger.exception("Failed to load player photo for mlb_id %d", mlb_id)
        return None
