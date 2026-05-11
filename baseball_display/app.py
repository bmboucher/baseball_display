import logging
import multiprocessing as mp
import os
import time

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.logging_setup import configure_logging
from baseball_display.multiproc import (
    init_shared_handles,
    publish_snapshot,
    shutdown_children,
    start_render_children,
)
from baseball_display.pi_input import PiInputAdapter
from baseball_display.screens import (
    Diamond,
    LeftJumbotron,
    RightJumbotron,
    ScreenBuffer,
    build_screen,
)
from baseball_display.settings import (
    get_settings,
    is_multi_process_enabled,
    load_settings,
)
from baseball_display.state import handle_event
from baseball_display.statsapi import start_prefetch_thread

configure_logging()
logger = logging.getLogger(__name__)

_PARENT_FPS = 30
_PARENT_TICK_SECONDS = 1.0 / _PARENT_FPS
_CONTROL_WINDOW_SIZE = (240, 120)


def _on_pi() -> bool:
    """True if rpi-lgpio (or legacy RPi.GPIO) is importable.

    Determines whether we drive real SPI panels or fall back to the
    desktop multi-process pygame-windows path.
    """
    try:
        import RPi.GPIO  # noqa: F401  PLC0415 — runtime import for detection
        return True
    except ImportError:
        return False


def main() -> None:
    load_settings()
    start_prefetch_thread()
    state.initialize_startup_mode("NYM")

    if is_multi_process_enabled():
        if _on_pi():
            # The "multi-process" flag is conceptually "render three panels
            # separately". On the Pi that means three SPI panels, not three
            # OS processes — pygame's one-display-per-process limit is moot
            # here because we render to off-screen surfaces with
            # SDL_VIDEODRIVER=dummy and ship pixels via spidev. Doing this
            # in one process also avoids cross-process contention for the
            # shared DC/RST/LED GPIOs, which rpi-lgpio refuses to allow.
            logger.info("Multi-process mode enabled → Pi panel render path")
            _run_pi_panels()
        else:
            logger.info("Multi-process mode enabled → desktop windows path")
            _run_multi_process()
    else:
        logger.info("Single-process mode")
        _run_single_process()


def _run_single_process() -> None:
    logger.info("Initializing pygame...")
    pygame.init()

    # create the main window and the screen buffers
    fullscreen: pygame.Surface = pygame.display.set_mode(
        (dc.APP_FULL_SCREEN_W, dc.APP_FULL_SCREEN_H)
    )
    pygame.display.set_caption(dc.APP_WINDOW_TITLE)
    screens: list[ScreenBuffer] = [LeftJumbotron(), RightJumbotron(), Diamond()]
    pi_input = PiInputAdapter.create()
    if pi_input is None:
        logger.info("Pi GPIO input adapter inactive; keyboard-only input enabled")
    else:
        logger.info("Pi GPIO input adapter active")

    logger.info("Starting main loop...")
    try:
        while True:
            # handle user input
            events = pygame.event.get()
            if pi_input is not None:
                events.extend(pi_input.poll_pygame_events())

            for event in events:
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

                try:
                    handle_event(event)
                except Exception:
                    logger.exception(f"Error handling event {event}")

            # rerender and paint the screen
            for screen in screens:
                try:
                    screen.draw(fullscreen)
                except Exception:
                    logger.exception(f"Error drawing screen {type(screen)}")
            pygame.display.flip()

            # potentially update the game data in the background
            try:
                state.update_state()
            except Exception:
                logger.exception(f"Error updating state")
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        if pi_input is not None:
            pi_input.close()
        pygame.quit()


def _run_pi_panels() -> None:
    """Single-process renderer for the Pi: own all GPIOs + SPI + panels.

    rpi-lgpio enforces exclusive pin ownership per process, so the previous
    multi-process design fought over the shared DC/RST/LED pins. Here all
    three panels live in one process; pygame renders to off-screen 480x320
    surfaces with SDL_VIDEODRIVER=dummy, and a single render loop pushes
    each surface to its panel via SPI.
    """
    # Imports only on Pi so non-Pi platforms don't need the deps.
    import RPi.GPIO as gpio  # type: ignore[import-not-found]

    from baseball_display.multiproc import _panel_config_from_settings
    from baseball_display.st7796s import ST7796S, open_spi

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_NOMOUSE", "1")
    pygame.init()
    # pygame.font and the screen buffers need a display surface to be set
    # up — with the dummy driver this is a 1x1 in-memory surface.
    pygame.display.set_mode((1, 1))

    settings = get_settings()
    if not settings.panels:
        logger.error("multi_process enabled but settings.panels is empty")
        return

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    first_ps = next(iter(settings.panels.values()))
    spi = open_spi(
        bus=first_ps.spi_bus, device=first_ps.spi_device, hz=first_ps.spi_hz
    )

    # One tuple per panel: (driver, ScreenBuffer, off-screen pygame Surface).
    panel_set: list[tuple[ST7796S, ScreenBuffer, pygame.Surface]] = []
    for name, ps in settings.panels.items():
        pc = _panel_config_from_settings(name, ps)
        driver = ST7796S(pc, gpio, spi)
        screen = build_screen(name)
        surface = pygame.Surface((dc.SCREEN_W, dc.SCREEN_H))
        panel_set.append((driver, screen, surface))

    # RST is shared, so one pulse resets all three; each subsequent init
    # only affects the panel whose CS is asserted by that ST7796S.init().
    panel_set[0][0].reset()
    for driver, _, _ in panel_set:
        driver.init()
        logger.info("Initialized panel %r on CS=GPIO%d", driver.config.name, driver.config.cs_pin)

    pi_input = PiInputAdapter.create()
    if pi_input is None:
        logger.warning(
            "Pi input adapter unavailable; encoders will not register"
        )

    logger.info("Starting Pi panel render loop...")
    try:
        while True:
            tick_start = time.monotonic()

            # Encoders inject pygame.event.Event instances directly via
            # pi_input; there's no real SDL window so pygame.event.get()
            # would return nothing useful here.
            if pi_input is not None:
                for event in pi_input.poll_pygame_events():
                    try:
                        handle_event(event)
                    except Exception:
                        logger.exception(f"Error handling event {event}")

            try:
                state.update_state()
            except Exception:
                logger.exception("Error updating state")
            state.consume_dirty()  # not used in this path (always re-render)

            for driver, screen, surface in panel_set:
                try:
                    screen.draw(surface)
                    driver.display(surface)
                except Exception:
                    logger.exception(
                        "Error rendering/pushing panel %r", driver.config.name
                    )

            elapsed = time.monotonic() - tick_start
            sleep_for = _PARENT_TICK_SECONDS - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        if pi_input is not None:
            pi_input.close()
        try:
            spi.close()
        except Exception:
            pass
        try:
            gpio.cleanup()
        except Exception:
            pass
        pygame.quit()


def _run_multi_process() -> None:
    # Use spawn everywhere so Windows dev and Linux/Pi prod behave identically.
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        # Already set (e.g. by a previous main() call in the same interpreter).
        pass

    handles = init_shared_handles()
    # Publish initial state so the first frame in each child has data to render.
    publish_snapshot(handles)
    state.consume_dirty()  # clear the dirty flag set by initialization

    pi_input = PiInputAdapter.create()
    # On the Pi all input comes from the GPIO encoders, so we skip pygame
    # entirely in the parent — no display, no event queue, no SDL context.
    # On desktop (no pi_input) we open a tiny pygame window solely to capture
    # keyboard input so the parent has a way to drive the state machine.
    use_control_window = pi_input is None

    if use_control_window:
        logger.info("Initializing pygame (parent control window)...")
        pygame.init()
        control = pygame.display.set_mode(_CONTROL_WINDOW_SIZE)
        pygame.display.set_caption("baseball_display control")
        control.fill((20, 20, 20))
        pygame.display.flip()
        logger.info("Keyboard input enabled via control window")
    else:
        logger.info("Pi GPIO input adapter active; parent runs without pygame")

    start_render_children(handles)

    logger.info("Starting parent loop...")
    try:
        while not handles.shutdown.is_set():
            tick_start = time.monotonic()

            # handle user input
            events: list[pygame.event.Event] = []
            if use_control_window:
                events.extend(pygame.event.get())
            if pi_input is not None:
                events.extend(pi_input.poll_pygame_events())

            for event in events:
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

                try:
                    handle_event(event)
                except Exception:
                    logger.exception(f"Error handling event {event}")

            # refresh game data (sets _dirty if anything mutated)
            try:
                state.update_state()
            except Exception:
                logger.exception("Error updating state")

            # ship snapshot to children only when state actually changed
            if state.consume_dirty():
                try:
                    publish_snapshot(handles)
                except Exception:
                    logger.exception("Error publishing snapshot")

            # bail out if any render child died unexpectedly
            for proc in handles.children:
                if not proc.is_alive():
                    logger.error(
                        "Render child %s died (exitcode=%s); shutting down",
                        proc.name,
                        proc.exitcode,
                    )
                    raise KeyboardInterrupt

            elapsed = time.monotonic() - tick_start
            sleep_for = _PARENT_TICK_SECONDS - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        if pi_input is not None:
            pi_input.close()
        shutdown_children(handles)
        if use_control_window:
            pygame.quit()
