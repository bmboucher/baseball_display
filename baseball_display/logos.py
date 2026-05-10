import io
import logging
import os
import urllib.request
from pathlib import Path
from typing import Optional, cast

import pygame
from reportlab.graphics import renderPM  # type: ignore[import-untyped]
from svglib.svglib import svg2rlg  # type: ignore[import-untyped]

from baseball_display.constants import MLB_LOGO_URL, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

_cache_dir: Path = Path(os.environ.get("CACHE_DIR", "./cache"))
_surfaces: dict[tuple[int, int, int], pygame.Surface] = {}


def get_logo(team_id: int, width: int, height: int) -> Optional[pygame.Surface]:
    """Return a Surface for *team_id* scaled to (width, height).

    Fetches and converts the SVG on first call; returns ``None`` on error.
    Subsequent calls for the same (team_id, width, height) return the cached surface.
    """
    key = (team_id, width, height)
    if key in _surfaces:
        return _surfaces[key]

    try:
        logo_dir = _cache_dir / "logos"
        logo_dir.mkdir(parents=True, exist_ok=True)
        svg_path = logo_dir / f"{team_id}.svg"

        if not svg_path.exists():
            url = MLB_LOGO_URL.format(team_id=team_id)
            logger.info("Downloading logo for team_id %d from %s", team_id, url)
            with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                svg_path.write_bytes(resp.read())

        drawing = svg2rlg(str(svg_path))
        if drawing is None:
            logger.warning("svg2rlg returned None for team_id %d", team_id)
            return None

        png_bytes = cast(bytes, renderPM.drawToString(drawing, fmt="PNG"))  # type: ignore[misc]
        surface = pygame.image.load(io.BytesIO(png_bytes)).convert_alpha()
        surface = pygame.transform.smoothscale(surface, (width, height))
        _surfaces[key] = surface
        logger.debug("Logo cached for team_id %d at %dx%d", team_id, width, height)
        return surface
    except Exception:
        logger.exception("Failed to load logo for team_id %d", team_id)
        return None
