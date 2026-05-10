from __future__ import annotations

from datetime import datetime

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import Component, make_font
from baseball_display.state import get_state


def _format_delta(total_seconds: float) -> str:
    if total_seconds <= 0:
        return dc.GAME_COUNTDOWN_STARTING_NOW_TEXT
    secs = int(total_seconds)
    days, remainder = divmod(secs, 86400)
    hours, remainder2 = divmod(remainder, 3600)
    mins, s = divmod(remainder2, 60)
    if days > 0:
        return f"{days}d {hours:02d}:{mins:02d}:{s:02d}"
    return f"{hours:02d}:{mins:02d}:{s:02d}"


class GameCountdown(Component):
    def __init__(self) -> None:
        self._rect = pygame.Rect(
            0,
            0,
            dc.GAME_COUNTDOWN_SCREEN_W,
            dc.GAME_COUNTDOWN_SCREEN_H,
        )

    def draw(self, surface: Surface) -> None:
        panel = Surface((dc.GAME_COUNTDOWN_SCREEN_W, dc.GAME_COUNTDOWN_SCREEN_H))
        panel.fill(dc.GAME_COUNTDOWN_COLOR_BG)

        game = get_state().selected_game
        if game is not None:
            now = datetime.now().astimezone()
            delta = (game.game_date - now).total_seconds()
            countdown_str = _format_delta(delta)

            label_font = make_font(dc.GAME_COUNTDOWN_LABEL_FONT_SIZE)
            countdown_font = make_font(dc.GAME_COUNTDOWN_COUNTDOWN_FONT_SIZE, bold=True)

            label_surf = label_font.render(
                dc.GAME_COUNTDOWN_LABEL_TEXT,
                True,
                dc.GAME_COUNTDOWN_COLOR_LABEL,
            )
            countdown_surf = countdown_font.render(
                countdown_str,
                True,
                dc.GAME_COUNTDOWN_COLOR_TEXT,
            )

            total_h = (
                label_surf.get_height()
                + dc.GAME_COUNTDOWN_LINE_GAP
                + countdown_surf.get_height()
            )
            start_y = (dc.GAME_COUNTDOWN_SCREEN_H - total_h) // 2

            label_x = (dc.GAME_COUNTDOWN_SCREEN_W - label_surf.get_width()) // 2
            panel.blit(label_surf, (label_x, start_y))

            countdown_x = (
                dc.GAME_COUNTDOWN_SCREEN_W - countdown_surf.get_width()
            ) // 2
            panel.blit(
                countdown_surf,
                (
                    countdown_x,
                    start_y
                    + label_surf.get_height()
                    + dc.GAME_COUNTDOWN_LINE_GAP,
                ),
            )

        surface.blit(panel, self._rect)
