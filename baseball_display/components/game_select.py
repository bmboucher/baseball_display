from __future__ import annotations

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.components.base import Component, make_font


class GameSelect(Component):
    def load(self):
        state.get_state().game_select.update_rows()

    def draw(self, surface: pygame.Surface) -> None:
        _state = state.get_state().game_select

        surface.fill(dc.GAME_SELECT_COLOR_BG)

        buf_w = dc.GAME_SELECT_SCREEN_W
        tab_w = buf_w // len(dc.GAME_SELECT_TABS)
        self._tab_rects = []
        for i, label in enumerate(dc.GAME_SELECT_TABS):
            rect = pygame.Rect(i * tab_w, 0, tab_w, dc.GAME_SELECT_MENU_TAB_HEIGHT)
            color = (
                dc.GAME_SELECT_COLOR_TAB_ACTIVE
                if i == _state.tab_index
                else dc.GAME_SELECT_COLOR_TAB_INACTIVE
            )
            pygame.draw.rect(surface, color, rect)
            text_surf = make_font(dc.GAME_SELECT_MENU_FONT_SIZE).render(
                label,
                True,
                dc.GAME_SELECT_COLOR_TEXT,
            )
            tx = rect.x + (tab_w - text_surf.get_width()) // 2
            ty = (
                dc.GAME_SELECT_MENU_TAB_HEIGHT - text_surf.get_height()
            ) // 2
            surface.blit(text_surf, (tx, ty))

        list_area_top = dc.GAME_SELECT_MENU_TAB_HEIGHT
        list_height = dc.GAME_SELECT_SCREEN_H - list_area_top
        max_visible = list_height // dc.GAME_SELECT_MENU_ROW_HEIGHT

        self._row_rects = []
        visible_games = _state.rows[
            _state.scroll_offset : _state.scroll_offset + max_visible
        ]
        _selected = _state.selected_row - _state.scroll_offset

        for i, game in enumerate(visible_games):
            row_y = list_area_top + i * dc.GAME_SELECT_MENU_ROW_HEIGHT
            row_rect = pygame.Rect(
                0,
                row_y,
                buf_w,
                dc.GAME_SELECT_MENU_ROW_HEIGHT,
            )
            row_color = (
                dc.GAME_SELECT_COLOR_ROW_EVEN
                if i % 2 == 0
                else dc.GAME_SELECT_COLOR_ROW_ODD
            )
            if i == _selected:
                row_color = dc.GAME_SELECT_COLOR_ROW_HOVER
            pygame.draw.rect(surface, row_color, row_rect)

            local_dt = game.game_date.astimezone()
            date_part = local_dt.strftime("%b %e")
            time_part = local_dt.strftime("%I:%M %p")
            if time_part.startswith("0"):
                time_part = " " + time_part[1:]
            if _state.tab_index == 0:
                game_label = (
                    f"{dc.GAME_SELECT_GAME_LABEL_PREFIX} {game.game_number}"
                )
                score_str: str | None = (
                    f"{game.away_score}-{game.home_score}"
                    if game.away_score is not None and game.home_score is not None
                    else None
                )
                away_bold = (
                    game.away_score is not None
                    and game.home_score is not None
                    and game.away_score > game.home_score
                )
                home_bold = (
                    game.away_score is not None
                    and game.home_score is not None
                    and game.home_score > game.away_score
                )
                font = make_font(dc.GAME_SELECT_MENU_FONT_SIZE)
                bold_font = make_font(dc.GAME_SELECT_MENU_FONT_SIZE, bold=True)
                prefix_surf = font.render(
                    f"{date_part}  ",
                    True,
                    dc.GAME_SELECT_COLOR_TEXT,
                )
                away_surf = (bold_font if away_bold else font).render(
                    game.away_team,
                    True,
                    dc.GAME_SELECT_COLOR_TEXT,
                )
                sep_surf = font.render(" @ ", True, dc.GAME_SELECT_COLOR_TEXT)
                home_surf = (bold_font if home_bold else font).render(
                    game.home_team,
                    True,
                    dc.GAME_SELECT_COLOR_TEXT,
                )
                game_surf = font.render(
                    game_label,
                    True,
                    dc.GAME_SELECT_COLOR_TEXT,
                )
                text_y = (
                    row_y
                    + (
                        dc.GAME_SELECT_MENU_ROW_HEIGHT - prefix_surf.get_height()
                    )
                    // 2
                )
                x = dc.GAME_SELECT_TEXT_PAD_X
                for rendered in (prefix_surf, away_surf, sep_surf, home_surf):
                    surface.blit(rendered, (x, text_y))
                    x += rendered.get_width()
                surface.blit(
                    game_surf,
                    (
                        buf_w
                        - game_surf.get_width()
                        - dc.GAME_SELECT_RIGHT_TEXT_PAD_X,
                        text_y,
                    ),
                )
                if score_str is not None:
                    score_surf = font.render(
                        score_str,
                        True,
                        dc.GAME_SELECT_COLOR_TEXT,
                    )
                    score_x = (
                        buf_w
                        - game_surf.get_width()
                        - score_surf.get_width()
                        - dc.GAME_SELECT_SCORE_GAP_X
                        - font.size(dc.GAME_SELECT_SCORE_PAD_TEXT)[0]
                    )
                    surface.blit(score_surf, (score_x, text_y))
            else:
                label = (
                    f"{date_part}  {time_part}  {game.away_team} @ {game.home_team}"
                )
                font = make_font(dc.GAME_SELECT_MENU_FONT_SIZE)
                game_label = (
                    f"{dc.GAME_SELECT_GAME_LABEL_PREFIX} {game.game_number}"
                )
                text_surf = font.render(label, True, dc.GAME_SELECT_COLOR_TEXT)
                game_surf = font.render(
                    game_label,
                    True,
                    dc.GAME_SELECT_COLOR_TEXT,
                )
                text_y = (
                    row_y
                    + (dc.GAME_SELECT_MENU_ROW_HEIGHT - text_surf.get_height()) // 2
                )
                surface.blit(text_surf, (dc.GAME_SELECT_TEXT_PAD_X, text_y))
                surface.blit(
                    game_surf,
                    (
                        buf_w
                        - game_surf.get_width()
                        - dc.GAME_SELECT_RIGHT_TEXT_PAD_X,
                        text_y,
                    ),
                )
