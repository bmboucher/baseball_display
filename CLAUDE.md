# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read README and PI_SETUP first

`README.md` has the architecture overview (three-panel layout, modes,
render paths) and `PI_SETUP.md` has the hardware setup (wiring,
config.txt, systemd, cron). Read both before any structural change.

The architecture rules are load-bearing:

- Display components **must only** call `get_game_display_data()` and
  `get_state()`. They must not call `get_game_data()` or touch raw
  `GameFeed` objects directly. All derived display data is computed
  inside `DisplayData.observe_game()` in `state.py`. If a component
  needs new data, add a field to `DisplayData` and populate it there.
- Sizes, colors, layout constants live in `display_constants.py`.
  Don't hardcode geometry/colors in components.
- All MLB HTTP traffic goes through `statsapi.py` (caching +
  per-thread rate-limited wrapper). Anything else risks getting the
  host IP throttled.

## Running modes

The entrypoint `app.main()` picks one of three render paths based on
the `multi_process` setting (or `BASEBALL_DISPLAY_MULTI_PROCESS=1` env
override) and whether `RPi.GPIO`/`rpi-lgpio` is importable:

- `_run_single_process` — desktop default. One 1440×320 pygame window
  with all three panels rendered side-by-side onto a fullscreen
  surface.
- `_run_pi_panels` — multi-process + Pi. Single process owns
  pygame (headless, SDL_VIDEODRIVER=dummy), all six GPIOs, the SPI
  bus, and three ST7796S panel drivers. Renders three off-screen
  Surfaces and pushes pixels via SPI.
- `_run_multi_process` — multi-process + non-Pi. Desktop debug mode:
  a small parent control window plus three spawned children, each
  with a visible 480×320 pygame window. Same IPC machinery as Pi was
  using before consolidation; kept for testing the IPC code paths.

There used to be a multi-process implementation on the Pi too, but
`rpi-lgpio` enforces exclusive per-process pin ownership and the three
children fought over the shared DC/RST/LED GPIOs. The single-process
Pi path replaced it — `pygame` doesn't need separate processes when
all displays are off-screen.

## Environment

- Python 3.12 on Windows desktop venv (`C:\Repos\baseball_display\.venv`).
- Python 3.13 on Pi (system venv per `PI_SETUP.md`).
- `pyproject.toml` says `requires-python = ">=3.8"` but newer features
  are used freely; the floor isn't enforced in CI.
- The `[raspberry-pi]` extra pulls `rpi-lgpio` (drop-in for `RPi.GPIO`
  on modern Pi kernels) plus `spidev` and `numpy`. Don't try to
  install `[raspberry-pi]` on Windows.
- On non-Pi platforms `PiInputAdapter.create()` returns `None` and the
  app falls back to pygame keyboard input. No action needed.

## Running

```powershell
python -m baseball_display    # preferred
baseball-display              # console script (after editable install)
python main.py                # equivalent shim
```

`main.py` and `baseball_display/__main__.py` both call `app.main`,
guarded by `if __name__ == "__main__":` because the desktop
multi-process path uses `spawn` and would otherwise recurse.

Settings come from `./settings.json`. Path override:
`BASEBALL_DISPLAY_SETTINGS=<path>`. Multi-process override:
`BASEBALL_DISPLAY_MULTI_PROCESS=1`.

## Tests

No real test suite. `test_observe.py` / `test_pitches.py` at the
project root are scratch debug scripts that hit live MLB endpoints
and `print()` results — no assertions, don't include in any "test
pass." Treat them as throwaway probes.

## MLB API: schemas → models workflow

The `mlb_api/` package is generated code:

1. `scripts/build_schemas.py` — fetches sample responses from
   `statsapi.mlb.com` and writes cleaned JSON Schemas into
   `baseball_display/mlb_api/schemas/`. Merges per-player schemas
   (which would otherwise become `Batting2`, …, `Batting75`) into a
   single `Player` schema via `genson`.
2. `scripts/regenerate_models.py` — runs `datamodel-codegen` on each
   schema and writes Pydantic v2 models into
   `baseball_display/mlb_api/models/`. Flags include `--reuse-model`,
   `--use-title-as-name`, and `--force-optional`.

Target one schema: `python scripts/regenerate_models.py live_game`.

`baseball_display/mlb_api/README.md` is the openapi-python-client
template README — ignore it; it doesn't describe this package's
actual API.

## Files you'll touch most

- `state.py` (2300+ lines): every state model, every mode transition,
  `DisplayData.observe_game()` (the play-by-play replay engine), and
  `handle_event`. When data flow feels wrong, the fix is almost always
  here.
- `display_constants.py`: geometry, colors, font sizes.
- `statsapi.py`: caching + rate-limited MLB HTTP. Always go through this.
- `screens.py`: the three `ScreenBuffer` subclasses and `build_screen()`.
- `st7796s.py`: the pure-Python SPI driver (Pi only). Dirty-rect
  tracking lives here.
- `app.py`: the render path picker and the three concrete render loops.

## Pi-specific notes

- Encoder wiring (BCM): X switch=24, X enc=22/23 → LEFT/RIGHT + SPACE;
  Y switch=17, Y enc=18/27 → UP/DOWN + ENTER. Documented in
  `PI_SETUP.md` §1.
- Panel wiring (BCM): CS GPIO 8/7/0 (left/right/diamond), shared D/C
  GPIO 1, shared RST GPIO 5, backlight GPIO 25. The Python driver in
  `st7796s.py` manages all GPIOs manually — the kernel SPI controller's
  hardware CE0/CE1 are overridden via `gpio.setup(..., OUT)` (Linux
  GPIO chardev takes precedence over the SPI alt-function as long as
  we don't open `/dev/spidev0.0` with active CS).
- The pure-Python ST7796S driver exists because the stock Pi OS kernel
  doesn't ship an `fb_st7796s`, and `fb_ili9486` doesn't issue the
  vendor `CSCON` (0xF0) command ST7796S needs before accepting pixel
  writes. The custom DTS overlay attempts were a dead end.
- SPI clock is 16 MHz. Higher clocks cause bit errors on the
  three-panel shared-MOSI fanout (panels render noise). If you change
  wiring (shorter leads, etc.), bench with `scripts/panel_test.py` and
  `PANEL_TEST_SPI_HZ` to find the new ceiling.
- `scripts/verify_encoders.py` is a standalone Pi-only diagnostic — it
  imports `RPi.GPIO` at module load, so don't run it on Windows.

## Auto-update / autostart

Production Pi runs as a systemd service (`baseball-display.service`,
`PI_SETUP.md` §6). A `/etc/cron.d/baseball-display-update` job
runs `scripts/update_and_restart.sh` at 2 AM America/New_York; the
script `git pull --ff-only`s the repo (as the repo's owning user),
optionally re-runs `pip install -e .` if `pyproject.toml` changed,
and restarts the service when HEAD moves. Logs to syslog with tag
`baseball-display-update` and to `/var/log/baseball-display-update.log`.
