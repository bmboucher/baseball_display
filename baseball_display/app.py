import logging
from logging.config import dictConfig

import pygame

import baseball_display.display_constants as dc
from baseball_display import state
from baseball_display.pi_input import PiInputAdapter
from baseball_display.screens import (
    Diamond,
    LeftJumbotron,
    RightJumbotron,
    ScreenBuffer,
)
from baseball_display.settings import load_settings
from baseball_display.state import handle_event
from baseball_display.statsapi import start_prefetch_thread

dictConfig(
    {
        "version": 1,
        "loggers": {
            "baseball_display": {
                "handlers": ["console"],
                "level": "INFO",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "simple",
            },
        },
        "formatters": {
            "simple": {
                "format": "[%(asctime)s] %(levelname)s - %(message)s",
            },
        },
    }
)

logger = logging.getLogger(__name__)


def main() -> None:
    load_settings()
    start_prefetch_thread()
    state.initialize_startup_mode("NYM")
    logger.info("Initializing pygame...")
    pygame.init()

    # create the main window and the screen buffers
    fullscreen: pygame.Surface = pygame.display.set_mode(
        (dc.APP_FULL_SCREEN_W, dc.APP_FULL_SCREEN_H)
    )
    pygame.display.set_caption(dc.APP_WINDOW_TITLE)
    screens: list[ScreenBuffer] = [LeftJumbotron(), RightJumbotron(), Diamond()]
    pi_input = PiInputAdapter.create()

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
