import logging
import multiprocessing as mp
import time

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.logging_setup import configure_logging
from baseball_display.multiproc import (
    init_panels_on_pi,
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
)
from baseball_display.settings import is_multi_process_enabled, load_settings
from baseball_display.state import handle_event
from baseball_display.statsapi import start_prefetch_thread

configure_logging()
logger = logging.getLogger(__name__)

_PARENT_FPS = 30
_PARENT_TICK_SECONDS = 1.0 / _PARENT_FPS
_CONTROL_WINDOW_SIZE = (240, 120)


def main() -> None:
    load_settings()
    start_prefetch_thread()
    state.initialize_startup_mode("NYM")

    if is_multi_process_enabled():
        logger.info("Multi-process mode enabled")
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

    # On the Pi: reset + init all three ST7796S panels here, before spawning
    # children. RST is shared, so it can only be pulsed once; each per-panel
    # init then runs with only that panel's CS asserted. Returns False on
    # non-Pi platforms (RPi.GPIO/spidev unavailable) and is a no-op there.
    init_panels_on_pi()

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
