from __future__ import annotations

import pygame

import baseball_display.display_constants as dc
from baseball_display import logos, player_photos
from baseball_display.components.base import Component, make_font
from baseball_display.state import get_state
from baseball_display.statsapi import get_roster, get_teams


def _row_bg(index: int, is_selected: bool) -> tuple[int, int, int]:
    if is_selected:
        return dc.PLAYER_SELECT_COLOR_ROW_HOVER
    return (
        dc.PLAYER_SELECT_COLOR_ROW_EVEN
        if index % 2 == 0
        else dc.PLAYER_SELECT_COLOR_ROW_ODD
    )


def _draw_number_badge(
    surf: pygame.Surface,
    number: str,
    font: pygame.font.Font,
    x: int,
    y: int,
    row_h: int,
    pad_x: int = dc.PLAYER_SELECT_NUMBER_BADGE_PAD_X,
) -> int:
    num_surf = font.render(number.zfill(2), True, dc.PLAYER_SELECT_NUMBER_BADGE_FG)
    badge_w = num_surf.get_width() + pad_x * 2
    bx = x
    badge_rect = pygame.Rect(
        bx,
        y + (row_h - font.get_height()) // 2,
        badge_w,
        font.get_height(),
    )
    pygame.draw.rect(
        surf,
        dc.PLAYER_SELECT_NUMBER_BADGE_BG,
        badge_rect,
        border_radius=dc.PLAYER_SELECT_BADGE_BORDER_RADIUS,
    )
    surf.blit(num_surf, (bx + pad_x, badge_rect.y))
    return bx + badge_w + dc.PLAYER_SELECT_NUMBER_BADGE_GAP


class PlayerSelect(Component):
    def draw(self, surface: pygame.Surface) -> None:
        player_state = get_state().players
        surface.fill(dc.PLAYER_SELECT_COLOR_BG)

        if player_state.sub_mode == "stats" and player_state.stats is not None:
            self._draw_stats_mode(surface, player_state)
        else:
            self._draw_browse_mode(surface, player_state)

        pygame.draw.line(
            surface,
            dc.PLAYER_SELECT_COLOR_DIVIDER,
            (dc.PLAYER_SELECT_PANEL_W, 0),
            (dc.PLAYER_SELECT_PANEL_W, dc.PLAYER_SELECT_SCREEN_H),
        )

    def _draw_browse_mode(self, surf: pygame.Surface, state: object) -> None:  # type: ignore[override]
        from baseball_display.state import PlayersState

        assert isinstance(state, PlayersState)
        browse = state.browse

        teams = get_teams()
        sel_team = browse.selected_team_index
        small_font = make_font(dc.PLAYER_SELECT_MENU_FONT_SIZE - 2)

        half = dc.PLAYER_SELECT_ROWS_VISIBLE // 2
        n_teams = len(teams)
        start = (sel_team - half) % n_teams if n_teams else 0

        for i in range(min(dc.PLAYER_SELECT_ROWS_VISIBLE, n_teams)):
            idx = (start + i) % n_teams
            team = teams[idx]
            row_y = i * dc.PLAYER_SELECT_ROW_H
            is_selected = idx == sel_team
            pygame.draw.rect(
                surf,
                _row_bg(i, is_selected),
                pygame.Rect(
                    0,
                    row_y,
                    dc.PLAYER_SELECT_PANEL_W,
                    dc.PLAYER_SELECT_ROW_H,
                ),
            )

            lx = dc.PLAYER_SELECT_EDGE_PAD
            logo = logos.get_logo(
                team.id,
                dc.PLAYER_SELECT_LOGO_SMALL,
                dc.PLAYER_SELECT_LOGO_SMALL,
            )
            if logo:
                surf.blit(
                    logo,
                    (
                        lx,
                        row_y
                        + (dc.PLAYER_SELECT_ROW_H - dc.PLAYER_SELECT_LOGO_SMALL) // 2,
                    ),
                )
                lx += dc.PLAYER_SELECT_LOGO_SMALL + dc.PLAYER_SELECT_EDGE_PAD

            name_surf = small_font.render(team.name, True, dc.PLAYER_SELECT_COLOR_TEXT)
            max_w = dc.PLAYER_SELECT_PANEL_W - lx - dc.PLAYER_SELECT_EDGE_PAD
            if name_surf.get_width() > max_w:
                name = team.name
                while (
                    len(name) > 1
                    and small_font.size(name + dc.PLAYER_SELECT_ELLIPSIS)[0] > max_w
                ):
                    name = name[:-1]
                name_surf = small_font.render(
                    name + dc.PLAYER_SELECT_ELLIPSIS,
                    True,
                    dc.PLAYER_SELECT_COLOR_TEXT,
                )
            surf.blit(
                name_surf,
                (
                    lx,
                    row_y + (dc.PLAYER_SELECT_ROW_H - name_surf.get_height()) // 2,
                ),
            )

        current_team = browse.current_team()
        if current_team is None:
            return

        roster = get_roster(current_team.id)
        if not roster:
            loading = small_font.render(
                dc.PLAYER_SELECT_LOADING_TEXT,
                True,
                dc.PLAYER_SELECT_COLOR_SCOREBOARD_DIMMED,
            )
            surf.blit(
                loading,
                (
                    dc.PLAYER_SELECT_PANEL_W + dc.PLAYER_SELECT_SECTION_PAD,
                    dc.PLAYER_SELECT_SECTION_PAD + 2,
                ),
            )
            return

        sel_player = browse.selected_player_index
        n_roster = len(roster)
        start = (sel_player - half) % n_roster if n_roster else 0

        for i in range(min(dc.PLAYER_SELECT_ROWS_VISIBLE, n_roster)):
            idx = (start + i) % n_roster
            player = roster[idx]
            row_y = i * dc.PLAYER_SELECT_ROW_H
            is_selected = idx == sel_player
            pygame.draw.rect(
                surf,
                _row_bg(i, is_selected),
                pygame.Rect(
                    dc.PLAYER_SELECT_PANEL_W,
                    row_y,
                    dc.PLAYER_SELECT_PANEL_W,
                    dc.PLAYER_SELECT_ROW_H,
                ),
            )

            x = dc.PLAYER_SELECT_PANEL_W + dc.PLAYER_SELECT_EDGE_PAD
            if player.jersey_number:
                x = _draw_number_badge(
                    surf,
                    player.jersey_number,
                    small_font,
                    x,
                    row_y,
                    dc.PLAYER_SELECT_ROW_H,
                )

            pos_surf = small_font.render(
                player.position,
                True,
                dc.PLAYER_SELECT_COLOR_SCOREBOARD_DIMMED,
            )
            pos_x = (
                dc.PLAYER_SELECT_SCREEN_W
                - pos_surf.get_width()
                - dc.PLAYER_SELECT_EDGE_PAD
            )

            name = player.full_name
            max_w = pos_x - x - dc.PLAYER_SELECT_EDGE_PAD
            name_surf = small_font.render(name, True, dc.PLAYER_SELECT_COLOR_TEXT)
            if name_surf.get_width() > max_w:
                while (
                    len(name) > 1
                    and small_font.size(name + dc.PLAYER_SELECT_ELLIPSIS)[0] > max_w
                ):
                    name = name[:-1]
                name_surf = small_font.render(
                    name + dc.PLAYER_SELECT_ELLIPSIS,
                    True,
                    dc.PLAYER_SELECT_COLOR_TEXT,
                )
            surf.blit(
                name_surf,
                (
                    x,
                    row_y + (dc.PLAYER_SELECT_ROW_H - name_surf.get_height()) // 2,
                ),
            )
            surf.blit(
                pos_surf,
                (
                    pos_x,
                    row_y + (dc.PLAYER_SELECT_ROW_H - pos_surf.get_height()) // 2,
                ),
            )

    def _draw_stats_mode(self, surf: pygame.Surface, state: object) -> None:  # type: ignore[override]
        from baseball_display.state import PlayersState

        assert isinstance(state, PlayersState)
        assert state.stats is not None
        stats_state = state.stats

        team_id: int | None = None
        for team in get_teams():
            if team.abbreviation == stats_state.player_team_abbr:
                team_id = team.id
                break

        logo = (
            logos.get_logo(
                team_id,
                dc.PLAYER_SELECT_LOGO_CARD,
                dc.PLAYER_SELECT_LOGO_CARD,
            )
            if team_id
            else None
        )
        name_font = make_font(dc.PLAYER_SELECT_MENU_FONT_SIZE, bold=True)
        small_font = make_font(dc.PLAYER_SELECT_MENU_FONT_SIZE - 4)

        ly = dc.PLAYER_SELECT_SECTION_PAD + 2
        if logo:
            surf.blit(
                logo,
                (
                    (dc.PLAYER_SELECT_PANEL_W - dc.PLAYER_SELECT_LOGO_CARD) // 2,
                    ly,
                ),
            )
            ly += dc.PLAYER_SELECT_LOGO_CARD + dc.PLAYER_SELECT_SECTION_PAD

        name_surf = name_font.render(
            stats_state.player_name.upper(),
            True,
            dc.PLAYER_SELECT_COLOR_TEXT,
        )
        surf.blit(
            name_surf,
            (
                max(
                    dc.PLAYER_SELECT_EDGE_PAD,
                    (dc.PLAYER_SELECT_PANEL_W - name_surf.get_width()) // 2,
                ),
                ly,
            ),
        )
        ly += name_surf.get_height() + dc.PLAYER_SELECT_SECTION_PAD

        meta = (
            f"#{stats_state.player_number}  {stats_state.player_position}  "
            f"{stats_state.player_team_abbr}"
        )
        meta_surf = small_font.render(
            meta,
            True,
            dc.PLAYER_SELECT_COLOR_SCOREBOARD_DIMMED,
        )
        surf.blit(
            meta_surf,
            (
                max(
                    dc.PLAYER_SELECT_EDGE_PAD,
                    (dc.PLAYER_SELECT_PANEL_W - meta_surf.get_width()) // 2,
                ),
                ly,
            ),
        )
        ly += meta_surf.get_height()

        avail_w = dc.PLAYER_SELECT_PANEL_W - dc.PLAYER_SELECT_PHOTO_MARGIN
        avail_h = dc.PLAYER_SELECT_SCREEN_H - ly - dc.PLAYER_SELECT_PHOTO_MARGIN
        if avail_w > 0 and avail_h > 0:
            photo = player_photos.get_player_photo(
                stats_state.player_mlb_id,
                avail_w,
                avail_h,
            )
            if photo:
                pw, ph = photo.get_size()
                surf.blit(
                    photo,
                    (
                        (dc.PLAYER_SELECT_PANEL_W - pw) // 2,
                        dc.PLAYER_SELECT_SCREEN_H - ph - dc.PLAYER_SELECT_PHOTO_BOTTOM_PAD,
                    ),
                )

        tab_font = make_font(dc.PLAYER_SELECT_MENU_FONT_SIZE - 2)
        tabs = stats_state.tab_list()
        n_tabs = len(tabs)
        rows_visible = dc.PLAYER_SELECT_SCREEN_H // dc.PLAYER_SELECT_ROW_H
        half = rows_visible // 2
        start = max(0, stats_state.selected_tab_index - half)
        start = min(start, max(0, n_tabs - rows_visible))

        for i in range(rows_visible):
            idx = start + i
            if idx >= n_tabs:
                break
            label, _stat_type, season = tabs[idx]
            row_y = i * dc.PLAYER_SELECT_ROW_H
            is_selected = idx == stats_state.selected_tab_index
            pygame.draw.rect(
                surf,
                _row_bg(i, is_selected),
                pygame.Rect(
                    dc.PLAYER_SELECT_PANEL_W,
                    row_y,
                    dc.PLAYER_SELECT_PANEL_W,
                    dc.PLAYER_SELECT_ROW_H,
                ),
            )
            text = tab_font.render(label, True, dc.PLAYER_SELECT_COLOR_TEXT)
            surf.blit(
                text,
                (
                    dc.PLAYER_SELECT_PANEL_W + dc.PLAYER_SELECT_RIGHT_PANEL_TEXT_PAD,
                    row_y + (dc.PLAYER_SELECT_ROW_H - text.get_height()) // 2,
                ),
            )
            if season is not None:
                abbr = stats_state.available_year_teams.get(season, "")
                if abbr:
                    abbr_surf = tab_font.render(
                        abbr,
                        True,
                        dc.PLAYER_SELECT_COLOR_SCOREBOARD_DIMMED,
                    )
                    surf.blit(
                        abbr_surf,
                        (
                            dc.PLAYER_SELECT_SCREEN_W
                            - abbr_surf.get_width()
                            - dc.PLAYER_SELECT_RIGHT_PANEL_TEXT_PAD,
                            row_y
                            + (dc.PLAYER_SELECT_ROW_H - abbr_surf.get_height()) // 2,
                        ),
                    )
