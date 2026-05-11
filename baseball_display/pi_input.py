from __future__ import annotations

import logging
import time
import queue
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pygame

logger = logging.getLogger(__name__)

# Transition lookup for quadrature decoding.
# Key: (previous_state, current_state), where state is 2-bit value:
#   bit1=CLK, bit0=DT
# Value: +1 for CW micro-step, -1 for CCW micro-step, 0 for invalid/noise.
_TRANSITIONS = {
    (0b00, 0b01): +1,
    (0b01, 0b11): +1,
    (0b11, 0b10): +1,
    (0b10, 0b00): +1,
    (0b00, 0b10): -1,
    (0b10, 0b11): -1,
    (0b11, 0b01): -1,
    (0b01, 0b00): -1,
}


@dataclass(frozen=True)
class EncoderConfig:
    name: str
    clk_pin: int
    dt_pin: int
    sw_pin: int
    cw_key: int
    ccw_key: int
    button_key: int


class _RotaryEncoder:
    def __init__(
        self,
        config: EncoderConfig,
        gpio: Any,
        emit_key: Callable[[int], None],
    ) -> None:
        self.config = config
        self._gpio = gpio
        self._emit_key = emit_key
        self._last_state = 0
        self._accumulator = 0
        self._polling_mode = False
        self._last_button_pressed = False
        self._last_button_press_ts = 0.0
        self._button_debounce_seconds = 0.04

    def setup(self) -> None:
        self._gpio.setup(self.config.clk_pin, self._gpio.IN, pull_up_down=self._gpio.PUD_UP)
        self._gpio.setup(self.config.dt_pin, self._gpio.IN, pull_up_down=self._gpio.PUD_UP)
        self._gpio.setup(self.config.sw_pin, self._gpio.IN, pull_up_down=self._gpio.PUD_UP)

        self._last_state = self._read_state()
        self._last_button_pressed = self._read_button_pressed()

        try:
            self._gpio.add_event_detect(
                self.config.clk_pin,
                self._gpio.BOTH,
                callback=self._on_rotate,
                bouncetime=1,
            )
            self._gpio.add_event_detect(
                self.config.dt_pin,
                self._gpio.BOTH,
                callback=self._on_rotate,
                bouncetime=1,
            )
            self._gpio.add_event_detect(
                self.config.sw_pin,
                self._gpio.BOTH,
                callback=self._on_button,
                bouncetime=40,
            )
        except RuntimeError:
            self._polling_mode = True
            logger.warning(
                "[%s] GPIO edge detection unavailable; using polling fallback",
                self.config.name,
            )

    def cleanup(self) -> None:
        if self._polling_mode:
            return
        for pin in (self.config.clk_pin, self.config.dt_pin, self.config.sw_pin):
            try:
                self._gpio.remove_event_detect(pin)
            except Exception:
                logger.debug("remove_event_detect failed for pin %s", pin, exc_info=True)

    def _read_state(self) -> int:
        clk = self._gpio.input(self.config.clk_pin)
        dt = self._gpio.input(self.config.dt_pin)
        return (clk << 1) | dt

    def _read_button_pressed(self) -> bool:
        return self._gpio.input(self.config.sw_pin) == self._gpio.LOW

    def _on_rotate(self, _channel: int) -> None:
        current = self._read_state()
        delta = _TRANSITIONS.get((self._last_state, current), 0)
        self._last_state = current

        if delta == 0:
            return

        self._accumulator += delta
        if abs(self._accumulator) >= 4:
            detents = int(self._accumulator / 4)
            self._accumulator -= detents * 4
            if detents > 0:
                key = self.config.cw_key
            else:
                key = self.config.ccw_key
            for _ in range(abs(detents)):
                self._emit_key(key)

    def _on_button(self, _channel: int) -> None:
        # Pull-up wiring: LOW=pressed, HIGH=released. Emit only on press.
        pressed = self._read_button_pressed()
        if pressed:
            self._emit_key(self.config.button_key)

    def poll(self) -> None:
        if not self._polling_mode:
            return

        current_state = self._read_state()
        delta = _TRANSITIONS.get((self._last_state, current_state), 0)
        self._last_state = current_state

        if delta != 0:
            self._accumulator += delta
            if abs(self._accumulator) >= 4:
                detents = int(self._accumulator / 4)
                self._accumulator -= detents * 4
                key = self.config.cw_key if detents > 0 else self.config.ccw_key
                for _ in range(abs(detents)):
                    self._emit_key(key)

        pressed = self._read_button_pressed()
        now = time.monotonic()
        if pressed and not self._last_button_pressed:
            if now - self._last_button_press_ts >= self._button_debounce_seconds:
                self._emit_key(self.config.button_key)
                self._last_button_press_ts = now
        self._last_button_pressed = pressed


class PiInputAdapter:
    def __init__(self, gpio: Any, encoders: list[_RotaryEncoder]) -> None:
        self._gpio = gpio
        self._encoders = encoders
        self._queue: queue.SimpleQueue[int] = queue.SimpleQueue()
        self._closed = False

    @classmethod
    def create(cls) -> PiInputAdapter | None:
        if not sys.platform.startswith("linux"):
            logger.info("Pi GPIO input disabled: non-Linux platform")
            return None

        if not _is_raspberry_pi():
            logger.info(
                "Raspberry Pi model string not detected; attempting GPIO init on Linux anyway"
            )

        try:
            import RPi.GPIO as gpio  # type: ignore[import-not-found]
        except Exception as exc:
            logger.info(
                "RPi.GPIO not available (%s); running keyboard-only input mode",
                exc,
            )
            return None

        try:
            gpio.setmode(gpio.BCM)
            gpio.setwarnings(False)

            adapter = cls(gpio, [])
            adapter._encoders = [
                _RotaryEncoder(
                    EncoderConfig(
                        name="X encoder (left)",
                        clk_pin=22,
                        dt_pin=23,
                        sw_pin=24,
                        cw_key=pygame.K_RIGHT,
                        ccw_key=pygame.K_LEFT,
                        button_key=pygame.K_RETURN,
                    ),
                    gpio,
                    adapter._queue.put_nowait,
                ),
                _RotaryEncoder(
                    EncoderConfig(
                        name="Y encoder (right)",
                        clk_pin=18,
                        dt_pin=27,
                        sw_pin=17,
                        cw_key=pygame.K_DOWN,
                        ccw_key=pygame.K_UP,
                        button_key=pygame.K_SPACE,
                    ),
                    gpio,
                    adapter._queue.put_nowait,
                ),
            ]

            for encoder in adapter._encoders:
                encoder.setup()

            logger.info(
                "Pi GPIO input enabled: X encoder -> LEFT/RIGHT + RETURN, "
                "Y encoder -> UP/DOWN + SPACE"
            )
            return adapter
        except Exception:
            logger.exception("Failed to initialize Pi GPIO input; falling back to keyboard-only")
            try:
                gpio.cleanup()
            except Exception:
                logger.debug("GPIO cleanup after init failure failed", exc_info=True)
            return None

    def poll_pygame_events(self) -> list[pygame.event.Event]:
        for encoder in self._encoders:
            encoder.poll()

        events: list[pygame.event.Event] = []
        while True:
            try:
                key = self._queue.get_nowait()
            except queue.Empty:
                break
            events.append(pygame.event.Event(pygame.KEYDOWN, key=key))
        return events

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

        for encoder in self._encoders:
            encoder.cleanup()

        try:
            self._gpio.cleanup()
        except Exception:
            logger.debug("GPIO cleanup failed", exc_info=True)


def _is_raspberry_pi() -> bool:
    model_paths = [
        Path("/proc/device-tree/model"),
        Path("/sys/firmware/devicetree/base/model"),
    ]

    for model_file in model_paths:
        try:
            model = model_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "Raspberry Pi" in model:
            return True

    return False
