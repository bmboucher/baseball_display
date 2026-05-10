from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.components.base import Component


class BlankScreen(Component):
    def draw(self, surface: Surface):
        surface.fill(dc.BLANK_SCREEN_COLOR_BG)
