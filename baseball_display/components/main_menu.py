from __future__ import annotations

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.components.base import Component, make_font


def _row_bg(index: int, is_selected: bool) -> tuple[int, int, int]:
    if is_selected:
        return dc.MAIN_MENU_COLOR_ROW_HOVER
    return (
        dc.MAIN_MENU_COLOR_ROW_EVEN
        if index % 2 == 0
        else dc.MAIN_MENU_COLOR_ROW_ODD
    )


class MainMenu(Component):
    def draw(self, surface: pygame.Surface) -> None:
        selected = state.get_state().main_menu.selected_row
        surface.fill(dc.MAIN_MENU_COLOR_BG)

        for i, label in enumerate(dc.MAIN_MENU_ITEMS_LIST):
            row_rect = pygame.Rect(
                0,
                i * dc.MAIN_MENU_MENU_ROW_HEIGHT,
                dc.MAIN_MENU_SCREEN_W,
                dc.MAIN_MENU_MENU_ROW_HEIGHT,
            )
            pygame.draw.rect(surface, _row_bg(i, i == selected), row_rect)

            text_surf = make_font(dc.MAIN_MENU_MENU_FONT_SIZE).render(
                label,
                True,
                dc.MAIN_MENU_COLOR_TEXT,
            )
            text_y = (
                row_rect.y
                + (dc.MAIN_MENU_MENU_ROW_HEIGHT - text_surf.get_height()) // 2
            )
            surface.blit(text_surf, (dc.MAIN_MENU_TEXT_PAD_X, text_y))
