"""Fetch MLB team logos (SVG) and convert them to transparent pygame Surfaces.

The MLB logo SVGs are rasterized with ``svglib`` + ``reportlab``'s ``renderPM``
backend, which only emits opaque RGB (it has no usable alpha support). Rendering
once would trap every logo inside a solid white square. To recover a real alpha
channel we rasterize each logo twice -- once on a white background and once on a
black background -- and solve for the per-pixel coverage from the difference.
"""

import io
import logging
import os
import urllib.request
from pathlib import Path
from typing import Optional, cast

import pygame
from PIL import Image
from reportlab.graphics import renderPM  # type: ignore[import-untyped]
import svglib.svglib as svglib  # type: ignore[import-untyped]

from baseball_display.constants import MLB_LOGO_URL, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

_cache_dir: Path = Path(os.environ.get("CACHE_DIR", "./cache"))
_native_surfaces: dict[int, pygame.Surface] = {}
_scaled_surfaces: dict[tuple[int, int, int], pygame.Surface] = {}

_WHITE_BACKGROUND = 0xFFFFFF
_BLACK_BACKGROUND = 0x000000


def get_logo(team_id: int, width: int, height: int) -> Optional[pygame.Surface]:
    """Return a Surface for *team_id* scaled to (width, height).

    Fetches and converts the SVG on first call; returns ``None`` on error.
    Subsequent calls for the same (team_id, width, height) return the cached surface.
    """
    key = (team_id, width, height)
    if key in _scaled_surfaces:
        return _scaled_surfaces[key]

    try:
        native = _get_native_surface(team_id)
        if native is None:
            return None
        scaled = pygame.transform.smoothscale(native, (width, height))
        _scaled_surfaces[key] = scaled
        logger.debug("Logo cached for team_id %d at %dx%d", team_id, width, height)
        return scaled
    except Exception:
        logger.exception("Failed to load logo for team_id %d", team_id)
        return None


###### PRIVATE #######


def _get_native_surface(team_id: int) -> Optional[pygame.Surface]:
    """Rasterize the team's SVG to a transparent Surface at its native size, cached."""
    if team_id in _native_surfaces:
        return _native_surfaces[team_id]

    svg_path = _ensure_svg_downloaded(team_id)
    on_white = _render_svg_on_background(svg_path, _WHITE_BACKGROUND)
    on_black = _render_svg_on_background(svg_path, _BLACK_BACKGROUND)
    if on_white is None or on_black is None:
        return None

    rgba = _recover_alpha(on_white, on_black)
    surface = pygame.image.fromstring(rgba.tobytes(), rgba.size, "RGBA")
    _native_surfaces[team_id] = surface
    return surface


def _ensure_svg_downloaded(team_id: int) -> Path:
    """Return the local SVG path for *team_id*, downloading it if not yet cached."""
    logo_dir = _cache_dir / "logos"
    logo_dir.mkdir(parents=True, exist_ok=True)
    svg_path = logo_dir / f"{team_id}.svg"

    if not svg_path.exists():
        url = MLB_LOGO_URL.format(team_id=team_id)
        logger.info("Downloading logo for team_id %d from %s", team_id, url)
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            svg_path.write_bytes(response.read())

    return svg_path


def _render_svg_on_background(svg_path: Path, background: int) -> Optional[Image.Image]:
    """Rasterize an SVG onto a solid *background* color, returning an RGB image."""
    drawing = svglib.svg2rlg(str(svg_path))
    if drawing is None:
        logger.warning("svg2rlg returned None for %s", svg_path)
        return None

    png_bytes = cast(bytes, renderPM.drawToString(drawing, fmt="PNG", bg=background))  # type: ignore[misc]
    return Image.open(io.BytesIO(png_bytes)).convert("RGB")


def _recover_alpha(on_white: Image.Image, on_black: Image.Image) -> Image.Image:
    """Recover a straight-alpha RGBA image from the same logo drawn on two backgrounds.

    A pixel of true color ``C`` and coverage ``a`` composites onto background ``B``
    as ``C*a + B*(1-a)``. Drawing on black (B=0) gives ``C*a`` (premultiplied color),
    and the white/black difference gives ``255*(1-a)``, so ``a`` and the straight
    color ``C = (C*a)/a`` both fall out per pixel.
    """
    width, height = on_white.size
    white_px = on_white.load()
    black_px = on_black.load()

    rgba = Image.new("RGBA", (width, height))
    out_px = rgba.load()
    for y in range(height):
        for x in range(width):
            red_w, green_w, blue_w = white_px[x, y]
            red_b, green_b, blue_b = black_px[x, y]

            coverage = 255 - ((red_w - red_b) + (green_w - green_b) + (blue_w - blue_b)) // 3
            coverage = max(0, min(255, coverage))
            if coverage == 0:
                out_px[x, y] = (0, 0, 0, 0)
                continue

            # Un-premultiply the black-background color (C*a) back to straight color C.
            red = min(255, red_b * 255 // coverage)
            green = min(255, green_b * 255 // coverage)
            blue = min(255, blue_b * 255 // coverage)
            out_px[x, y] = (red, green, blue, coverage)

    return rgba
