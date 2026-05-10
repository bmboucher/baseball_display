from __future__ import annotations

from typing import Any

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import ValueComponent, make_font
from baseball_display.state import get_game_display_data


class CountDisplay(ValueComponent):
    def __init__(self) -> None:
        rect = pygame.Rect(
            dc.COUNT_DISPLAY_SCREEN_W - dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W,
            dc.COUNT_DISPLAY_CLOCK_DISPLAY_H,
            dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W,
            dc.COUNT_DISPLAY_PITCHER_AREA_H - dc.COUNT_DISPLAY_CLOCK_DISPLAY_H,
        )
        super().__init__(rect)

    def get_value(self) -> Any:
        dd = get_game_display_data()
        return (dd.balls, dd.strikes, dd.outs)

    def render_value(self, value: Any) -> Surface:
        balls, strikes, outs = value
        panel_h = dc.COUNT_DISPLAY_PITCHER_AREA_H - dc.COUNT_DISPLAY_CLOCK_DISPLAY_H
        surf = Surface((dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W, panel_h))

        sections: list[tuple[str, int, tuple[int, int, int], int]] = [
            (dc.COUNT_DISPLAY_SECTIONS[0][0], balls, dc.COUNT_DISPLAY_SECTIONS[0][1], dc.COUNT_DISPLAY_SECTIONS[0][2]),
            (dc.COUNT_DISPLAY_SECTIONS[1][0], strikes, dc.COUNT_DISPLAY_SECTIONS[1][1], dc.COUNT_DISPLAY_SECTIONS[1][2]),
            (dc.COUNT_DISPLAY_SECTIONS[2][0], outs, dc.COUNT_DISPLAY_SECTIONS[2][1], dc.COUNT_DISPLAY_SECTIONS[2][2]),
        ]
        section_h = panel_h // len(sections)
        font = make_font(dc.COUNT_DISPLAY_BSO_FONT_SIZE)
        dot_area_w = (
            dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W
            - dc.COUNT_DISPLAY_LETTER_AREA_W
            - dc.COUNT_DISPLAY_RIGHT_PAD
        )

        for row, (label, count, dot_color, max_dots) in enumerate(sections):
            y0 = row * section_h
            this_h = section_h if row < len(sections) - 1 else panel_h - y0
            center_y = y0 + this_h // 2

            pygame.draw.rect(
                surf,
                dc.COUNT_DISPLAY_BG_COLORS[row],
                pygame.Rect(0, y0, dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W, this_h),
            )

            label_surf = font.render(label, True, dc.COUNT_DISPLAY_COLOR_TEXT)
            lx = (
                dc.COUNT_DISPLAY_SCOREBOARD_BSO_PANEL_W - label_surf.get_width()
            ) // 2 - dot_area_w // 2
            ly = center_y - label_surf.get_height() // 2
            surf.blit(label_surf, (lx, ly))

            total_dot_span = (
                (max_dots - 1) * dc.COUNT_DISPLAY_DOT_SPACING
                + 2 * dc.COUNT_DISPLAY_DOT_RADIUS
            )
            dot_x = (
                dc.COUNT_DISPLAY_LETTER_AREA_W
                + (dot_area_w - total_dot_span) // 2
                + dc.COUNT_DISPLAY_DOT_RADIUS
            )
            for i in range(max_dots):
                color = dot_color if i < count else dc.COUNT_DISPLAY_COLOR_EMPTY
                pygame.draw.circle(
                    surf,
                    color,
                    (dot_x, center_y),
                    dc.COUNT_DISPLAY_DOT_RADIUS,
                )
                dot_x += dc.COUNT_DISPLAY_DOT_SPACING

        return surf
