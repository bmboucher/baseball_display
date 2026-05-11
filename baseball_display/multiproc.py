"""Multi-process render mode.

Parent process owns input + MLB HTTP + DisplayData / State; three render
children each drive one physical SPI panel (left/right/diamond). The parent
publishes a pickled (DisplayData, State) snapshot to a shared
``multiprocessing.Manager.Namespace`` whenever local state has been mutated;
children check a shared ``Value('i')`` version counter once per frame (no
IPC roundtrip) and only re-fetch + unpickle the snapshot when the version
has advanced.

On the Pi, each child renders into an off-screen pygame Surface (with
SDL_VIDEODRIVER=dummy) and ships pixels directly to its ST7796S panel over
SPI. Cross-process SPI/GPIO contention is serialized by a shared
``mp.Lock``. The parent performs the one-time reset + per-panel init
before spawning children, because RST is shared across all three panels.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import os
import pickle
from dataclasses import dataclass, field
from typing import Any

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.logging_setup import configure_logging
from baseball_display.screens import SCREEN_NAMES, build_screen
from baseball_display.settings import PanelSettings, get_settings, resolve_panel

logger = logging.getLogger(__name__)

_JOIN_TIMEOUT_SECS = 2.0
_CHILD_FPS = 30


@dataclass
class SharedHandles:
    """Parent-side handle to the shared IPC primitives + spawned children."""

    manager: Any  # SyncManager — keep alive for the proxy's lifetime
    ns: Any  # Namespace proxy holding the pickled snapshot bytes
    version: Any  # mp.Value('i') — bumped by parent on each publish
    shutdown: Any  # mp.Event — set by parent on exit
    spi_lock: Any  # mp.Lock — serializes SPI bus + shared-GPIO access
    children: list[mp.Process] = field(default_factory=list)


def init_shared_handles() -> SharedHandles:
    manager = mp.Manager()
    ns = manager.Namespace()
    ns.snapshot = b""
    version = mp.Value("i", 0)
    shutdown = mp.Event()
    spi_lock = mp.Lock()
    return SharedHandles(
        manager=manager,
        ns=ns,
        version=version,
        shutdown=shutdown,
        spi_lock=spi_lock,
    )


def publish_snapshot(handles: SharedHandles) -> None:
    """Pickle the parent's current DisplayData + State and bump the version."""
    payload = pickle.dumps(
        (state.get_game_display_data(), state.get_state()),
        protocol=pickle.HIGHEST_PROTOCOL,
    )
    handles.ns.snapshot = payload
    with handles.version.get_lock():
        handles.version.value += 1


def init_panels_on_pi() -> bool:
    """Reset + init every configured ST7796S panel from the parent.

    Returns True if Pi modules were available and panels were initialized,
    False on non-Pi platforms (so callers know to skip panel-specific
    behavior in render children).

    Reset (GPIO5) is wired in parallel to all three panels, so it must
    only be pulsed once. We do it here, in the parent, before children
    are spawned — each subsequent panel.init() asserts only that panel's
    CS so init bytes don't bleed across panels.
    """
    try:
        import RPi.GPIO as gpio  # type: ignore[import-not-found]
    except Exception as e:
        logger.info("Pi GPIO/SPI unavailable (%s); panel init skipped", e)
        return False

    from baseball_display.st7796s import ST7796S, PanelConfig, open_spi

    settings = get_settings()
    if not settings.panels:
        logger.warning("No panel configs found in settings; nothing to init")
        return False

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    # All panels share one SPI bus; use the first panel's spi_hz to size it.
    first_ps = next(iter(settings.panels.values()))
    spi = open_spi(bus=first_ps.spi_bus, device=first_ps.spi_device, hz=first_ps.spi_hz)
    panels: list[ST7796S] = []
    for name, ps in settings.panels.items():
        pc = _panel_config_from_settings(name, ps)
        panels.append(ST7796S(pc, gpio, spi))

    if panels:
        panels[0].reset()  # one shared-RST pulse, drives all three panels

    for p in panels:
        p.init()
        logger.info("Initialized panel %r on CS=GPIO%d", p.config.name, p.config.cs_pin)

    spi.close()
    return True


def start_render_children(handles: SharedHandles) -> None:
    """Spawn one render process per screen name."""
    for name in SCREEN_NAMES:
        panel_settings = resolve_panel(name)
        proc = mp.Process(
            target=_render_worker,
            args=(
                name,
                panel_settings,
                handles.ns,
                handles.version,
                handles.shutdown,
                handles.spi_lock,
            ),
            name=f"baseball_display-{name}",
            daemon=False,
        )
        proc.start()
        handles.children.append(proc)
        logger.info(
            "Spawned render child %s (pid=%s, cs_pin=%s)",
            name,
            proc.pid,
            panel_settings.cs_pin if panel_settings else None,
        )


def shutdown_children(handles: SharedHandles) -> None:
    handles.shutdown.set()
    for proc in handles.children:
        proc.join(timeout=_JOIN_TIMEOUT_SECS)
    for proc in handles.children:
        if proc.is_alive():
            logger.warning("Render child %s did not exit; terminating", proc.name)
            proc.terminate()
            proc.join(timeout=_JOIN_TIMEOUT_SECS)


def _panel_config_from_settings(name: str, ps: PanelSettings) -> Any:
    """Lazy import to keep st7796s out of the Windows import path."""
    from baseball_display.st7796s import PanelConfig

    return PanelConfig(
        name=name,
        cs_pin=ps.cs_pin,
        dc_pin=ps.dc_pin,
        rst_pin=ps.rst_pin,
        led_pin=ps.led_pin,
        spi_bus=ps.spi_bus,
        spi_device=ps.spi_device,
        spi_hz=ps.spi_hz,
        rotation=ps.rotation,
        bgr=ps.bgr,
    )


def _try_open_panel(
    screen_name: str,
    panel_settings: PanelSettings,
    spi_lock: Any,
    log: logging.Logger,
) -> Any:
    """Attempt to open the SPI panel. Returns ST7796S or None on failure."""
    try:
        import RPi.GPIO as gpio  # type: ignore[import-not-found]

        from baseball_display.st7796s import ST7796S, open_spi

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        pc = _panel_config_from_settings(screen_name, panel_settings)
        spi = open_spi(bus=pc.spi_bus, device=pc.spi_device, hz=pc.spi_hz)
        panel = ST7796S(pc, gpio, spi, lock=spi_lock)
        log.info("Panel opened: CS=GPIO%d, rotation=%d", pc.cs_pin, pc.rotation)
        return panel
    except ImportError:
        log.info("Pi modules unavailable; falling back to visible window")
        return None
    except Exception:
        log.exception("Failed to open panel; falling back to visible window")
        return None


def _render_worker(
    screen_name: str,
    panel_settings: PanelSettings | None,
    ns: Any,
    version: Any,
    shutdown: Any,
    spi_lock: Any,
) -> None:
    """Child entry: render one ScreenBuffer and push pixels to its panel
    (Pi) or to a desktop window (fallback)."""
    configure_logging()
    log = logging.getLogger(f"baseball_display.render.{screen_name}")
    log.info("Render child starting for %r", screen_name)

    # Decide rendering target BEFORE pygame inits, because SDL reads
    # SDL_VIDEODRIVER at init time. On the Pi we render off-screen and ship
    # pixels via SPI; on the desktop we want a visible window for debugging.
    panel = (
        _try_open_panel(screen_name, panel_settings, spi_lock, log)
        if panel_settings is not None
        else None
    )
    if panel is not None:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ.setdefault("SDL_NOMOUSE", "1")

    import pygame  # noqa: PLC0415 — must come after env-var setup

    pygame.init()
    surface = pygame.display.set_mode((dc.SCREEN_W, dc.SCREEN_H))
    if panel is None:
        pygame.display.set_caption(f"baseball_display [{screen_name}]")
    screen = build_screen(screen_name)
    clock = pygame.time.Clock()
    local_version = -1

    try:
        while not shutdown.is_set():
            # Pull a fresh snapshot only when the parent has advanced the version.
            current_version = version.value
            if current_version != local_version:
                payload = ns.snapshot
                if payload:
                    try:
                        display_data, st = pickle.loads(payload)
                    except Exception:
                        log.exception("Failed to unpickle snapshot")
                    else:
                        state.set_game_display_data(display_data)
                        state.set_state(st)
                        local_version = current_version

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.info("QUIT received; signaling shutdown")
                    shutdown.set()
                    break

            try:
                screen.draw(surface)
            except Exception:
                log.exception("Error drawing screen")

            if panel is not None:
                try:
                    panel.display(surface)
                except Exception:
                    log.exception("Error pushing frame to panel")
            else:
                pygame.display.flip()

            clock.tick(_CHILD_FPS)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        log.info("Render child %r exiting", screen_name)
