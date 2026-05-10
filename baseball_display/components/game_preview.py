from __future__ import annotations

from typing import Any

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import ValueComponent, make_font
from baseball_display.logos import get_logo
from baseball_display.state import get_state


class GamePreview(ValueComponent):
    def __init__(self) -> None:
        super().__init__(
            pygame.Rect(
                0,
                0,
                dc.GAME_PREVIEW_SCREEN_W,
                dc.GAME_PREVIEW_SCREEN_H,
            )
        )

    def get_value(self) -> Any:
        app_state = get_state()
        game = app_state.selected_game or app_state.game_select.get_selected_game()
        if game is None:
            return None
        local_dt = game.game_date.astimezone()
        time_str = local_dt.strftime("%I:%M %p").lstrip("0")
        date_str = local_dt.strftime("%B %d, %Y").replace(" 0", " ")
        datetime_str = f"{date_str}{dc.GAME_PREVIEW_DATETIME_SEPARATOR}{time_str}"
        return (
            game.away_team_name,
            game.home_team_name,
            datetime_str,
            game.venue,
            game.away_team_id,
            game.home_team_id,
        )

    def render_value(self, value: Any) -> Surface:
        surf = Surface((dc.GAME_PREVIEW_SCREEN_W, dc.GAME_PREVIEW_SCREEN_H))
        surf.fill(dc.GAME_PREVIEW_COLOR_BG)

        if value is None:
            return surf

        (
            away_name,
            home_name,
            datetime_str,
            venue,
            away_id,
            home_id,
        ) = value

        team_font = make_font(dc.GAME_PREVIEW_TEAM_FONT_SIZE, bold=True)
        at_font = make_font(dc.GAME_PREVIEW_AT_FONT_SIZE)
        meta_font = make_font(dc.GAME_PREVIEW_META_FONT_SIZE)

        def render_centered(
            text: str,
            font: pygame.font.Font,
            y: int,
            color: tuple[int, int, int] = dc.GAME_PREVIEW_COLOR_TEXT,
        ) -> int:
            rendered = font.render(text, True, color)
            surf.blit(
                rendered,
                ((dc.GAME_PREVIEW_SCREEN_W - rendered.get_width()) // 2, y),
            )
            return y + rendered.get_height()

        team_h = team_font.get_height()
        at_h = at_font.get_height()
        meta_h = meta_font.get_height()
        divider_thickness = 1

        meta_lines = [datetime_str] + ([venue] if venue else [])
        teams_block_h = (
            team_h
            + dc.GAME_PREVIEW_LINE_GAP
            + at_h
            + dc.GAME_PREVIEW_LINE_GAP
            + team_h
        )
        divider_block_h = (
            dc.GAME_PREVIEW_DIVIDER_GAP
            + divider_thickness
            + dc.GAME_PREVIEW_DIVIDER_GAP
        )
        meta_block_h = len(meta_lines) * meta_h + (len(meta_lines) - 1) * dc.GAME_PREVIEW_LINE_GAP
        total_h = teams_block_h + divider_block_h + meta_block_h

        y = dc.GAME_PREVIEW_SCREEN_H - total_h - dc.GAME_PREVIEW_PAD

        logo_area_h = y - dc.GAME_PREVIEW_LOGO_TOP_PAD
        if logo_area_h > 0:
            logo_size = min(
                logo_area_h - 2 * dc.GAME_PREVIEW_LOGO_WHITE_PAD,
                (dc.GAME_PREVIEW_SCREEN_W - dc.GAME_PREVIEW_LOGO_GAP) // 2
                - 2 * dc.GAME_PREVIEW_LOGO_WHITE_PAD,
            )
            if logo_size > 0:
                tile = logo_size + 2 * dc.GAME_PREVIEW_LOGO_WHITE_PAD
                centre_x = dc.GAME_PREVIEW_SCREEN_W // 2
                logo_y_inner = (
                    dc.GAME_PREVIEW_LOGO_TOP_PAD
                    + (logo_area_h - tile) // 2
                    + dc.GAME_PREVIEW_LOGO_WHITE_PAD
                )

                for team_id, tile_x in (
                    (
                        away_id,
                        centre_x - dc.GAME_PREVIEW_LOGO_GAP // 2 - tile,
                    ),
                    (
                        home_id,
                        centre_x + dc.GAME_PREVIEW_LOGO_GAP // 2,
                    ),
                ):
                    pad_rect = pygame.Rect(
                        tile_x,
                        dc.GAME_PREVIEW_LOGO_TOP_PAD + (logo_area_h - tile) // 2,
                        tile,
                        tile,
                    )
                    pygame.draw.rect(surf, dc.GAME_PREVIEW_LOGO_TILE_BG, pad_rect)
                    logo_surf = get_logo(team_id, logo_size, logo_size)
                    if logo_surf:
                        surf.blit(
                            logo_surf,
                            (
                                tile_x + dc.GAME_PREVIEW_LOGO_WHITE_PAD,
                                logo_y_inner,
                            ),
                        )

        y = render_centered(away_name, team_font, y)
        y += dc.GAME_PREVIEW_LINE_GAP
        y = render_centered(
            dc.GAME_PREVIEW_AT_TEXT,
            at_font,
            y,
            dc.GAME_PREVIEW_AT_COLOR,
        )
        y += dc.GAME_PREVIEW_LINE_GAP
        y = render_centered(home_name, team_font, y)

        y += dc.GAME_PREVIEW_DIVIDER_GAP
        pygame.draw.line(
            surf,
            dc.GAME_PREVIEW_DIVIDER_COLOR,
            (dc.GAME_PREVIEW_PAD * 3, y),
            (dc.GAME_PREVIEW_SCREEN_W - dc.GAME_PREVIEW_PAD * 3, y),
        )
        y += divider_thickness + dc.GAME_PREVIEW_DIVIDER_GAP

        for i, line in enumerate(meta_lines):
            y = render_centered(line, meta_font, y, dc.GAME_PREVIEW_COLOR_TEXT)
            if i < len(meta_lines) - 1:
                y += dc.GAME_PREVIEW_LINE_GAP

        return surf
