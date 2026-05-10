from abc import ABC, abstractmethod
from typing import Any, Generator, Optional

import pygame
from pygame import Surface

import baseball_display.display_constants as dc
from baseball_display.state import DisplayMode, get_state

_UNSET: object = object()

_font_cache: dict[tuple[int, bool], pygame.font.Font] = {}


def make_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Return a cached monospace SysFont at the given size and weight."""
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("monospace", size, bold=bold)
    return _font_cache[key]


class Component(ABC):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        raise NotImplementedError

    def load(self):
        pass


class ValueComponent(Component):
    """Component that caches its rendered surface and only redraws when the value changes."""

    def __init__(self, rect: pygame.Rect) -> None:
        self._rect = rect
        self._last_value: Any = _UNSET
        self._cached: Optional[Surface] = None

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def render_value(self, value: Any) -> Surface:
        raise NotImplementedError

    def draw(self, surface: Surface) -> None:
        val = self.get_value()
        if val != self._last_value:
            self._last_value = val
            self._cached = self.render_value(val)
        if self._cached is not None:
            surface.blit(self._cached, self._rect)


class ScreenBuffer(ABC):
    def __init__(self, x: int, y: int) -> None:
        self._surface = Surface(
            (dc.BASE_COMPONENT_SCREEN_W, dc.BASE_COMPONENT_SCREEN_H)
        )
        self._offset = (x, y)
        self._active_components: list[Component] = []
        self._prev_mode: DisplayMode | None = None

    @abstractmethod
    def get_active_components(
        self, mode: DisplayMode
    ) -> Generator[Component, None, None]:
        raise NotImplementedError

    def draw(self, screen: Surface):
        mode = get_state().mode
        if mode != self._prev_mode:
            self._surface.fill(dc.BASE_COMPONENT_COLOR_BG)
        for component in self.get_active_components(mode):
            if mode != self._prev_mode:
                component.load()
            component.draw(self._surface)
        self._prev_mode = mode
        screen.blit(self._surface, self._offset)
