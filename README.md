# baseball_display

A pygame-based MLB scoreboard display application. Renders live, finished, and upcoming MLB games across a three-panel "jumbotron" layout (1440×320 px, three 480×320 panels side by side).

## Running

```bash
python -m baseball_display
```

Or, after installing the package:

```bash
baseball-display
```

The `.venv` is at `C:\Repos\baseball_display\.venv`. The project uses Python 3.12 and pygame 2.6.

---

## Architecture Overview

### Three-Panel Layout

The window is `FULL_SCREEN_W × FULL_SCREEN_H = 1440 × 320`. Each panel is `SCREEN_W × SCREEN_H = 480 × 320`:

| Panel | Position | Purpose |
|---|---|---|
| `LeftJumbotron` | `(0, 0)` | Main game view: menus, game select, scoreboard + count panel |
| `RightJumbotron` | `(480, 0)` | Currently blank (reserved for future content) |
| `Diamond` | `(960, 0)` | Currently blank (reserved for field diagram) |

### Main Loop (`app.py`)

The entry point initializes pygame, creates the three `ScreenBuffer` instances, and runs a tight loop:

1. Poll pygame events → dispatch to `state.handle_event()`
2. For each `ScreenBuffer`, call `draw(fullscreen)` (composites its 480×320 surface onto the main window)
3. `pygame.display.flip()`
4. Call `state.update_state()` to fetch new game data in the background (rate-limited by `MIN_TIME_BETWEEN_REQUESTS`)

---

## Module Reference

### `constants.py`

Single source of truth for all magic numbers and configuration. Everything is exported with `*` and imported that way throughout the codebase. Key groups:

- **Screen geometry**: `SCREEN_W=480`, `SCREEN_H=320`, panel offsets
- **Network**: `MLB_SCHEDULE_URL`, `MLB_LOGO_URL`, `REQUEST_TIMEOUT_SECONDS`, `MIN_TIME_BETWEEN_REQUESTS`
- **Schedule window**: `SCHEDULE_LOOKBACK_DAYS=7`, `SCHEDULE_LOOKAHEAD_DAYS=2`
- **Menu**: `MAIN_MENU_ITEMS`, `TABS`, `TAB_STATUSES`, `MENU_*` sizing constants
- **Scoreboard**: `SCOREBOARD_H=148` (`SCOREBOARD_HEADER_HEIGHT + 2 * SCOREBOARD_TEAM_COL_W`), `SCOREBOARD_BSO_PANEL_W=72`, font sizes, colors

When adding new UI, add sizing/color constants here rather than hardcoding them in components.

---

### `state.py`

Central application state. All mutable state lives here. Components read state via module-level accessor functions; they never hold references to state objects directly.

#### `DisplayMode` (Enum)

Controls which components are active in each `ScreenBuffer`:

- `MAIN_MENU` — top-level navigation
- `GAME_SELECT` — tabbed list of games (Finished / Live / Upcoming)
- `REPLAY` — finished game with inning/appearance scrubbing
- `LIVE` — live game scoreboard
- `PREVIEW` — upcoming game info

#### State models (Pydantic `BaseModel`)

| Model | Purpose |
|---|---|
| `MainMenuState` | Cursor row for the 4-item main menu |
| `GameSelectState` | Tab index, scroll offset, selected row, cached game rows |
| `SelectedGame` | Immutable snapshot of the game chosen in `GameSelectState` |
| `ReplayState` | Clock time, inning index, appearance index for replay scrubbing |
| `InningData` | `top: int | None`, `bottom: int | None` — one inning's half-inning values |
| `DisplayData` | Computed display snapshot: `inning_runs`, `runs/hits/errors` (as `InningData`), `balls`, `strikes`, `outs`, `clock` |
| `State` | Root model combining all of the above; owns `handle_scroll_x/y` and `handle_click_x/y` dispatch |

#### Key accessors

```python
get_state() -> State
get_game_display_data() -> DisplayData
get_game_data() -> baseball.Game | None
```

> **Architecture rule — display components must only use `get_game_display_data()`.**
> Components must never call `get_game_data()` or access raw `baseball.*` objects directly.
> Code inside `state.py` itself may call `get_game_data()` freely.
> All derived display data is computed inside `DisplayData.observe_game()` / `observe_appearance()`.
> If a new piece of data is needed in a component, add a field to `DisplayData` and populate it there.

#### `update_state()`

Called once per frame. If a game is selected and enough time has passed since the last fetch, it calls `baseball.get_game(...)` and invokes `_game_display_data.observe_game(game, replay_state)` to recompute `DisplayData`.

#### `DisplayData.observe_game(game, replay_state)`

Walks the `baseball.Game` inning/appearance tree, replaying pitches and outcomes up to the current `ReplayState` cursor (or to the end for live/finished games). Updates all fields in place: `inning_runs`, `runs`, `hits`, `errors`, `balls`, `strikes`, `outs`, `clock`, `pa_events`, and the active batter/pitcher/inning identifiers.

---

### `schedule.py`

Fetches and caches the MLB schedule for a rolling window (`SCHEDULE_LOOKBACK_DAYS` to `SCHEDULE_LOOKAHEAD_DAYS`). Parses the MLB Stats API JSON into `ScheduledGame` Pydantic models.

```python
get_available_games() -> Iterable[ScheduledGame]
```

The schedule is fetched lazily on first call and cached in-process.

---

### `logos.py`

Downloads team SVG logos from `MLB_LOGO_URL`, converts them to `pygame.Surface` via `svglib` + `reportlab`, and caches by `(team_id, width, height)`. SVG files are disk-cached under `./cache/logos/`.

```python
get_logo(team_id: int, width: int, height: int) -> pygame.Surface | None
```

Returns `None` on any error (network failure, parse failure, etc.) so callers must handle the missing-logo case gracefully.

---

### `components/base.py`

Defines the three base classes for all UI elements:

#### `Component` (ABC)

```python
class Component(ABC):
    def draw(self, surface: Surface) -> None: ...   # required
    def load(self): ...                             # optional; called on mode switch
```

`load()` is called once each time the component becomes active (mode changes). Use it for lazy initialization that needs pygame to be running (e.g., font loading that depends on screen state).

#### `ValueComponent(Component)` (ABC)

A caching wrapper for components whose output is a pure function of a single value. Implement two methods:

```python
def get_value(self) -> Any: ...           # extract the relevant slice of state
def render_value(self, value: Any) -> Surface: ...  # paint a fresh surface
```

`draw()` compares `get_value()` to the last seen value. If different, it calls `render_value()` and caches the result. This avoids re-rendering every frame when state hasn't changed.

Constructor takes a `pygame.Rect` that defines where the cached surface is blitted on the parent surface.

#### `ScreenBuffer` (ABC)

Owns a 480×320 `pygame.Surface` and an `(x, y)` offset on the main window.

```python
def get_active_components(self, mode: DisplayMode) -> Generator[Component, None, None]:
    ...  # yield components in back-to-front draw order
```

`draw()` calls each yielded component's `draw()` in order, then blits the internal surface to the main window. Components drawn later appear on top of earlier ones.

---

### `screens.py`

Concrete `ScreenBuffer` subclasses. Each screen holds component instances as attributes and yields the right subset based on `DisplayMode`.

```python
class LeftJumbotron(ScreenBuffer):
    # MAIN_MENU      → MainMenu
    # GAME_SELECT    → GameSelect
    # REPLAY / LIVE  → Scoreboard, then CountDisplay (drawn on top)
    # else           → BlankScreen
```

`RightJumbotron` and `Diamond` currently yield `BlankScreen` unconditionally.

---

### `components/`

| File | Class | Base | Description |
|---|---|---|---|
| `blank.py` | `BlankScreen` | `Component` | Fills the surface with `COLOR_BG` |
| `main_menu.py` | `MainMenu` | `Component` | 4-item vertical menu, highlights selected row |
| `game_select.py` | `GameSelect` | `Component` | Tabbed scrollable list of `ScheduledGame`s |
| `scoreboard.py` | `Scoreboard` | `Component` | Traditional MLB line score; occupies the bottom `SCOREBOARD_H=148` px at full 480 px width |
| `count_display.py` | `CountDisplay` | `ValueComponent` | Balls/Strikes/Outs panel; occupies the top `SCREEN_H - SCOREBOARD_H = 172` px of the right `SCOREBOARD_BSO_PANEL_W = 72` px column |

---

## LeftJumbotron Layout (REPLAY / LIVE mode)

```
┌────────────────────────────────────────┬──────────┐  y=0
│                                        │  BALLS   │
│         (nothing / future use)         │ ●●○○     │
│                                        ├──────────┤
│                                        │ STRIKES  │
│                                        │ ●●○      │
│                                        ├──────────┤
│                                        │  OUTS    │
│                                        │ ●○○      │
├────────────────────────────────────────┴──────────┤  y=172
│  Scoreboard (full 480px width)                    │
│  Header row + away row + home row = 148px         │
└───────────────────────────────────────────────────┘  y=320
         x=0                             x=408     x=480
```

---

## Input Handling (`state.py: handle_event`)

Input is designed for two push-button rotary encoders on a Raspberry Pi. The pygame `KEYDOWN` events below map directly to those physical controls:

| Key | Encoder action | Effect |
|---|---|---||
| Arrow Up / Down | Encoder A rotate | `handle_scroll_y(±1)` |
| Arrow Left / Right | Encoder B rotate | `handle_scroll_x(±1)` |
| Enter / Return | Encoder A press | `handle_click_x()` — confirms selection, advances mode |
| Space | Encoder B press | `handle_click_y()` — goes back |

Mode transitions:
- `MAIN_MENU` → (Enter on "Games") → `GAME_SELECT`
- `GAME_SELECT` → (Enter) → `REPLAY` / `LIVE` / `PREVIEW` depending on tab
- `GAME_SELECT` → (Space) → `MAIN_MENU`
- `REPLAY/LIVE/PREVIEW` → (Space) → `GAME_SELECT`

---

## How to Add a New Component

### Simple component

1. Create `baseball_display/components/my_component.py`:

```python
import pygame
from pygame import Surface
from baseball_display.components.base import Component
from baseball_display.constants import *
from baseball_display.state import get_state

class MyComponent(Component):
    def draw(self, surface: Surface) -> None:
        # read state, paint onto surface
        ...
```

2. Export from `baseball_display/components/__init__.py`:

```python
from .my_component import MyComponent
```

3. Add an instance to the appropriate `ScreenBuffer` in `screens.py` and yield it from `get_active_components()`.

### ValueComponent (cached rendering)

Use this when the component output depends on a small, equality-comparable value slice:

```python
from baseball_display.components.base import ValueComponent

class MyComponent(ValueComponent):
    def __init__(self) -> None:
        rect = pygame.Rect(x, y, w, h)   # where to blit on the parent surface
        super().__init__(rect)

    def get_value(self):
        dd = get_game_display_data()
        return dd.some_field   # return only what affects rendering

    def render_value(self, value) -> Surface:
        surf = Surface((w, h))
        # paint surf using value
        return surf
```

`render_value` is only called when `get_value()` returns something different from the previous frame. The returned surface is reused unchanged on subsequent frames.

### Adding a new display mode

1. Add a variant to `DisplayMode` in `state.py`.
2. Add the corresponding state model and wire it into `State`.
3. Add `handle_scroll_x/y` and `handle_click_x/y` branches in `State`.
4. Add an `elif mode == DisplayMode.NEW_MODE:` branch in each relevant `ScreenBuffer.get_active_components()`.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pygame` 2.6 | Rendering, event loop |
| `pydantic` | State models with validation |
| `baseball` | MLB game data (schedule, play-by-play) |
| `svglib` + `reportlab` | SVG → PNG → `pygame.Surface` for team logos |
