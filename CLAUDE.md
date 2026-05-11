# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read the README first, but verify

`README.md` has an extensive architecture section (three-panel layout, state model, components, input handling, "how to add a component" recipes). **Read it before making structural changes.** However, the README has drifted from the code in several places — verify against the source before relying on its specifics:

- `DisplayMode` now also includes `SETTINGS` and `PLAYERS` (see `state.py` ~line 802). The README only lists the original 5.
- `RightJumbotron` and `Diamond` are no longer blank — `screens.py` renders different components depending on mode.
- `components/` has grown well beyond the README's table (now includes `batting_order`, `clock_display`, `field`, `game_countdown`, `game_preview`, `pa_events`, `pitch_display`, `player_select`, `player_stats_panel`, `settings_menu`).
- The README references a `schedule.py` module that no longer exists. MLB HTTP is now in `statsapi.py` (caching + rate-limited wrapper) plus the generated client in `mlb_api/`.

The **load-bearing architecture rules** in the README are still correct and important:

- Display components **must only** call `get_game_display_data()` — never `get_game_data()` and never touch raw `baseball.*` / `GameFeed` objects. All derived display data is computed inside `DisplayData.observe_game()`. If a component needs new data, add a field on `DisplayData` and populate it there.
- All sizing / colors / network constants belong in `constants.py` (and `display_constants.py`); don't hardcode them in components.
- All MLB HTTP traffic goes through `statsapi.py`. Anything else risks the rate limiter / cache and may get the host IP throttled.

## Environment

- Python 3.12, pygame 2.6 (note: `pyproject.toml` says `requires-python = ">=3.8"`, but the working venv is 3.12).
- Venv lives at `C:\Repos\baseball_display\.venv`. Activate from PowerShell with `.\.venv\Scripts\Activate.ps1`.
- Editable install: `pip install -e .` (the `[raspberry-pi]` extra adds `RPi.GPIO` and is only installable on a Pi).
- On Windows the rotary-encoder code path is automatically disabled — `PiInputAdapter.create()` returns `None` and the app falls back to keyboard input. No action needed.

## Running

```powershell
python -m baseball_display    # preferred
baseball-display              # installed console script (after editable install)
python main.py                # equivalent shim
```

`main.py` and `baseball_display/__main__.py` both just call `app.main`.

Settings come from `./settings.json` (currently just `refresh_rate`). Override the path with `BASEBALL_DISPLAY_SETTINGS=<path>` env var. Missing file → defaults, no error.

## Tests

There is **no real test suite**. `test_observe.py` and `test_pitches.py` at the project root are **scratch debug scripts** — they hit live MLB endpoints for specific game dates and `print()` results. They are not pytest tests and have no assertions. Don't run them as part of a "test pass"; treat them as throwaway probes you can rewrite freely.

If you add real tests, there's currently no test runner configured; pick one (pytest is the obvious choice) and document it here.

## MLB API: schemas → models workflow

The `mlb_api/` package is **generated code**. The flow is:

1. `scripts/build_schemas.py` — fetches sample responses from `statsapi.mlb.com` and writes cleaned JSON Schemas into `baseball_display/mlb_api/schemas/`. Crucially, it merges all per-player schemas (which would otherwise become `Batting2`, `Batting3`, … `Batting75`) into a single `Player` schema using `genson`.
2. `scripts/regenerate_models.py` — runs `datamodel-codegen` on each schema and writes Pydantic v2 models into `baseball_display/mlb_api/models/`. Flags include `--reuse-model` (collapse duplicates), `--use-title-as-name` (use schema `title` for class names), and `--force-optional` (real responses omit fields the sample had).

Run `python scripts/regenerate_models.py` after editing any schema. To target one: `python scripts/regenerate_models.py live_game`.

`baseball_display/mlb_api/README.md` is the openapi-python-client template README and is **not** representative of this package's actual API — ignore it.

## File you'll touch most

- `state.py` (2300+ lines) — every state model, every mode transition, `DisplayData.observe_game()` (the play-by-play replay engine), and the central `handle_event` dispatcher. When data flow feels wrong, this is almost always where the fix goes.
- `constants.py` / `display_constants.py` — geometry, colors, menu definitions.
- `statsapi.py` — caching + rate-limited MLB HTTP wrapper. Touch this rather than calling `urllib`/`httpx` directly from elsewhere.
- `screens.py` — three `ScreenBuffer` subclasses; their `get_active_components()` decides which components render in which mode.

## Pi-specific notes

Encoder wiring (BCM): A switch=17, A enc=27/22, B switch=5, B enc=6/13. The Pi adapter translates encoder rotation/press into pygame `KEYDOWN` events (arrows / Enter / Space) so the desktop and Pi code paths share input handling. `scripts/verify_encoders.py` is a standalone Pi-only diagnostic — it imports `RPi.GPIO` at module load, so don't run it on Windows.
