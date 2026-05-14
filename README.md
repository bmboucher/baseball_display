# baseball_display

A pygame-based MLB scoreboard for a three-panel "jumbotron." Each panel is
480×320; combined they show a live scoreboard, batting order / player
stats, and a field diagram with runner/defender badges.

Two render targets are supported from the same codebase:

- **Desktop**: a single 1440×320 pygame window (three panels side by side).
- **Raspberry Pi**: three physical ST7796S SPI displays, driven from one
  process via a pure-Python SPI driver. See [`PI_SETUP.md`](PI_SETUP.md)
  for the full hardware setup (wiring, kernel config, systemd unit,
  nightly auto-update cron).

## Quick start (desktop)

```bash
cd baseball_display          # must run from inside the project directory
python3 -m venv .venv
source .venv/bin/activate    # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -e .
python -m baseball_display
```

> Run these (and `python -m baseball_display`) from inside the
> `baseball_display/` project directory. From any parent directory,
> Python's import machinery resolves `baseball_display` as a namespace
> package pointing at the project folder itself and bypasses the
> editable install, producing a confusing `ImportError` like
> `cannot import name 'make_endpoint' from 'baseball_display.cache'`.

The UI font is bundled (Fira Code) so desktop and Pi render identically.

`settings.json` (in the working directory) holds runtime config. Set the
path via the `BASEBALL_DISPLAY_SETTINGS` env var. Missing file ⇒ defaults.

```jsonc
{
  "refresh_rate": 10,          // seconds between MLB API polls
  "multi_process": false,      // see "Multi-process mode" below
  "startup_team": "NYM"        // team abbreviation used to pick the initial game/mode at boot
}
```

## Running modes

`baseball_display.app.main()` picks one of three render paths at startup:

| Condition                                       | Path                       | What you see                                     |
|-------------------------------------------------|----------------------------|--------------------------------------------------|
| `multi_process=false` (default)                 | `_run_single_process`      | One 1440×320 pygame window                       |
| `multi_process=true` **and** on a Pi            | `_run_pi_panels`           | Three ST7796S SPI panels (headless, no window)   |
| `multi_process=true` **and** not on a Pi        | `_run_multi_process`       | A small "control" window + three 480×320 windows |

Detection is `import RPi.GPIO` — succeeds when `rpi-lgpio` is installed
(Pi only). Override the flag from the shell with
`BASEBALL_DISPLAY_MULTI_PROCESS=1`.

## Architecture

### Three-panel layout

```
┌──────────────────────────┬──────────────────────────┬──────────────────────────┐
│      LeftJumbotron       │      RightJumbotron      │         Diamond          │
│         480×320          │         480×320          │         480×320          │
└──────────────────────────┴──────────────────────────┴──────────────────────────┘
   x=0, y=0                   x=480                       x=960
```

Each panel is a `ScreenBuffer` (in `screens.py`). Components are yielded
per current `DisplayMode`:

| Mode          | LeftJumbotron                                         | RightJumbotron       | Diamond                       |
|---------------|-------------------------------------------------------|----------------------|-------------------------------|
| `MAIN_MENU`   | `MainMenu`                                            | (blank)              | field diagram (no overlays)   |
| `GAME_SELECT` | `GameSelect`                                          | `GamePreview`        | field diagram (no overlays)   |
| `PREVIEW`     | `GameCountdown`                                       | `GamePreview`        | field diagram (no overlays)   |
| `LIVE` / `REPLAY` | `Scoreboard`, `PitchDisplay`, `PAEvents`, `CountDisplay`, `ClockDisplay` | `BattingOrder`  | field + runner/defender/pitch overlays |
| `SETTINGS`    | `SettingsMenu`                                        | (blank)              | field diagram (no overlays)   |
| `PLAYERS`     | `PlayerSelect`                                        | `PlayerStatsPanel`   | field diagram (no overlays)   |

### Pi single-process render path

On the Pi we render to three off-screen pygame Surfaces (with
`SDL_VIDEODRIVER=dummy`, no real display) and push pixels via SPI:

1. `pygame.init()` once, dummy display.
2. Reset the panels (shared RST line pulsed once).
3. Send the ST7796S init sequence to each panel (CSCON unlock + gamma +
   MADCTL/COLMOD); see [`baseball_display/st7796s.py`](baseball_display/st7796s.py).
4. Main loop (≤30 FPS): poll encoders, `state.update_state()`, render
   each `ScreenBuffer` to its 480×320 surface, push pixels through the
   dirty-rectangle SPI driver.

The ST7796S driver tracks the previously-pushed RGB888 bytes per panel
and ships only the bounding box of changed pixels (RGB565 BE, chunked
to `spidev.bufsiz`). For mostly-static panels (scoreboard, batting
order) this means most frames skip SPI entirely; for the diamond's
runner animation, only the animation path is pushed.

### Desktop multi-process path

Used only for debugging the IPC + dirty-rect logic on a workstation.
Parent process owns input + MLB HTTP + State; three spawned children
each open a visible 480×320 pygame window. The parent publishes a
pickled `(DisplayData, State)` snapshot to a Manager namespace whenever
state changes; children pull on a shared version-counter bump. See
[`baseball_display/multiproc.py`](baseball_display/multiproc.py).

## Input

| Encoder            | Switch     | Rotate                     | Key emitted                |
|--------------------|------------|----------------------------|----------------------------|
| X (left)           | GPIO 24    | GPIO 22 (DT) + 23 (CLK)    | LEFT/RIGHT + SPACE (back)  |
| Y (right)          | GPIO 17    | GPIO 27 (DT) + 18 (CLK)    | UP/DOWN + ENTER (select)   |

`pi_input.PiInputAdapter` injects `pygame.KEYDOWN` events so the desktop
keyboard path and Pi encoder path use the same `state.handle_event`
dispatcher.

Mode transitions:

- `MAIN_MENU` → (Enter on "Games") → `GAME_SELECT`
- `MAIN_MENU` → (Enter on "Player Stats") → `PLAYERS`
- `MAIN_MENU` → (Enter on "Settings") → `SETTINGS`
- `GAME_SELECT` → (Enter) → `REPLAY` / `LIVE` / `PREVIEW` (depending on tab)
- Any submode → (Space) → back one level

## State model

All mutable state lives in `state.py` as Pydantic v2 models. Components
read state only via module-level accessor functions; **components must
never call `get_game_data()` or touch raw `GameFeed` objects** — all
display-derived data must live on `DisplayData` and be populated inside
`DisplayData.observe_game()`. The play-by-play replay engine is the only
thing that walks the live feed.

Module-level globals (`state.py`):

| Global                  | Type                | Set by                          |
|-------------------------|---------------------|---------------------------------|
| `_state`                | `State`             | `handle_event` mutations, `update_state` |
| `_game_data`            | `GameFeed \| None`  | `update_state` (refresh tick)   |
| `_game_data_parsed`     | `_GameData \| None` | `update_state`                  |
| `_game_display_data`    | `DisplayData`       | `DisplayData.observe_game`      |
| `_dirty`                | `bool`              | `handle_event`, `update_state` (consumed in multi-process for snapshot publish) |

The multi-process desktop path also uses `set_state` / `set_game_display_data`
setters to install pickled snapshots in render children — the
single-process and Pi paths use the in-place mutation directly.

## How to add a component

1. Create `baseball_display/components/my_component.py`. Subclass
   `Component` (override `draw(surface)`) or `ValueComponent` (override
   `get_value()` and `render_value(value)` — the base class caches the
   rendered surface and re-renders only when the value changes).
2. Re-export from `baseball_display/components/__init__.py`.
3. Read state with `get_game_display_data()` / `get_state()`. Pull
   constants from `display_constants.py`; don't hardcode geometry/colors.
4. Instantiate inside the relevant `ScreenBuffer` subclass in
   `screens.py` and yield it from `get_active_components(mode)`.

## How to add a display mode

1. Add a variant to `DisplayMode` in `state.py`.
2. Add the corresponding sub-state model and wire it into `State`.
3. Add `handle_scroll_x/y` and `handle_click_x/y` branches in `State`.
4. Add an `elif mode == DisplayMode.NEW_MODE:` branch in each relevant
   `ScreenBuffer.get_active_components()`.

## Project layout

```
baseball_display/
  app.py              # entrypoint; picks render path
  state.py            # all state models + DisplayMode + handle_event
  screens.py          # ScreenBuffer subclasses; build_screen() factory
  components/         # one file per UI component
  st7796s.py          # pure-Python ST7796S SPI driver (Pi only)
  multiproc.py        # desktop multi-process debug renderer
  pi_input.py         # rotary-encoder → pygame.KEYDOWN adapter
  statsapi.py         # caching, rate-limited MLB Stats API wrapper
  mlb_api/            # generated Pydantic models + JSON schemas
  display_constants.py# geometry, colors, font sizes
  settings.py         # Settings (refresh_rate, multi_process, panels)
  logging_setup.py    # shared dictConfig
scripts/
  build_schemas.py            # regenerate JSON schemas from sample responses
  regenerate_models.py        # regenerate Pydantic models from schemas
  patch_live_game_schema.py   # post-process patches for the live_game schema
  panel_test.py               # Pi bench test: cycle each panel through solid colors
  update_and_restart.sh       # nightly self-update (called by cron)
  verify_encoders.py          # standalone encoder diagnostic
PI_SETUP.md           # full Pi setup (hardware, OS, systemd, cron)
```

## Tests / Development

There is **no automated test suite**. `test_observe.py` and
`test_pitches.py` at the project root are live-endpoint debug scripts —
they hit `statsapi.mlb.com` and `print()` results, with no assertions.
Don't run them under `pytest` and don't count them as a "test pass."

## Dependencies

| Package          | Purpose                                          | When required           |
|------------------|--------------------------------------------------|-------------------------|
| `pygame`         | Rendering, fonts, event loop                     | Always                  |
| `pydantic`       | State models, JSON validation                    | Always                  |
| `MLB-StatsAPI`   | MLB API client                                   | Always                  |
| `rpi-lgpio`      | `RPi.GPIO`-compatible GPIO on modern Pi kernels  | Pi (`[raspberry-pi]`)   |
| `spidev`         | SPI bus access                                   | Pi (`[raspberry-pi]`)   |
| `numpy`          | RGB888 → RGB565 conversion + dirty-rect diff     | Pi (`[raspberry-pi]`)   |
