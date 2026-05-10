from __future__ import annotations

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import Component, make_font
from baseball_display.state import get_game_display_data


class PitchDisplay(Component):
    def __init__(self) -> None:
        self._rect = pygame.Rect(
            0,
            0,
            dc.PITCH_DISPLAY_PITCH_PANEL_W,
            dc.PITCH_DISPLAY_PITCHER_AREA_H,
        )

    def draw(self, surface: Surface) -> None:
        data = get_game_display_data()

        panel = Surface(
            (dc.PITCH_DISPLAY_PITCH_PANEL_W, dc.PITCH_DISPLAY_PITCHER_AREA_H)
        )
        panel.fill(dc.PITCH_DISPLAY_COLOR_BG)

        self._draw_zone_area(panel, data.pitch_locations)
        self._draw_speed_area(panel, data.last_pitch_speed)

        surface.blit(panel, self._rect)

    # ── Zone diagram ──────────────────────────────────────────────────────────

    def _draw_zone_area(
        self,
        surface: Surface,
        pitch_locations: list[tuple[float, float, str]],
    ) -> None:
        # Background for zone area
        pygame.draw.rect(
            surface,
            dc.PITCH_DISPLAY_COLOR_ZONE_BG,
            pygame.Rect(
                0,
                0,
                dc.PITCH_DISPLAY_PITCH_PANEL_W,
                dc.PITCH_DISPLAY_ZONE_AREA_H,
            ),
        )

        # Drawn box fills the full available area (stretched, not square)
        box_x = dc.PITCH_DISPLAY_INNER_PAD
        box_y = dc.PITCH_DISPLAY_INNER_PAD
        box_w = dc.PITCH_DISPLAY_PITCH_PANEL_W - 2 * dc.PITCH_DISPLAY_INNER_PAD
        box_h = dc.PITCH_DISPLAY_ZONE_AREA_H - 2 * dc.PITCH_DISPLAY_INNER_PAD

        # Outer boundary
        pygame.draw.rect(
            surface,
            dc.PITCH_DISPLAY_COLOR_ZONE_BG,
            pygame.Rect(box_x, box_y, box_w, box_h),
        )

        # Strike zone inner rectangle
        outer_x_min = dc.PITCH_DISPLAY_ZONE_X_MIN - dc.PITCH_DISPLAY_OUTER_PAD
        outer_x_max = dc.PITCH_DISPLAY_ZONE_X_MAX + dc.PITCH_DISPLAY_OUTER_PAD
        outer_y_min = dc.PITCH_DISPLAY_ZONE_Y_MIN - dc.PITCH_DISPLAY_OUTER_PAD
        outer_y_max = dc.PITCH_DISPLAY_ZONE_Y_MAX + dc.PITCH_DISPLAY_OUTER_PAD
        span_x = outer_x_max - outer_x_min
        span_y = outer_y_max - outer_y_min

        def map_x(cx: float) -> int:
            return box_x + int((cx - outer_x_min) / span_x * box_w)

        def map_y(cy: float) -> int:
            # pZ increases upward; screen y increases downward — invert
            return box_y + int((1.0 - (cy - outer_y_min) / span_y) * box_h)

        # map_y is inverted: higher pZ -> lower screen y, so max pZ gives the top.
        zone_top = map_y(dc.PITCH_DISPLAY_ZONE_Y_MAX)
        zone_rect = pygame.Rect(
            map_x(dc.PITCH_DISPLAY_ZONE_X_MIN),
            zone_top,
            map_x(dc.PITCH_DISPLAY_ZONE_X_MAX)
            - map_x(dc.PITCH_DISPLAY_ZONE_X_MIN),
            map_y(dc.PITCH_DISPLAY_ZONE_Y_MIN) - zone_top,
        )
        pygame.draw.rect(surface, dc.PITCH_DISPLAY_COLOR_ZONE_RECT, zone_rect, 1)

        # Find the index of the last entry with a real (non-sentinel) position
        last_valid_idx = -1
        for i, (px_c, py_c, _) in enumerate(pitch_locations):
            if (px_c, py_c) != dc.PITCH_DISPLAY_AUTO_BALL_POS:
                last_valid_idx = i

        # Draw all pitch dots, then halo on the most recent valid one
        for i, (px_c, py_c, cat) in enumerate(pitch_locations):
            if (px_c, py_c) == dc.PITCH_DISPLAY_AUTO_BALL_POS:
                continue
            px = map_x(px_c)
            py = map_y(py_c)
            # Clamp to outer box bounds
            px = max(
                box_x + dc.PITCH_DISPLAY_HALO_RADIUS,
                min(box_x + box_w - dc.PITCH_DISPLAY_HALO_RADIUS, px),
            )
            py = max(
                box_y + dc.PITCH_DISPLAY_HALO_RADIUS,
                min(box_y + box_h - dc.PITCH_DISPLAY_HALO_RADIUS, py),
            )
            color = dc.PITCH_DISPLAY_CATEGORY_DOT_COLORS.get(
                cat,
                dc.PITCH_DISPLAY_COLOR_IN_PLAY_DOT,
            )
            pygame.draw.circle(surface, color, (px, py), dc.PITCH_DISPLAY_DOT_RADIUS)
            if i == last_valid_idx:
                pygame.draw.circle(
                    surface,
                    dc.PITCH_DISPLAY_COLOR_HALO,
                    (px, py),
                    dc.PITCH_DISPLAY_HALO_RADIUS,
                    1,
                )

    # ── Speed readout ─────────────────────────────────────────────────────────

    def _draw_speed_area(self, surface: Surface, speed: float | None) -> None:
        y0 = dc.PITCH_DISPLAY_ZONE_AREA_H
        # Divider
        pygame.draw.line(
            surface,
            dc.PITCH_DISPLAY_COLOR_DIVIDER,
            (0, y0),
            (dc.PITCH_DISPLAY_PITCH_PANEL_W, y0),
        )

        speed_font = make_font(dc.PITCH_DISPLAY_SPEED_FONT_SIZE, bold=True)
        mph_font = make_font(dc.PITCH_DISPLAY_MPH_FONT_SIZE)

        speed_str = (
            f"{speed:.1f}" if speed is not None else dc.PITCH_DISPLAY_EMPTY_SPEED_TEXT
        )
        speed_surf = speed_font.render(speed_str, True, dc.PITCH_DISPLAY_COLOR_SPEED)
        mph_surf = mph_font.render(
            dc.PITCH_DISPLAY_MPH_TEXT,
            True,
            dc.PITCH_DISPLAY_COLOR_MPH,
        )

        total_h = speed_surf.get_height() + mph_surf.get_height() + 2
        start_y = y0 + (dc.PITCH_DISPLAY_SPEED_AREA_H - total_h) // 2

        speed_x = (dc.PITCH_DISPLAY_PITCH_PANEL_W - speed_surf.get_width()) // 2
        surface.blit(speed_surf, (speed_x, start_y))

        mph_x = (dc.PITCH_DISPLAY_PITCH_PANEL_W - mph_surf.get_width()) // 2
        surface.blit(mph_surf, (mph_x, start_y + speed_surf.get_height() + 2))
