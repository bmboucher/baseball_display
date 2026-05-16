from __future__ import annotations

import pygame

import baseball_display.display_constants as dc
from baseball_display import state, wifi as wifi_mod
from baseball_display.components.base import Component, make_font


def _status_color(kind: str) -> tuple[int, int, int]:
    if kind == "success":
        return dc.WIFI_STATUS_SUCCESS_COLOR
    if kind == "error":
        return dc.WIFI_STATUS_ERROR_COLOR
    return dc.WIFI_STATUS_PENDING_COLOR


def _row_bg(index: int, is_selected: bool) -> tuple[int, int, int]:
    if is_selected:
        return dc.SETTINGS_MENU_COLOR_ROW_HOVER
    return (
        dc.SETTINGS_MENU_COLOR_ROW_EVEN
        if index % 2 == 0
        else dc.SETTINGS_MENU_COLOR_ROW_ODD
    )


def _draw_header(surface: pygame.Surface, text: str) -> None:
    rect = pygame.Rect(0, 0, dc.SETTINGS_MENU_SCREEN_W, dc.SETTINGS_MENU_MENU_TAB_HEIGHT)
    pygame.draw.rect(surface, dc.SETTINGS_MENU_COLOR_TAB_ACTIVE, rect)
    surf = make_font(dc.SETTINGS_MENU_MENU_FONT_SIZE).render(
        text, True, dc.SETTINGS_MENU_COLOR_TEXT
    )
    x = (dc.SETTINGS_MENU_SCREEN_W - surf.get_width()) // 2
    y = (dc.SETTINGS_MENU_MENU_TAB_HEIGHT - surf.get_height()) // 2
    surface.blit(surf, (x, y))


def _signal_bars(signal_pct: int, width_chars: int = 4) -> str:
    filled = max(0, min(width_chars, round(signal_pct / 100 * width_chars)))
    return (
        dc.WIFI_SCAN_SIGNAL_FULL_CHAR * filled
        + dc.WIFI_SCAN_SIGNAL_EMPTY_CHAR * (width_chars - filled)
    )


def _security_label(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw or raw == "--":
        return dc.WIFI_SCAN_OPEN_TEXT
    # nmcli reports e.g. "WPA2 802.1X" — keep the first token.
    return raw.split()[0]


class SettingsMenuWiFi(Component):
    def draw(self, surface: pygame.Surface) -> None:
        wifi_state = state.get_state().settings_menu.wifi
        surface.fill(dc.SETTINGS_MENU_COLOR_BG)

        if not wifi_mod.is_available():
            self._draw_unavailable(surface)
            return

        if wifi_state.editor_kind == "scan" and wifi_state.scan is not None:
            self._draw_scan(surface, wifi_state.scan)
        elif wifi_state.editor_kind == "keyboard" and wifi_state.keyboard is not None:
            self._draw_keyboard(surface, wifi_state.keyboard)
        else:
            self._draw_summary(surface, wifi_state)

    # ------------------------------------------------------------------
    # Summary view: SSID / Password / Test Connection
    # ------------------------------------------------------------------

    def _draw_summary(self, surface: pygame.Surface, wifi_state) -> None:
        _draw_header(surface, dc.WIFI_HEADER_TEXT)
        font = make_font(dc.SETTINGS_MENU_MENU_FONT_SIZE)

        for i, label in enumerate(dc.WIFI_ROWS):
            row_y = dc.SETTINGS_MENU_MENU_TAB_HEIGHT + i * dc.SETTINGS_MENU_MENU_ROW_HEIGHT
            row_rect = pygame.Rect(
                0, row_y, dc.SETTINGS_MENU_SCREEN_W, dc.SETTINGS_MENU_MENU_ROW_HEIGHT
            )
            is_selected = i == wifi_state.selected_row
            pygame.draw.rect(surface, _row_bg(i, is_selected), row_rect)

            text_y = row_y + (dc.SETTINGS_MENU_MENU_ROW_HEIGHT - font.get_height()) // 2
            name_surf = font.render(label, True, dc.SETTINGS_MENU_COLOR_TEXT)
            surface.blit(name_surf, (dc.SETTINGS_MENU_TEXT_PAD_X, text_y))

            if label == dc.WIFI_ROW_SSID:
                value_str = wifi_state.pending_ssid or dc.WIFI_EMPTY_VALUE_TEXT
            elif label == dc.WIFI_ROW_PASSWORD:
                value_str = (
                    dc.WIFI_PASSWORD_MASK_CHAR * len(wifi_state.pending_password)
                    if wifi_state.pending_password
                    else dc.WIFI_EMPTY_VALUE_TEXT
                )
            else:
                value_str = dc.SETTINGS_MENU_SUBMENU_GLYPH

            # Truncate long SSIDs to fit on the row.
            max_w = (
                dc.SETTINGS_MENU_SCREEN_W
                - dc.SETTINGS_MENU_TEXT_PAD_X * 2
                - name_surf.get_width()
                - 8
            )
            value_str = _truncate_to_width(value_str, font, max_w)

            val_surf = font.render(value_str, True, dc.SETTINGS_MENU_COLOR_TEXT)
            val_x = dc.SETTINGS_MENU_SCREEN_W - val_surf.get_width() - dc.SETTINGS_MENU_TEXT_PAD_X
            surface.blit(val_surf, (val_x, text_y))

        # Status line at the bottom.
        if wifi_state.test_status:
            status_font = make_font(dc.WIFI_STATUS_FONT_SIZE)
            color = _status_color(wifi_state.test_status_color)
            status_surf = status_font.render(wifi_state.test_status, True, color)
            sx = dc.WIFI_STATUS_PAD_X
            sy = dc.SCREEN_H - status_surf.get_height() - dc.WIFI_STATUS_PAD_BOTTOM
            surface.blit(status_surf, (sx, sy))

    # ------------------------------------------------------------------
    # Scan view: list of nearby SSIDs + manual-entry row
    # ------------------------------------------------------------------

    def _draw_scan(self, surface: pygame.Surface, scan) -> None:
        _draw_header(surface, dc.WIFI_SCAN_HEADER_TEXT)
        font = make_font(dc.WIFI_SCAN_FONT_SIZE)

        if scan.scanning:
            surf = font.render(dc.WIFI_SCANNING_TEXT, True, dc.SETTINGS_MENU_COLOR_TEXT)
            x = (dc.SETTINGS_MENU_SCREEN_W - surf.get_width()) // 2
            y = dc.SETTINGS_MENU_MENU_TAB_HEIGHT + (
                dc.SCREEN_H - dc.SETTINGS_MENU_MENU_TAB_HEIGHT - surf.get_height()
            ) // 2
            surface.blit(surf, (x, y))
            return

        total = scan.total_rows()
        if total == 1:  # only the [manual] row → "no networks found"
            note_font = make_font(dc.WIFI_SCAN_FONT_SIZE)
            note = note_font.render(
                dc.WIFI_NO_NETWORKS_TEXT, True, dc.COLOR_SCOREBOARD_DIMMED
            )
            surface.blit(
                note,
                (
                    (dc.SETTINGS_MENU_SCREEN_W - note.get_width()) // 2,
                    dc.SETTINGS_MENU_MENU_TAB_HEIGHT + 12,
                ),
            )

        # Scroll so selected row stays visible.
        visible = dc.WIFI_SCAN_VISIBLE_ROWS
        first = scan.scrolled
        if scan.selected_index < first:
            first = scan.selected_index
        elif scan.selected_index >= first + visible:
            first = scan.selected_index - visible + 1
        scan.scrolled = max(0, first)

        for vi in range(visible):
            ri = scan.scrolled + vi
            if ri >= total:
                break
            row_y = dc.SETTINGS_MENU_MENU_TAB_HEIGHT + vi * dc.WIFI_SCAN_ROW_HEIGHT
            row_rect = pygame.Rect(
                0, row_y, dc.SETTINGS_MENU_SCREEN_W, dc.WIFI_SCAN_ROW_HEIGHT
            )
            is_selected = ri == scan.selected_index
            pygame.draw.rect(surface, _row_bg(ri, is_selected), row_rect)

            text_y = row_y + (dc.WIFI_SCAN_ROW_HEIGHT - font.get_height()) // 2

            if ri == len(scan.networks):
                # Manual-entry row
                label_surf = font.render(
                    dc.WIFI_MANUAL_ENTRY_LABEL, True, dc.SETTINGS_MENU_COLOR_TEXT
                )
                surface.blit(label_surf, (dc.WIFI_STATUS_PAD_X, text_y))
                continue

            ssid, signal, security = scan.networks[ri]
            bars = _signal_bars(signal)
            bars_surf = font.render(bars, True, dc.SETTINGS_MENU_COLOR_TEXT)
            surface.blit(bars_surf, (dc.WIFI_STATUS_PAD_X, text_y))

            sec_label = _security_label(security)
            sec_surf = font.render(sec_label, True, dc.COLOR_SCOREBOARD_DIMMED)
            sec_x = dc.SETTINGS_MENU_SCREEN_W - sec_surf.get_width() - dc.WIFI_STATUS_PAD_X
            surface.blit(sec_surf, (sec_x, text_y))

            ssid_x = dc.WIFI_STATUS_PAD_X + dc.WIFI_SCAN_SIGNAL_W + 4
            ssid_max_w = sec_x - ssid_x - 6
            ssid_disp = _truncate_to_width(ssid, font, ssid_max_w)
            ssid_surf = font.render(ssid_disp, True, dc.SETTINGS_MENU_COLOR_TEXT)
            surface.blit(ssid_surf, (ssid_x, text_y))

    # ------------------------------------------------------------------
    # Keyboard view
    # ------------------------------------------------------------------

    def _draw_keyboard(self, surface: pygame.Surface, kb) -> None:
        # Field-name header.
        header_font = make_font(dc.WIFI_KB_HEADER_FONT_SIZE)
        header_text = f"{dc.WIFI_KEYBOARD_HEADER_PREFIX}{kb.field}"
        header_surf = header_font.render(header_text, True, dc.SETTINGS_MENU_COLOR_TEXT)
        surface.blit(header_surf, (dc.WIFI_STATUS_PAD_X, 4))

        # In-progress value strip.
        value_rect = pygame.Rect(
            0, dc.WIFI_KB_HEADER_H, dc.SCREEN_W, dc.WIFI_KB_VALUE_H
        )
        pygame.draw.rect(surface, dc.WIFI_KB_VALUE_BG, value_rect)
        value_font = make_font(dc.WIFI_KB_VALUE_FONT_SIZE)
        value_text = kb.value or ""
        # Show last N chars if too long, so the cursor stays visible.
        max_chars = dc.WIFI_KB_MAX_VALUE_CHARS
        display_value = value_text[-max_chars:] if len(value_text) > max_chars else value_text
        value_surf = value_font.render(display_value, True, dc.SETTINGS_MENU_COLOR_TEXT)
        vy = dc.WIFI_KB_HEADER_H + (dc.WIFI_KB_VALUE_H - value_surf.get_height()) // 2
        surface.blit(value_surf, (dc.WIFI_STATUS_PAD_X, vy))
        # Block cursor at the end of value.
        cursor_x = dc.WIFI_STATUS_PAD_X + value_surf.get_width() + 2
        cursor_rect = pygame.Rect(cursor_x, vy + 2, 2, value_surf.get_height() - 4)
        pygame.draw.rect(surface, dc.WIFI_KB_CURSOR_COLOR, cursor_rect)

        # Key grid.
        grid = kb.current_grid()
        font = make_font(dc.WIFI_KB_KEY_FONT_SIZE)
        y = dc.WIFI_KB_TOP_PAD + dc.WIFI_KB_GRID_PAD_Y

        for ri, row in enumerate(grid):
            # Center this row horizontally based on its actual width.
            widths = [_key_width(token) for token in row]
            total_w = sum(widths) + dc.WIFI_KB_KEY_GAP * (len(row) - 1)
            x0 = (dc.SCREEN_W - total_w) // 2

            x = x0
            for ci, token in enumerate(row):
                w = widths[ci]
                key_rect = pygame.Rect(x, y, w, dc.WIFI_KB_KEY_H)
                is_selected = ri == kb.row and ci == kb.col
                is_special = len(token) > 1
                bg = (
                    dc.WIFI_KB_KEY_BG_HOVER
                    if is_selected
                    else dc.WIFI_KB_KEY_BG_SPECIAL if is_special else dc.WIFI_KB_KEY_BG
                )
                pygame.draw.rect(surface, bg, key_rect, border_radius=dc.WIFI_KB_KEY_RADIUS)
                pygame.draw.rect(
                    surface,
                    dc.WIFI_KB_KEY_BORDER,
                    key_rect,
                    width=1,
                    border_radius=dc.WIFI_KB_KEY_RADIUS,
                )
                label = _key_label(token, kb.layer)
                label_surf = font.render(label, True, dc.SETTINGS_MENU_COLOR_TEXT)
                lx = x + (w - label_surf.get_width()) // 2
                ly = y + (dc.WIFI_KB_KEY_H - label_surf.get_height()) // 2
                surface.blit(label_surf, (lx, ly))
                x += w + dc.WIFI_KB_KEY_GAP
            y += dc.WIFI_KB_KEY_H + dc.WIFI_KB_KEY_GAP

    # ------------------------------------------------------------------
    # Unavailable view (Windows / no nmcli)
    # ------------------------------------------------------------------

    def _draw_unavailable(self, surface: pygame.Surface) -> None:
        _draw_header(surface, dc.WIFI_HEADER_TEXT)
        font = make_font(dc.SETTINGS_MENU_MENU_FONT_SIZE)
        surf = font.render(dc.WIFI_UNAVAILABLE_TEXT, True, dc.COLOR_SCOREBOARD_DIMMED)
        x = (dc.SCREEN_W - surf.get_width()) // 2
        y = dc.SETTINGS_MENU_MENU_TAB_HEIGHT + (
            dc.SCREEN_H - dc.SETTINGS_MENU_MENU_TAB_HEIGHT - surf.get_height()
        ) // 2
        surface.blit(surf, (x, y))


def _key_width(token: str) -> int:
    if len(token) > 1:
        return dc.WIFI_KB_SPECIAL_KEY_WIDTHS.get(token, dc.WIFI_KB_KEY_W)
    return dc.WIFI_KB_KEY_W


def _key_label(token: str, layer: str) -> str:
    if token == dc.WIFI_KB_SPECIAL_SHIFT:
        return dc.WIFI_KB_SHIFT_LABELS.get(layer, "ABC")
    if len(token) > 1:
        return dc.WIFI_KB_SPECIAL_LABELS.get(token, token)
    return token


def _truncate_to_width(text: str, font: pygame.font.Font, max_width: int) -> str:
    if max_width <= 0:
        return ""
    if font.size(text)[0] <= max_width:
        return text
    ellipsis = "…"
    while text and font.size(text + ellipsis)[0] > max_width:
        text = text[:-1]
    return text + ellipsis if text else ellipsis
