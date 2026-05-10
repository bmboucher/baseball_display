from __future__ import annotations

import time
from typing import Any

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display import logos
from baseball_display.components.base import ValueComponent, make_font
from baseball_display.state import get_game_display_data


def _draw_number_badge(
    surf: Surface,
    number: str,
    font: pygame.font.Font,
    x: int,
    y: int,
    h: int,
    bg_color: tuple[int, int, int],
    pad_x: int = dc.BATTING_ORDER_BADGE_PAD_X,
    right_x: int | None = None,
) -> int:
    """Draw a jersey-number badge.

    If right_x is given the badge is right-aligned to that x coordinate.
    Returns x after the badge (when left-aligned) or x before it (when right-aligned).
    """
    num_surf = font.render(number, True, dc.BATTING_ORDER_COLOR_NUMBER_BADGE_FG)
    badge_w = num_surf.get_width() + pad_x * 2
    bx = (right_x - badge_w) if right_x is not None else x
    badge_rect = pygame.Rect(
        bx,
        y + (h - font.get_height()) // 2,
        badge_w,
        font.get_height(),
    )
    pygame.draw.rect(surf, bg_color, badge_rect, border_radius=2)
    surf.blit(num_surf, (bx + pad_x, badge_rect.y))
    return bx + badge_w + dc.BATTING_ORDER_BADGE_GAP


def _draw_stat_grid(
    surf: Surface,
    pairs: list[tuple[str, str]],
    rx: int,
    ry: int,
    num_cols: int,
    label_font: pygame.font.Font,
    val_font: pygame.font.Font,
    col_w: int | list[int],
) -> int:
    """Draw label+value pairs in a grid. Returns y below the last row.

    col_w may be a single int (uniform) or a list of per-column widths.
    """
    col_widths: list[int] = col_w if isinstance(col_w, list) else [col_w] * num_cols
    col_x: list[int] = []
    acc = rx
    for w in col_widths:
        col_x.append(acc)
        acc += w

    label_h = label_font.get_height()
    row_h = label_h + dc.BATTING_ORDER_LABEL_VALUE_GAP + val_font.get_height()
    for i, (label, val) in enumerate(pairs):
        col = i % num_cols
        cx = col_x[col]
        cy = ry + (i // num_cols) * (row_h + dc.BATTING_ORDER_GRID_ROW_GAP)
        surf.blit(
            label_font.render(label, True, dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED),
            (cx, cy),
        )
        surf.blit(
            val_font.render(val, True, dc.BATTING_ORDER_COLOR_TEXT),
            (cx, cy + label_h + dc.BATTING_ORDER_LABEL_VALUE_GAP),
        )
    num_rows = (len(pairs) + num_cols - 1) // num_cols
    return ry + num_rows * (row_h + dc.BATTING_ORDER_GRID_ROW_GAP)


class BattingOrder(ValueComponent):
    def __init__(self) -> None:
        super().__init__(
            pygame.Rect(
                0,
                0,
                dc.BATTING_ORDER_SCREEN_W,
                dc.BATTING_ORDER_SCREEN_H,
            )
        )

    def get_value(self) -> Any:
        dd = get_game_display_data()
        epoch = int(time.monotonic() // dc.BATTING_ORDER_STATS_ALTERNATE_SECS) % 2
        return (
            tuple(dd.lineup),
            dd.batter_info,
            dd.batter_season_stats,
            dd.batter_career_stats,
            dd.pitcher_info,
            dd.pitcher_season_stats,
            dd.pitcher_career_stats,
            dd.away_team_id,
            dd.home_team_id,
            dd.batting_is_away,
            epoch,
        )

    def render_value(self, value: Any) -> Surface:
        (
            lineup_entries,
            batter_info,
            batter_season_stats,
            batter_career_stats,
            pitcher_info,
            pitcher_season_stats,
            pitcher_career_stats,
            away_team_id,
            home_team_id,
            batting_is_away,
            epoch,
        ) = value

        show_career = bool(epoch)
        indicator_label = (
            dc.BATTING_ORDER_CAREER_LABEL
            if show_career
            else dc.BATTING_ORDER_SEASON_LABEL
        )
        batter_stats = (
            (batter_career_stats if show_career else batter_season_stats)
            or batter_season_stats
            or batter_career_stats
        )
        pitcher_stats = (
            (pitcher_career_stats if show_career else pitcher_season_stats)
            or pitcher_season_stats
            or pitcher_career_stats
        )

        batter_team_id: int | None = away_team_id if batting_is_away else home_team_id
        pitcher_team_id: int | None = home_team_id if batting_is_away else away_team_id
        batting_badge_bg = (
            dc.BATTING_ORDER_COLOR_NUMBER_BADGE_AWAY_BG
            if batting_is_away
            else dc.BATTING_ORDER_COLOR_NUMBER_BADGE_HOME_BG
        )
        pitching_badge_bg = (
            dc.BATTING_ORDER_COLOR_NUMBER_BADGE_HOME_BG
            if batting_is_away
            else dc.BATTING_ORDER_COLOR_NUMBER_BADGE_AWAY_BG
        )
        surf = Surface((dc.BATTING_ORDER_SCREEN_W, dc.BATTING_ORDER_SCREEN_H))
        surf.fill(dc.BATTING_ORDER_COLOR_BG)

        pygame.draw.line(
            surf,
            dc.BATTING_ORDER_COLOR_DIVIDER,
            (dc.BATTING_ORDER_LINEUP_PANEL_W, 0),
            (dc.BATTING_ORDER_LINEUP_PANEL_W, dc.BATTING_ORDER_SCREEN_H),
        )
        pygame.draw.line(
            surf,
            dc.BATTING_ORDER_COLOR_DIVIDER,
            (dc.BATTING_ORDER_LINEUP_PANEL_W, dc.BATTING_ORDER_HALF_H),
            (dc.BATTING_ORDER_SCREEN_W, dc.BATTING_ORDER_HALF_H),
        )

        if not lineup_entries and batter_info is None:
            msg = make_font(dc.BATTING_ORDER_LINEUP_FONT_SIZE).render(
                dc.BATTING_ORDER_LOADING_TEXT,
                True,
                dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED,
            )
            surf.blit(
                msg,
                msg.get_rect(
                    center=(
                        dc.BATTING_ORDER_SCREEN_W // 2,
                        dc.BATTING_ORDER_SCREEN_H // 2,
                    )
                ),
            )
            return surf

        stats_font = make_font(dc.BATTING_ORDER_STATS_FONT_SIZE)
        rx = dc.BATTING_ORDER_LINEUP_PANEL_W + dc.BATTING_ORDER_RIGHT_PAD
        col_w4 = (
            dc.BATTING_ORDER_RIGHT_W - dc.BATTING_ORDER_RIGHT_PAD
        ) // 4

        lineup_font = make_font(dc.BATTING_ORDER_LINEUP_FONT_SIZE)
        for slot_idx, entry in enumerate(lineup_entries):
            row_y = slot_idx * dc.BATTING_ORDER_LINEUP_ROW_H
            if entry.is_active:
                pygame.draw.rect(
                    surf,
                    dc.BATTING_ORDER_COLOR_LINEUP_ACTIVE_BG,
                    pygame.Rect(
                        0,
                        row_y,
                        dc.BATTING_ORDER_LINEUP_PANEL_W,
                        dc.BATTING_ORDER_LINEUP_ROW_H,
                    ),
                )
            fg = (
                dc.BATTING_ORDER_ACTIVE_FG
                if entry.is_active
                else dc.BATTING_ORDER_COLOR_TEXT
            )
            text_x = dc.BATTING_ORDER_PANEL_TEXT_PAD
            if entry.number:
                text_x = _draw_number_badge(
                    surf,
                    entry.number.zfill(2),
                    lineup_font,
                    dc.BATTING_ORDER_PANEL_TEXT_PAD,
                    row_y,
                    dc.BATTING_ORDER_LINEUP_ROW_H,
                    batting_badge_bg,
                )
            name_surf = lineup_font.render(entry.last_name, True, fg)
            surf.blit(
                name_surf,
                (
                    text_x,
                    row_y
                    + (
                        dc.BATTING_ORDER_LINEUP_ROW_H - name_surf.get_height()
                    )
                    // 2,
                ),
            )
            if slot_idx > 0:
                pygame.draw.line(
                    surf,
                    dc.BATTING_ORDER_COLOR_DIVIDER,
                    (0, row_y),
                    (dc.BATTING_ORDER_LINEUP_PANEL_W, row_y),
                )

        batter_name_font = make_font(dc.BATTING_ORDER_BATTER_NAME_FONT_SIZE, bold=True)
        ry = dc.BATTING_ORDER_SECTION_TOP_PAD
        if batter_info is not None:
            batter_logo = (
                logos.get_logo(
                    batter_team_id,
                    dc.BATTING_ORDER_LOGO_SIZE,
                    dc.BATTING_ORDER_LOGO_SIZE,
                )
                if batter_team_id
                else None
            )
            batter_label = batter_info.display_name
            logo_tile = dc.BATTING_ORDER_LOGO_SIZE + dc.BATTING_ORDER_LOGO_WHITE_PAD * 2
            row_h = max(logo_tile, batter_name_font.get_height())
            name_x = rx
            badge_right_x = dc.BATTING_ORDER_SCREEN_W - dc.BATTING_ORDER_RIGHT_PAD
            if batter_logo:
                logo_y = ry + (row_h - logo_tile) // 2
                pygame.draw.rect(
                    surf,
                    dc.BATTING_ORDER_LOGO_TILE_BG,
                    pygame.Rect(rx, logo_y, logo_tile, logo_tile),
                )
                surf.blit(
                    batter_logo,
                    (
                        rx + dc.BATTING_ORDER_LOGO_WHITE_PAD,
                        logo_y + dc.BATTING_ORDER_LOGO_WHITE_PAD,
                    ),
                )
                name_x = rx + logo_tile + dc.BATTING_ORDER_LOGO_TEXT_GAP
            if batter_info.number:
                _draw_number_badge(
                    surf,
                    batter_info.number.zfill(2),
                    batter_name_font,
                    0,
                    ry,
                    row_h,
                    batting_badge_bg,
                    right_x=badge_right_x,
                )
                num_w = batter_name_font.size(batter_info.number.zfill(2))[0]
                badge_right_x = (
                    badge_right_x - num_w - dc.BATTING_ORDER_BADGE_TEXT_GAP
                )
            max_name_w = badge_right_x - name_x - dc.BATTING_ORDER_NAME_TRUNCATION_PAD
            name_surf = batter_name_font.render(
                batter_label,
                True,
                dc.BATTING_ORDER_COLOR_TEXT,
            )
            if name_surf.get_width() > max_name_w:
                while (
                    batter_label
                    and batter_name_font.size(
                        batter_label + dc.BATTING_ORDER_NAME_ELLIPSIS
                    )[0]
                    > max_name_w
                ):
                    batter_label = batter_label[:-1]
                name_surf = batter_name_font.render(
                    batter_label + dc.BATTING_ORDER_NAME_ELLIPSIS,
                    True,
                    dc.BATTING_ORDER_COLOR_TEXT,
                )
            surf.blit(
                name_surf,
                (name_x, ry + (row_h - name_surf.get_height()) // 2),
            )
            ry += row_h
            ry += dc.BATTING_ORDER_LOGO_TEXT_GAP
            if batter_stats is not None:
                batter_grid = [
                    ("AVG", batter_stats.avg),
                    ("HR", batter_stats.hr),
                    ("RBI", batter_stats.rbi),
                    ("R", batter_stats.r),
                    ("OBP", batter_stats.obp),
                    ("SLG", batter_stats.slg),
                    ("OPS", batter_stats.ops),
                    ("SB", batter_stats.sb),
                ]
                _draw_stat_grid(
                    surf,
                    batter_grid,
                    rx,
                    ry,
                    4,
                    stats_font,
                    stats_font,
                    col_w4,
                )
            else:
                surf.blit(
                    stats_font.render(
                        dc.BATTING_ORDER_LOADING_STATS_TEXT,
                        True,
                        dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED,
                    ),
                    (rx, ry),
                )
        else:
            surf.blit(
                stats_font.render(
                    dc.BATTING_ORDER_NO_BATTER_TEXT,
                    True,
                    dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED,
                ),
                (rx, ry),
            )

        pitcher_name_font = make_font(dc.BATTING_ORDER_BATTER_NAME_FONT_SIZE, bold=True)
        py = dc.BATTING_ORDER_HALF_H + dc.BATTING_ORDER_SECTION_TOP_PAD
        if pitcher_info is not None:
            pitcher_logo = (
                logos.get_logo(
                    pitcher_team_id,
                    dc.BATTING_ORDER_LOGO_SIZE,
                    dc.BATTING_ORDER_LOGO_SIZE,
                )
                if pitcher_team_id
                else None
            )
            pitcher_label = pitcher_info.display_name
            logo_tile = dc.BATTING_ORDER_LOGO_SIZE + dc.BATTING_ORDER_LOGO_WHITE_PAD * 2
            row_h = max(logo_tile, pitcher_name_font.get_height())
            name_x = rx
            if pitcher_logo:
                logo_y = py + (row_h - logo_tile) // 2
                pygame.draw.rect(
                    surf,
                    dc.BATTING_ORDER_LOGO_TILE_BG,
                    pygame.Rect(rx, logo_y, logo_tile, logo_tile),
                )
                surf.blit(
                    pitcher_logo,
                    (
                        rx + dc.BATTING_ORDER_LOGO_WHITE_PAD,
                        logo_y + dc.BATTING_ORDER_LOGO_WHITE_PAD,
                    ),
                )
                name_x = rx + logo_tile + dc.BATTING_ORDER_LOGO_TEXT_GAP
            badge_right_x = dc.BATTING_ORDER_SCREEN_W - dc.BATTING_ORDER_RIGHT_PAD
            if pitcher_info.number:
                _draw_number_badge(
                    surf,
                    pitcher_info.number.zfill(2),
                    pitcher_name_font,
                    0,
                    py,
                    row_h,
                    pitching_badge_bg,
                    right_x=badge_right_x,
                )
                num_w = pitcher_name_font.size(pitcher_info.number.zfill(2))[0]
                badge_right_x = (
                    badge_right_x - num_w - dc.BATTING_ORDER_BADGE_TEXT_GAP
                )
            max_name_w = badge_right_x - name_x - dc.BATTING_ORDER_NAME_TRUNCATION_PAD
            name_surf = pitcher_name_font.render(
                pitcher_label,
                True,
                dc.BATTING_ORDER_COLOR_TEXT,
            )
            if name_surf.get_width() > max_name_w:
                while (
                    pitcher_label
                    and pitcher_name_font.size(
                        pitcher_label + dc.BATTING_ORDER_NAME_ELLIPSIS
                    )[0]
                    > max_name_w
                ):
                    pitcher_label = pitcher_label[:-1]
                name_surf = pitcher_name_font.render(
                    pitcher_label + dc.BATTING_ORDER_NAME_ELLIPSIS,
                    True,
                    dc.BATTING_ORDER_COLOR_TEXT,
                )
            surf.blit(
                name_surf,
                (name_x, py + (row_h - name_surf.get_height()) // 2),
            )
            py += row_h
            py += dc.BATTING_ORDER_LOGO_TEXT_GAP
            if pitcher_stats is not None:
                pcol_w4 = (
                    dc.BATTING_ORDER_RIGHT_W - dc.BATTING_ORDER_RIGHT_PAD
                ) // 4
                narrow_w = (
                    dc.BATTING_ORDER_RIGHT_W
                    - dc.BATTING_ORDER_RIGHT_PAD
                    - dc.BATTING_ORDER_PC_ST_W
                ) // 4
                pitch_row1 = [
                    ("IP", pitcher_stats.ip),
                    ("H", pitcher_stats.h),
                    ("R", pitcher_stats.r),
                    ("ER", pitcher_stats.er),
                ]
                pitch_row2 = [
                    ("BB", pitcher_stats.bb),
                    ("K", pitcher_stats.so),
                    ("HR", pitcher_stats.hr),
                    ("PC-ST", pitcher_stats.pc_st),
                    ("ERA", pitcher_stats.era),
                ]
                py = _draw_stat_grid(
                    surf,
                    pitch_row1,
                    rx,
                    py,
                    4,
                    stats_font,
                    stats_font,
                    pcol_w4,
                )
                _draw_stat_grid(
                    surf,
                    pitch_row2,
                    rx,
                    py,
                    5,
                    stats_font,
                    stats_font,
                    [
                        narrow_w,
                        narrow_w,
                        narrow_w,
                        dc.BATTING_ORDER_PC_ST_W,
                        narrow_w,
                    ],
                )
            else:
                surf.blit(
                    stats_font.render(
                        dc.BATTING_ORDER_LOADING_STATS_TEXT,
                        True,
                        dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED,
                    ),
                    (rx, py),
                )
        else:
            surf.blit(
                stats_font.render(
                    dc.BATTING_ORDER_NO_PITCHER_TEXT,
                    True,
                    dc.BATTING_ORDER_COLOR_SCOREBOARD_DIMMED,
                ),
                (rx, py),
            )

        ind_font = make_font(dc.BATTING_ORDER_STATS_FONT_SIZE)
        ind_surf = ind_font.render(
            indicator_label,
            True,
            dc.BATTING_ORDER_INDICATOR_COLOR,
        )
        surf.blit(
            ind_surf,
            (
                dc.BATTING_ORDER_SCREEN_W
                - ind_surf.get_width()
                - dc.BATTING_ORDER_INDICATOR_MARGIN,
                dc.BATTING_ORDER_SCREEN_H
                - ind_surf.get_height()
                - dc.BATTING_ORDER_INDICATOR_MARGIN,
            ),
        )

        return surf
