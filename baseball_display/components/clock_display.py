from __future__ import annotations

from typing import Any

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import ValueComponent, make_font
from baseball_display.state import get_game_display_data


class ClockDisplay(ValueComponent):
    def __init__(self) -> None:
        rect = pygame.Rect(
            dc.CLOCK_DISPLAY_SCREEN_W - dc.CLOCK_DISPLAY_SCOREBOARD_BSO_PANEL_W,
            0,
            dc.CLOCK_DISPLAY_SCOREBOARD_BSO_PANEL_W,
            dc.CLOCK_DISPLAY_H,
        )
        super().__init__(rect)

    def get_value(self) -> Any:
        return get_game_display_data().clock

    def render_value(self, value: Any) -> Surface:
        font = make_font(dc.CLOCK_DISPLAY_FONT_SIZE, bold=True)
        text_surf = font.render(str(value), True, dc.CLOCK_DISPLAY_COLOR_TEXT)
        surf = Surface(self._rect.size)
        surf.fill(dc.CLOCK_DISPLAY_COLOR_BG)
        x = (
            dc.CLOCK_DISPLAY_SCOREBOARD_BSO_PANEL_W - text_surf.get_width()
        ) // 2
        y = (dc.CLOCK_DISPLAY_H - text_surf.get_height()) // 2
        surf.blit(text_surf, (x, y))
        return surf
