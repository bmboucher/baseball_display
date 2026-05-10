from typing import Optional

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display import logos, state
from baseball_display.components.base import Component, make_font
from baseball_display.state import get_game_display_data


def _draw_cell(
    surface: Surface,
    text: str,
    rect: pygame.Rect,
    bg: tuple[int, int, int],
    fg: tuple[int, int, int],
    font: pygame.font.Font,
) -> None:
    pygame.draw.rect(surface, bg, rect)
    img = font.render(text, True, fg)
    surface.blit(img, img.get_rect(center=rect.center))


def _draw_team_cell(
    surface: Surface,
    abbreviation: str,
    team_id: int,
    rect: pygame.Rect,
    bg: tuple[int, int, int],
) -> None:
    pygame.draw.rect(surface, bg, rect)
    logo_size = min(rect.width, rect.height) - 2 * dc.SCOREBOARD_LOGO_PAD
    logo = logos.get_logo(team_id, logo_size, logo_size)
    if logo is not None:
        logo_rect = logo.get_rect(center=rect.center)
        white_rect = logo_rect.inflate(
            2 * dc.SCOREBOARD_LOGO_PAD,
            2 * dc.SCOREBOARD_LOGO_PAD,
        )
        pygame.draw.rect(surface, dc.SCOREBOARD_COLOR_LOGO_BG, white_rect)
        surface.blit(logo, logo_rect)
    else:
        img = make_font(dc.SCOREBOARD_FONT_SIZE).render(
            abbreviation,
            True,
            dc.SCOREBOARD_COLOR_TEXT,
        )
        surface.blit(img, img.get_rect(center=rect.center))


class Scoreboard(Component):
    def draw(self, surface: Surface) -> None:
        dd = get_game_display_data()
        surface.fill(dc.SCOREBOARD_COLOR_BG)

        if not dd.inning_runs:
            msg = make_font(dc.SCOREBOARD_FONT_SIZE).render(
                dc.SCOREBOARD_LOADING_TEXT,
                True,
                dc.COLOR_SCOREBOARD_DIMMED,
            )
            surface.blit(
                msg,
                msg.get_rect(
                    center=(dc.SCOREBOARD_SCREEN_W // 2, dc.SCOREBOARD_SCREEN_H // 2)
                ),
            )
            return

        selected = state.get_state().selected_game
        if selected is None:
            return
        away_team_id = selected.away_team_id
        home_team_id = selected.home_team_id

        num_innings = len(dd.inning_runs)

        inning_col_w = (
            dc.SCOREBOARD_SCREEN_W
            - dc.SCOREBOARD_TEAM_COL_W
            - 3 * dc.SCOREBOARD_RHE_COL_W
        ) // num_innings

        away_runs: list[Optional[int]] = [
            dd.inning_runs[i].top for i in range(num_innings)
        ]
        home_runs: list[Optional[int]] = [
            dd.inning_runs[i].bottom for i in range(num_innings)
        ]

        away_r = dd.runs.top or 0
        away_h = dd.hits.top or 0
        away_e = dd.errors.bottom or 0
        home_r = dd.runs.bottom or 0
        home_h = dd.hits.bottom or 0
        home_e = dd.errors.top or 0

        row_h = dc.SCOREBOARD_TEAM_COL_W
        y_offset = dc.SCOREBOARD_SCREEN_H - dc.SCOREBOARD_H
        header_y = y_offset
        away_y = y_offset + dc.SCOREBOARD_HEADER_HEIGHT
        home_y = away_y + row_h

        font = make_font(dc.SCOREBOARD_FONT_SIZE)
        score_font = make_font(dc.SCOREBOARD_SCORE_FONT_SIZE, bold=True)

        def x_for_inning(i: int) -> int:
            return dc.SCOREBOARD_TEAM_COL_W + i * inning_col_w

        def x_rhe(col: int) -> int:
            return (
                dc.SCOREBOARD_TEAM_COL_W
                + num_innings * inning_col_w
                + col * dc.SCOREBOARD_RHE_COL_W
            )

        _draw_cell(
            surface,
            "",
            pygame.Rect(
                0,
                header_y,
                dc.SCOREBOARD_TEAM_COL_W,
                dc.SCOREBOARD_HEADER_HEIGHT,
            ),
            dc.COLOR_SCOREBOARD_HEADER_BG,
            dc.SCOREBOARD_COLOR_TEXT,
            font,
        )
        for i in range(num_innings):
            _draw_cell(
                surface,
                str(i + 1),
                pygame.Rect(
                    x_for_inning(i),
                    header_y,
                    inning_col_w,
                    dc.SCOREBOARD_HEADER_HEIGHT,
                ),
                dc.COLOR_SCOREBOARD_HEADER_BG,
                dc.SCOREBOARD_COLOR_TEXT,
                font,
            )
        for col, label in enumerate(dc.SCOREBOARD_TOTAL_LABELS):
            _draw_cell(
                surface,
                label,
                pygame.Rect(
                    x_rhe(col),
                    header_y,
                    dc.SCOREBOARD_RHE_COL_W,
                    dc.SCOREBOARD_HEADER_HEIGHT,
                ),
                dc.COLOR_SCOREBOARD_RHE_BG,
                dc.SCOREBOARD_COLOR_TEXT,
                font,
            )

        _draw_team_cell(
            surface,
            selected.away_team,
            away_team_id,
            pygame.Rect(0, away_y, dc.SCOREBOARD_TEAM_COL_W, row_h),
            dc.COLOR_SCOREBOARD_AWAY_BG,
        )
        for i, val in enumerate(away_runs):
            if val is None:
                text, fg = dc.SCOREBOARD_EMPTY_INNING_TEXT, dc.COLOR_SCOREBOARD_DIMMED
            else:
                text, fg = str(val), dc.SCOREBOARD_COLOR_TEXT
            _draw_cell(
                surface,
                text,
                pygame.Rect(x_for_inning(i), away_y, inning_col_w, row_h),
                dc.COLOR_SCOREBOARD_AWAY_BG,
                fg,
                score_font,
            )
        for col, val in enumerate((away_r, away_h, away_e)):
            _draw_cell(
                surface,
                str(val),
                pygame.Rect(x_rhe(col), away_y, dc.SCOREBOARD_RHE_COL_W, row_h),
                dc.COLOR_SCOREBOARD_RHE_BG,
                dc.SCOREBOARD_COLOR_TEXT,
                score_font,
            )

        _draw_team_cell(
            surface,
            selected.home_team,
            home_team_id,
            pygame.Rect(0, home_y, dc.SCOREBOARD_TEAM_COL_W, row_h),
            dc.COLOR_SCOREBOARD_HOME_BG,
        )
        for i, val in enumerate(home_runs):
            if val is None:
                text, fg = dc.SCOREBOARD_EMPTY_INNING_TEXT, dc.COLOR_SCOREBOARD_DIMMED
            else:
                text, fg = str(val), dc.SCOREBOARD_COLOR_TEXT
            _draw_cell(
                surface,
                text,
                pygame.Rect(x_for_inning(i), home_y, inning_col_w, row_h),
                dc.COLOR_SCOREBOARD_HOME_BG,
                fg,
                score_font,
            )
        for col, val in enumerate((home_r, home_h, home_e)):
            _draw_cell(
                surface,
                str(val),
                pygame.Rect(x_rhe(col), home_y, dc.SCOREBOARD_RHE_COL_W, row_h),
                dc.COLOR_SCOREBOARD_RHE_BG,
                dc.SCOREBOARD_COLOR_TEXT,
                score_font,
            )

        active_i = dd.active_inning_idx
        if active_i is not None and active_i < num_innings:
            bx = x_for_inning(active_i)
            by = away_y if dd.active_is_top_half else home_y
            border_rect = pygame.Rect(bx, by, inning_col_w, row_h)
            pygame.draw.rect(
                surface,
                dc.COLOR_SCOREBOARD_ACTIVE_BORDER,
                border_rect,
                dc.SCOREBOARD_ACTIVE_BORDER_W,
            )

        pygame.draw.line(
            surface,
            dc.SCOREBOARD_COLOR_DIVIDER,
            (x_rhe(0), y_offset),
            (x_rhe(0), dc.SCOREBOARD_SCREEN_H),
        )
        for y in (header_y, away_y, home_y):
            pygame.draw.line(
                surface,
                dc.SCOREBOARD_COLOR_DIVIDER,
                (0, y),
                (dc.SCOREBOARD_SCREEN_W, y),
            )
