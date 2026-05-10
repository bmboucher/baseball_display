from __future__ import annotations

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import Component, make_font
from baseball_display.state import (
    DisplayMode,
    PAEvent,
    get_game_display_data,
    get_state,
)


def _wrap_text(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    """Split text into lines that fit within max_w pixels."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if font.size(candidate)[0] <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _fit_single_line(text: str, font: pygame.font.Font, max_w: int) -> str:
    """Trim text to a single line that fits within max_w pixels."""
    if font.size(text)[0] <= max_w:
        return text

    ellipsis = dc.PA_EVENTS_ELLIPSIS
    trimmed = text.rstrip()
    while trimmed:
        candidate = f"{trimmed}{ellipsis}"
        if font.size(candidate)[0] <= max_w:
            return candidate
        trimmed = trimmed[:-1].rstrip()

    return ellipsis if font.size(ellipsis)[0] <= max_w else ""


def _render_content(events: tuple[PAEvent, ...]) -> tuple[Surface, int]:
    """Render all event blocks onto a single tall surface.

    Returns the surface and its total pixel height.  The surface height equals
    max(total_h, 1) so it is always valid even when events is empty.
    """
    font = make_font(dc.PA_EVENTS_FONT_SIZE)
    line_h = font.get_linesize()
    inner_w = dc.PA_EVENTS_AREA_W - 2 * dc.PA_EVENTS_PAD

    blocks: list[tuple[PAEvent, list[str], int]] = []
    for event in events:
        if event.right_text is not None:
            # Pitch row: single line, no wrapping
            lines = [event.text]
        else:
            lines = _wrap_text(event.text, font, inner_w)
        block_h = len(lines) * line_h + 2 * dc.PA_EVENTS_PAD
        blocks.append((event, lines, block_h))

    total_h = sum(bh for _, _, bh in blocks) + dc.PA_EVENTS_GAP * max(
        len(blocks) - 1,
        0,
    )
    surf_h = max(total_h, 1)
    surf = Surface((dc.PA_EVENTS_AREA_W, surf_h))
    surf.fill(dc.PA_EVENTS_COLOR_BG)

    y = 0
    for event, lines, block_h in blocks:
        color = dc.PA_EVENTS_CATEGORY_COLORS.get(
            event.category,
            dc.PA_EVENTS_COLOR_IN_PLAY,
        )
        pygame.draw.rect(
            surf,
            color,
            pygame.Rect(0, y, dc.PA_EVENTS_AREA_W, block_h),
        )
        right_surf: Surface | None = None
        max_left_w = inner_w
        if event.right_text is not None:
            right_surf = font.render(event.right_text, True, dc.PA_EVENTS_COLOR_TEXT)
            max_left_w = max(
                0,
                inner_w - right_surf.get_width() - dc.PA_EVENTS_RIGHT_TEXT_GAP,
            )
            lines = [_fit_single_line(event.text, font, max_left_w)]

        for i, line in enumerate(lines):
            text_surf = font.render(line, True, dc.PA_EVENTS_COLOR_TEXT)
            surf.blit(
                text_surf,
                (
                    dc.PA_EVENTS_PAD,
                    y + dc.PA_EVENTS_PAD + i * line_h,
                ),
            )
        # Right-aligned outcome text on the last (only) line of pitch rows
        if right_surf is not None:
            rx = dc.PA_EVENTS_AREA_W - dc.PA_EVENTS_PAD - right_surf.get_width()
            surf.blit(right_surf, (rx, y + dc.PA_EVENTS_PAD))
        y += block_h + dc.PA_EVENTS_GAP

    return surf, total_h


class PAEvents(Component):
    def __init__(self) -> None:
        self._rect = pygame.Rect(
            dc.PA_EVENTS_PITCH_PANEL_W,
            0,
            dc.PA_EVENTS_AREA_W,
            dc.PA_EVENTS_AREA_H,
        )

        # Cached pre-rendered content surface
        self._last_events: tuple[PAEvent, ...] = ()
        self._content_surf: Surface
        self._content_h: int
        self._content_surf, self._content_h = _render_content(())

        # Animation state
        self._scroll_pos: float = 0.0  # pixels from top currently visible
        self._direction: int = 1  # 1 = scrolling down, -1 = scrolling up
        self._pause_remaining: float = dc.PA_EVENTS_PAUSE_SECS
        self._last_tick: int = pygame.time.get_ticks()

    def _reset_animation(self) -> None:
        overflow = max(self._content_h - dc.PA_EVENTS_AREA_H, 0)
        self._scroll_pos = float(overflow)  # start at bottom (most recent events)
        self._direction = -1  # scroll upward first
        self._pause_remaining = dc.PA_EVENTS_PAUSE_SECS
        self._last_tick = pygame.time.get_ticks()

    def draw(self, surface: Surface) -> None:
        events = tuple(get_game_display_data().pa_events)

        # Rebuild content surface only when events change
        if events != self._last_events:
            self._last_events = events
            self._content_surf, self._content_h = _render_content(events)
            self._reset_animation()

        panel = Surface((dc.PA_EVENTS_AREA_W, dc.PA_EVENTS_AREA_H))
        panel.fill(dc.PA_EVENTS_COLOR_BG)

        overflow = self._content_h - dc.PA_EVENTS_AREA_H

        if overflow <= 0:
            # Content fits — top-aligned, no animation
            panel.blit(self._content_surf, (0, 0))
        elif get_state().mode != DisplayMode.REPLAY:
            # LIVE (or any non-REPLAY) mode — pin to bottom so newest is visible
            panel.blit(self._content_surf, (0, -overflow))
        else:
            # REPLAY mode with overflow — animated scroll
            now = pygame.time.get_ticks()
            dt = min((now - self._last_tick) / 1000.0, dc.PA_EVENTS_MAX_DT)
            self._last_tick = now

            if self._pause_remaining > 0.0:
                self._pause_remaining -= dt
            else:
                self._scroll_pos += self._direction * dc.PA_EVENTS_SCROLL_SPEED * dt
                if self._scroll_pos >= overflow:
                    self._scroll_pos = float(overflow)
                    self._direction = -1
                    self._pause_remaining = dc.PA_EVENTS_PAUSE_SECS
                elif self._scroll_pos <= 0.0:
                    self._scroll_pos = 0.0
                    self._direction = 1
                    self._pause_remaining = dc.PA_EVENTS_PAUSE_SECS

            panel.blit(self._content_surf, (0, -int(self._scroll_pos)))

        surface.blit(panel, self._rect)
