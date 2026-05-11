#!/usr/bin/env python3
"""Bench-test the three ST7796S SPI panels directly.

Initializes all three panels, then fills each one in turn with a
sequence of solid colors so you can verify:

- Which physical panel responds to each CS pin (left=GPIO8, right=GPIO7,
  diamond=GPIO0). If the wrong panel lights up, you've got crossed wiring.
- Whether color names match the display (e.g., RED looking red, not blue).
  If red and blue are swapped, flip ``bgr`` in settings.json.
- Whether CS gating is actually working. If ALL panels respond to ANY
  panel's fill call, ``spi.no_cs`` isn't being honored by this kernel —
  see the troubleshooting section in PI_SETUP.md.
- Whether each panel fills the WHOLE screen, not just a corner. If a
  panel only fills a small square, the rotation / MADCTL settings need
  tweaking.

Pi-only. Imports RPi.GPIO at module load, so do not run on desktop.

Usage:
    python -m baseball_display  # must not be running concurrently
    python scripts/panel_test.py
"""

from __future__ import annotations

import time

import RPi.GPIO as gpio  # type: ignore[import-not-found]

from baseball_display.st7796s import PanelConfig, ST7796S, open_spi


# Wiring per PI_SETUP.md. Override here if your wiring differs.
PANEL_CONFIGS = [
    PanelConfig(name="left",    cs_pin=8, led_pin=25, rotation=270),
    PanelConfig(name="right",   cs_pin=7,             rotation=270),
    PanelConfig(name="diamond", cs_pin=0,             rotation=270),
]

# RGB565 big-endian color words.
COLORS: list[tuple[str, bytes]] = [
    ("RED",   b"\xf8\x00"),
    ("GREEN", b"\x07\xe0"),
    ("BLUE",  b"\x00\x1f"),
    ("WHITE", b"\xff\xff"),
    ("BLACK", b"\x00\x00"),
]

DWELL_SECONDS = 0.8


def main() -> None:
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    spi = open_spi(bus=0, device=0, hz=40_000_000)
    panels = [ST7796S(cfg, gpio, spi) for cfg in PANEL_CONFIGS]

    # RST is shared, so one panel issues the pulse and all three reset together.
    panels[0].reset()
    for p in panels:
        p.init()
        print(f"  inited {p.config.name} (CS=GPIO{p.config.cs_pin})")

    print()
    print("Filling each panel with each color. Watch which physical panel reacts.")
    print()

    for color_name, color_word in COLORS:
        for panel in panels:
            print(f"  {panel.config.name:<8} -> {color_name}")
            panel.fill(color_word)
            time.sleep(DWELL_SECONDS)

    print()
    print("done — leaving panels on last color (BLACK)")


if __name__ == "__main__":
    main()
