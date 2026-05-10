#!/usr/bin/env python3
"""Quick rotary encoder + push-button verification tool for Raspberry Pi.

Wiring (BCM numbering):
- Device A switch: GPIO 17
- Device A encoder: GPIO 27 (CLK), GPIO 22 (DT)
- Device B switch: GPIO 5
- Device B encoder: GPIO 6 (CLK), GPIO 13 (DT)

Usage:
    python3 scripts/verify_encoders.py

Press Ctrl+C to quit.
"""

from __future__ import annotations

import signal
import sys
import time
from dataclasses import dataclass

import RPi.GPIO as GPIO


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


@dataclass
class EncoderConfig:
    name: str
    clk_pin: int
    dt_pin: int
    sw_pin: int


class RotaryEncoder:
    def __init__(self, config: EncoderConfig) -> None:
        self.config = config
        self._last_state = 0
        self._accumulator = 0
        self.steps = 0

    def setup(self) -> None:
        GPIO.setup(self.config.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.config.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.config.sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self._last_state = self._read_state()

        # Watch both encoder pins to decode quadrature transitions.
        GPIO.add_event_detect(
            self.config.clk_pin,
            GPIO.BOTH,
            callback=self._on_rotate,
            bouncetime=1,
        )
        GPIO.add_event_detect(
            self.config.dt_pin,
            GPIO.BOTH,
            callback=self._on_rotate,
            bouncetime=1,
        )

        # Watch button edges for press/release events.
        GPIO.add_event_detect(
            self.config.sw_pin,
            GPIO.BOTH,
            callback=self._on_button,
            bouncetime=40,
        )

    def _read_state(self) -> int:
        clk = GPIO.input(self.config.clk_pin)
        dt = GPIO.input(self.config.dt_pin)
        return (clk << 1) | dt

    def _on_rotate(self, _channel: int) -> None:
        current = self._read_state()
        delta = _TRANSITIONS.get((self._last_state, current), 0)
        self._last_state = current

        if delta == 0:
            return

        # Four micro-steps typically represent one detent on common encoders.
        self._accumulator += delta
        if abs(self._accumulator) >= 4:
            detents = int(self._accumulator / 4)
            self._accumulator -= detents * 4
            self.steps += detents
            direction = "CW" if detents > 0 else "CCW"
            print(f"[{self.config.name}] rotate {direction}  total_steps={self.steps}")

    def _on_button(self, _channel: int) -> None:
        # With pull-up wiring: LOW=pressed, HIGH=released.
        pressed = GPIO.input(self.config.sw_pin) == GPIO.LOW
        state = "PRESSED" if pressed else "RELEASED"
        print(f"[{self.config.name}] button {state}")


def main() -> int:
    encoders = [
        RotaryEncoder(EncoderConfig("Device A", clk_pin=27, dt_pin=22, sw_pin=17)),
        RotaryEncoder(EncoderConfig("Device B", clk_pin=6, dt_pin=13, sw_pin=5)),
    ]

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for enc in encoders:
        enc.setup()

    print("Listening for encoder/button events. Press Ctrl+C to exit.")

    stop = False

    def _handle_stop(_sig: int, _frame: object) -> None:
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, _handle_stop)
    signal.signal(signal.SIGTERM, _handle_stop)

    try:
        while not stop:
            time.sleep(0.2)
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up. Bye.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
