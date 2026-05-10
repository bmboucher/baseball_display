from __future__ import annotations

import time
from typing import Any, cast

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import Component, make_font
from baseball_display.constants import STAT_DISPLAY_NAMES
from baseball_display.state import get_state
from baseball_display.statsapi import (
    get_player_stats,
    get_player_stats_by_year,
    get_teams,
)


def _sorted_stats(raw: dict[str, Any]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for key, val in raw.items():
        display = STAT_DISPLAY_NAMES.get(key, key)
        if val is None:
            val_str = dc.PLAYER_STATS_PANEL_EMPTY_VALUE_TEXT
        elif isinstance(val, float):
            val_str = f"{val:.3f}"
        else:
            val_str = str(val)
        rows.append((display, val_str))
    rows.sort(key=lambda row: row[0].lower())
    return rows


def _extract_stat(entry: dict[str, Any]) -> dict[str, Any]:
    inner = entry.get("stat")
    if isinstance(inner, dict):
        return cast(dict[str, Any], inner)
    return entry


def _get_available_years(player_mlb_id: int) -> tuple[list[str], dict[str, str]]:
    hitting = get_player_stats_by_year(player_mlb_id, "hitting") or {}
    pitching = get_player_stats_by_year(player_mlb_id, "pitching") or {}
    years = sorted(set(hitting) | set(pitching), reverse=True)
    teams_by_id = {team.id: team.abbreviation for team in get_teams()}
    year_teams: dict[str, str] = {}
    for yr in years:
        entry = hitting.get(yr) or pitching.get(yr)
        if entry is None:
            continue
        team_id = entry.get("team_id")
        if team_id is not None:
            abbr = teams_by_id.get(team_id)
            if abbr:
                year_teams[yr] = abbr
    return years, year_teams


def _combined_stats(
    player_mlb_id: int,
    stat_type: str,
    season: str | None = None,
) -> list[tuple[str, str]]:
    if stat_type == "yearByYear" and season is not None:
        hitting_map = get_player_stats_by_year(player_mlb_id, "hitting") or {}
        pitching_map = get_player_stats_by_year(player_mlb_id, "pitching") or {}
        hitting: dict[str, Any] = _extract_stat(hitting_map.get(season, {}))
        pitching: dict[str, Any] = _extract_stat(pitching_map.get(season, {}))
    else:
        hitting = get_player_stats(player_mlb_id, stat_type, "hitting") or {}
        pitching = get_player_stats(player_mlb_id, stat_type, "pitching") or {}
    merged: dict[str, Any] = {**pitching, **hitting}
    return _sorted_stats(merged)


class PlayerStatsPanel(Component):
    _last_browse_player_id: int | None = None
    _player_changed_at: float = 0.0

    def draw(self, surface: Surface) -> None:
        surface.fill(dc.PLAYER_STATS_PANEL_COLOR_BG)
        player_state = get_state().players

        if player_state.sub_mode == "stats" and player_state.stats is not None:
            stats_state = player_state.stats
            if not stats_state.available_years:
                years, year_teams = _get_available_years(stats_state.player_mlb_id)
                stats_state.available_years = years
                stats_state.available_year_teams = year_teams
            _label, stat_type, season = stats_state.current_tab()
            self._render_stats(
                surface,
                stats_state.player_mlb_id,
                stat_type,
                season,
                stats_state.scroll_offset,
            )
        else:
            player = player_state.browse.current_player()
            if player is None:
                msg = make_font(dc.PLAYER_STATS_PANEL_MENU_FONT_SIZE).render(
                    dc.PLAYER_STATS_PANEL_NO_PLAYER_TEXT,
                    True,
                    dc.PLAYER_STATS_PANEL_COLOR_SCOREBOARD_DIMMED,
                )
                surface.blit(
                    msg,
                    msg.get_rect(
                        center=(
                            dc.PLAYER_STATS_PANEL_SCREEN_W // 2,
                            dc.PLAYER_STATS_PANEL_SCREEN_H // 2,
                        )
                    ),
                )
                return
            if player.mlb_id != self._last_browse_player_id:
                self._last_browse_player_id = player.mlb_id
                self._player_changed_at = time.monotonic()
            if (
                time.monotonic() - self._player_changed_at
                < dc.PLAYER_STATS_PANEL_BROWSE_COOLOFF
            ):
                msg = make_font(dc.PLAYER_STATS_PANEL_MENU_FONT_SIZE).render(
                    dc.PLAYER_STATS_PANEL_LOADING_TEXT,
                    True,
                    dc.PLAYER_STATS_PANEL_COLOR_SCOREBOARD_DIMMED,
                )
                surface.blit(
                    msg,
                    msg.get_rect(
                        center=(
                            dc.PLAYER_STATS_PANEL_SCREEN_W // 2,
                            dc.PLAYER_STATS_PANEL_SCREEN_H // 2,
                        )
                    ),
                )
                return
            rows = _combined_stats(player.mlb_id, "career")
            total_px = len(rows) * dc.PLAYER_STATS_PANEL_ROW_H
            scroll_px = int(time.monotonic() * dc.PLAYER_STATS_PANEL_SCROLL_PX_PER_SEC)
            scroll_px %= max(total_px, 1)
            self._draw_rows_continuous(surface, rows, scroll_px)

    def _render_stats(
        self,
        surf: Surface,
        player_mlb_id: int,
        stat_type: str,
        season: str | None,
        scroll_offset: int,
    ) -> None:
        rows = _combined_stats(player_mlb_id, stat_type, season)
        if not rows:
            msg = make_font(dc.PLAYER_STATS_PANEL_MENU_FONT_SIZE).render(
                dc.PLAYER_STATS_PANEL_NO_DATA_TEXT,
                True,
                dc.PLAYER_STATS_PANEL_COLOR_SCOREBOARD_DIMMED,
            )
            surf.blit(
                msg,
                (dc.PLAYER_STATS_PANEL_EDGE_PAD, dc.PLAYER_STATS_PANEL_EDGE_PAD),
            )
            return
        offset = scroll_offset % len(rows)
        self._draw_rows(surf, rows, offset)

    def _draw_rows(
        self,
        surf: Surface,
        rows: list[tuple[str, str]],
        scroll_offset: int,
    ) -> None:
        if not rows:
            return
        label_font = make_font(
            dc.PLAYER_STATS_PANEL_ROW_H - dc.PLAYER_STATS_PANEL_ROW_PAD * 2
        )
        total = len(rows)
        for i in range(dc.PLAYER_STATS_PANEL_ROWS_VISIBLE):
            idx = (scroll_offset + i) % total
            display_name, val_str = rows[idx]
            row_y = i * dc.PLAYER_STATS_PANEL_ROW_H
            bg = (
                dc.PLAYER_STATS_PANEL_COLOR_ROW_EVEN
                if idx % 2 == 0
                else dc.PLAYER_STATS_PANEL_COLOR_ROW_ODD
            )
            pygame.draw.rect(
                surf,
                bg,
                pygame.Rect(
                    0,
                    row_y,
                    dc.PLAYER_STATS_PANEL_SCREEN_W,
                    dc.PLAYER_STATS_PANEL_ROW_H,
                ),
            )
            name_surf = label_font.render(
                display_name,
                True,
                dc.PLAYER_STATS_PANEL_COLOR_SCOREBOARD_DIMMED,
            )
            surf.blit(
                name_surf,
                (
                    dc.PLAYER_STATS_PANEL_EDGE_PAD,
                    row_y + dc.PLAYER_STATS_PANEL_ROW_PAD,
                ),
            )
            val_surf = label_font.render(val_str, True, dc.PLAYER_STATS_PANEL_COLOR_TEXT)
            surf.blit(
                val_surf,
                (
                    dc.PLAYER_STATS_PANEL_SCREEN_W
                    - val_surf.get_width()
                    - dc.PLAYER_STATS_PANEL_EDGE_PAD,
                    row_y + dc.PLAYER_STATS_PANEL_ROW_PAD,
                ),
            )

    def _draw_rows_continuous(
        self,
        surf: Surface,
        rows: list[tuple[str, str]],
        scroll_px: int,
    ) -> None:
        if not rows:
            return

        label_font = make_font(
            dc.PLAYER_STATS_PANEL_ROW_H - dc.PLAYER_STATS_PANEL_ROW_PAD * 2
        )
        total = len(rows)
        first_row = (scroll_px // dc.PLAYER_STATS_PANEL_ROW_H) % total
        pixel_offset = scroll_px % dc.PLAYER_STATS_PANEL_ROW_H

        y = -pixel_offset
        i = 0
        while y < dc.PLAYER_STATS_PANEL_SCREEN_H:
            idx = (first_row + i) % total
            display_name, val_str = rows[idx]
            bg = (
                dc.PLAYER_STATS_PANEL_COLOR_ROW_EVEN
                if idx % 2 == 0
                else dc.PLAYER_STATS_PANEL_COLOR_ROW_ODD
            )
            pygame.draw.rect(
                surf,
                bg,
                pygame.Rect(
                    0,
                    y,
                    dc.PLAYER_STATS_PANEL_SCREEN_W,
                    dc.PLAYER_STATS_PANEL_ROW_H,
                ),
            )
            name_surf = label_font.render(
                display_name,
                True,
                dc.PLAYER_STATS_PANEL_COLOR_SCOREBOARD_DIMMED,
            )
            surf.blit(
                name_surf,
                (dc.PLAYER_STATS_PANEL_EDGE_PAD, y + dc.PLAYER_STATS_PANEL_ROW_PAD),
            )
            val_surf = label_font.render(val_str, True, dc.PLAYER_STATS_PANEL_COLOR_TEXT)
            surf.blit(
                val_surf,
                (
                    dc.PLAYER_STATS_PANEL_SCREEN_W
                    - val_surf.get_width()
                    - dc.PLAYER_STATS_PANEL_EDGE_PAD,
                    y + dc.PLAYER_STATS_PANEL_ROW_PAD,
                ),
            )
            y += dc.PLAYER_STATS_PANEL_ROW_H
            i += 1
