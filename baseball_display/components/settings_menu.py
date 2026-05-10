from __future__ import annotations

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.components.base import Component, make_font
from baseball_display.settings import get_settings


def _row_bg(index: int, is_selected: bool) -> tuple[int, int, int]:
    if is_selected:
        return dc.SETTINGS_MENU_COLOR_ROW_HOVER
    return (
        dc.SETTINGS_MENU_COLOR_ROW_EVEN
        if index % 2 == 0
        else dc.SETTINGS_MENU_COLOR_ROW_ODD
    )


class SettingsMenu(Component):
    def draw(self, surface: pygame.Surface) -> None:
        _state = state.get_state().settings_menu
        surface.fill(dc.SETTINGS_MENU_COLOR_BG)

        header_rect = pygame.Rect(
            0,
            0,
            dc.SETTINGS_MENU_SCREEN_W,
            dc.SETTINGS_MENU_MENU_TAB_HEIGHT,
        )
        pygame.draw.rect(surface, dc.SETTINGS_MENU_COLOR_TAB_ACTIVE, header_rect)
        header_surf = make_font(dc.SETTINGS_MENU_MENU_FONT_SIZE).render(
            dc.SETTINGS_MENU_HEADER_TEXT,
            True,
            dc.SETTINGS_MENU_COLOR_TEXT,
        )
        hx = (dc.SETTINGS_MENU_SCREEN_W - header_surf.get_width()) // 2
        hy = (
            dc.SETTINGS_MENU_MENU_TAB_HEIGHT - header_surf.get_height()
        ) // 2
        surface.blit(header_surf, (hx, hy))

        font = make_font(dc.SETTINGS_MENU_MENU_FONT_SIZE)

        for i, label in enumerate(dc.SETTINGS_MENU_ROWS):
            row_y = dc.SETTINGS_MENU_MENU_TAB_HEIGHT + i * dc.SETTINGS_MENU_MENU_ROW_HEIGHT
            row_rect = pygame.Rect(
                0,
                row_y,
                dc.SETTINGS_MENU_SCREEN_W,
                dc.SETTINGS_MENU_MENU_ROW_HEIGHT,
            )
            is_selected = i == _state.selected_row
            pygame.draw.rect(surface, _row_bg(i, is_selected), row_rect)

            text_y = row_y + (
                dc.SETTINGS_MENU_MENU_ROW_HEIGHT - font.get_height()
            ) // 2

            name_surf = font.render(label, True, dc.SETTINGS_MENU_COLOR_TEXT)
            surface.blit(name_surf, (dc.SETTINGS_MENU_TEXT_PAD_X, text_y))

            if is_selected and _state.editing:
                val = dc.SETTINGS_MENU_REFRESH_RATE_OPTIONS[_state.pending_option_index]
                value_str = (
                    f"{dc.SETTINGS_MENU_LEFT_ARROW} {val}{dc.SETTINGS_MENU_SECONDS_SUFFIX} {dc.SETTINGS_MENU_RIGHT_ARROW}"
                )
            else:
                val = get_settings().refresh_rate
                value_str = f"{val}{dc.SETTINGS_MENU_SECONDS_SUFFIX}"

            val_surf = font.render(value_str, True, dc.SETTINGS_MENU_COLOR_TEXT)
            val_x = (
                dc.SETTINGS_MENU_SCREEN_W
                - val_surf.get_width()
                - dc.SETTINGS_MENU_TEXT_PAD_X
            )
            surface.blit(val_surf, (val_x, text_y))
