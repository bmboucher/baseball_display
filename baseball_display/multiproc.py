"""Multi-process render mode.

Parent process owns input + MLB HTTP + DisplayData / State; three render
children each drive one physical screen (left/right/diamond). The parent
publishes a pickled (DisplayData, State) snapshot to a shared
``multiprocessing.Manager.Namespace`` whenever local state has been mutated;
children check a shared ``Value('i')`` version counter once per frame (no
IPC roundtrip) and only re-fetch + unpickle the snapshot when the version
has advanced.
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
from baseball_display.settings import resolve_fbdev

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
    children: list[mp.Process] = field(default_factory=list)


def init_shared_handles() -> SharedHandles:
    manager = mp.Manager()
    ns = manager.Namespace()
    ns.snapshot = b""
    version = mp.Value("i", 0)
    shutdown = mp.Event()
    return SharedHandles(manager=manager, ns=ns, version=version, shutdown=shutdown)


def publish_snapshot(handles: SharedHandles) -> None:
    """Pickle the parent's current DisplayData + State and bump the version."""
    payload = pickle.dumps(
        (state.get_game_display_data(), state.get_state()),
        protocol=pickle.HIGHEST_PROTOCOL,
    )
    handles.ns.snapshot = payload
    with handles.version.get_lock():
        handles.version.value += 1


def start_render_children(handles: SharedHandles) -> None:
    """Spawn one render process per screen name."""
    for name in SCREEN_NAMES:
        fbdev = resolve_fbdev(name)
        proc = mp.Process(
            target=_render_worker,
            args=(name, fbdev, handles.ns, handles.version, handles.shutdown),
            name=f"baseball_display-{name}",
            daemon=False,
        )
        proc.start()
        handles.children.append(proc)
        logger.info(
            "Spawned render child %s (pid=%s, fbdev=%s)", name, proc.pid, fbdev
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


def _render_worker(
    screen_name: str,
    fbdev: str | None,
    ns: Any,
    version: Any,
    shutdown: Any,
) -> None:
    """Child entry: own one pygame display and render one ScreenBuffer."""
    configure_logging()
    log = logging.getLogger(f"baseball_display.render.{screen_name}")
    log.info("Render child starting for screen %r (fbdev=%s)", screen_name, fbdev)

    # SDL reads these env vars at init time, so they must be set before
    # pygame is imported / pygame.init() is called.
    if fbdev:
        os.environ["SDL_VIDEODRIVER"] = "fbcon"
        os.environ["SDL_FBDEV"] = fbdev
        os.environ.setdefault("SDL_NOMOUSE", "1")

    import pygame  # noqa: PLC0415 — must come after env-var setup

    pygame.init()
    surface = pygame.display.set_mode((dc.SCREEN_W, dc.SCREEN_H))
    pygame.display.set_caption(f"baseball_display [{screen_name}]")
    screen = build_screen(screen_name)
    clock = pygame.time.Clock()
    local_version = -1

    try:
        while not shutdown.is_set():
            # Pull a fresh snapshot only when the parent has advanced the version.
            # Reading version.value is a cheap shared-memory op; reading ns.snapshot
            # is an IPC call, so we gate it behind the version compare.
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

            # Drain pygame events. The parent owns input; children only watch QUIT
            # so a window-close cleanly tears down the whole app.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.info("QUIT received; signaling shutdown")
                    shutdown.set()
                    break

            try:
                screen.draw(surface)
            except Exception:
                log.exception("Error drawing screen")
            pygame.display.flip()
            clock.tick(_CHILD_FPS)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        log.info("Render child %r exiting", screen_name)
