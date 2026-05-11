"""Pure-Python driver for the ST7796S 480x320 SPI display.

Why this exists: the kernel's ``fb_ili9486`` driver gets ST7796S panels as
far as "display on, framebuffer cleared" but doesn't issue the vendor-
specific Command-Set Control (CSCON, ``0xF0``) sequence that ST7796S
requires before subsequent pixel writes are accepted. With this driver
each render child takes its rendered pygame Surface, converts it to
RGB565, and ships it directly over SPI — bypassing the kernel framebuffer
entirely.

Three panels share one SPI bus (MOSI/MISO/SCLK) plus shared DC, RST and
backlight pins; each has its own chip-select GPIO. Cross-process bus +
shared-pin contention is managed by an ``mp.Lock`` (per render frame).

Hardware constants live in ``settings.py``'s ``PanelConfig``; this module
only knows how to drive one panel given its config and a GPIO handle.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ContextManager, Optional

logger = logging.getLogger(__name__)


_SPIDEV_BUFSIZ_FILE = Path("/sys/module/spidev/parameters/bufsiz")
_DEFAULT_BUFSIZ = 4096


def _read_spidev_bufsiz() -> int:
    """Read spidev's max transfer size. We must split writes at this boundary
    because writebytes2 toggles CS between blocks larger than bufsiz, and
    ST7796S treats that as the end of a RAMWR sequence."""
    try:
        return int(_SPIDEV_BUFSIZ_FILE.read_text().strip())
    except Exception:
        return _DEFAULT_BUFSIZ


@dataclass(frozen=True)
class PanelConfig:
    """Per-screen panel wiring + bus settings.

    ``cs_pin`` is the only GPIO that differs between panels; ``dc_pin``,
    ``rst_pin`` and ``led_pin`` are shared across all three panels by the
    Pi wiring. ``led_pin`` should only be populated on one panel's config
    (whichever one's the "owner") so the others don't try to re-claim it.
    """

    name: str  # "left" | "right" | "diamond"
    cs_pin: int  # BCM, e.g. 8 / 7 / 0
    dc_pin: int = 1
    rst_pin: int = 5
    led_pin: Optional[int] = None  # set only on one panel; None on others
    spi_bus: int = 0
    spi_device: int = 0
    spi_hz: int = 16_000_000
    width: int = 480
    height: int = 320
    rotation: int = 0  # 0/90/180/270 — applied via MADCTL
    bgr: bool = True  # if False, RGB order


# ST7796S MADCTL bits.
_MADCTL_MY = 0x80
_MADCTL_MX = 0x40
_MADCTL_MV = 0x20
_MADCTL_ML = 0x10
_MADCTL_BGR = 0x08

# Commands.
_CMD_SWRESET = 0x01
_CMD_SLPOUT = 0x11
_CMD_NORON = 0x13
_CMD_INVOFF = 0x20
_CMD_INVON = 0x21
_CMD_DISPOFF = 0x28
_CMD_DISPON = 0x29
_CMD_CASET = 0x2A
_CMD_RASET = 0x2B
_CMD_RAMWR = 0x2C
_CMD_MADCTL = 0x36
_CMD_COLMOD = 0x3A
_CMD_CSCON = 0xF0  # Command-Set Control (unlocks vendor commands)


def _madctl_for_rotation(rotation: int, bgr: bool) -> int:
    base = _MADCTL_BGR if bgr else 0
    if rotation == 0:
        return base | _MADCTL_MX
    if rotation == 90:
        return base | _MADCTL_MV
    if rotation == 180:
        return base | _MADCTL_MY
    if rotation == 270:
        return base | _MADCTL_MX | _MADCTL_MY | _MADCTL_MV
    raise ValueError(f"rotation must be 0/90/180/270, got {rotation}")


class _NullLock:
    def __enter__(self) -> "_NullLock":
        return self

    def __exit__(self, *args: Any) -> None:
        pass


class ST7796S:
    """One panel. Owns its CS pin; coordinates shared pins via *lock*."""

    def __init__(
        self,
        config: PanelConfig,
        gpio: Any,
        spi: Any,
        lock: Optional[ContextManager[Any]] = None,
        spi_bufsiz: Optional[int] = None,
    ) -> None:
        self.config = config
        self._gpio = gpio
        self._spi = spi
        self._lock = lock if lock is not None else _NullLock()
        self._bufsiz = spi_bufsiz if spi_bufsiz is not None else _read_spidev_bufsiz()
        # Rows per ioctl, computed so a single writebytes2 call stays within
        # spidev's bufsiz and therefore doesn't toggle CS mid-transfer.
        bytes_per_row = config.width * 2
        self._rows_per_chunk = max(1, self._bufsiz // bytes_per_row)

        gpio.setup(config.cs_pin, gpio.OUT, initial=gpio.HIGH)
        gpio.setup(config.dc_pin, gpio.OUT, initial=gpio.LOW)
        gpio.setup(config.rst_pin, gpio.OUT, initial=gpio.HIGH)
        if config.led_pin is not None:
            gpio.setup(config.led_pin, gpio.OUT, initial=gpio.HIGH)

    # ---- low-level transport ----

    def _select(self, on: bool) -> None:
        self._gpio.output(self.config.cs_pin, self._gpio.LOW if on else self._gpio.HIGH)

    def _set_dc(self, data: bool) -> None:
        self._gpio.output(self.config.dc_pin, self._gpio.HIGH if data else self._gpio.LOW)

    def _write_cmd(self, cmd: int) -> None:
        self._set_dc(False)
        self._select(True)
        self._spi.writebytes([cmd])
        self._select(False)

    def _write_data(self, data: Any) -> None:
        self._set_dc(True)
        self._select(True)
        if isinstance(data, (bytes, bytearray, memoryview)):
            self._spi.writebytes2(data)
        else:
            self._spi.writebytes(list(data))
        self._select(False)

    # ---- public API ----

    def reset(self) -> None:
        """Hardware reset. RST is shared, so this resets all panels on the bus."""
        rst = self.config.rst_pin
        self._gpio.output(rst, self._gpio.HIGH)
        time.sleep(0.005)
        self._gpio.output(rst, self._gpio.LOW)
        time.sleep(0.020)
        self._gpio.output(rst, self._gpio.HIGH)
        time.sleep(0.150)

    def init(self) -> None:
        """Send the ST7796S-specific init sequence under the bus lock."""
        cfg = self.config
        c, d = self._write_cmd, self._write_data
        with self._lock:
            c(_CMD_SWRESET)
            time.sleep(0.120)
            c(_CMD_SLPOUT)
            time.sleep(0.120)

            # Unlock vendor commands (the bit fb_ili9486 doesn't do).
            c(_CMD_CSCON); d([0xC3])
            c(_CMD_CSCON); d([0x96])

            c(_CMD_MADCTL); d([_madctl_for_rotation(cfg.rotation, cfg.bgr)])
            c(_CMD_COLMOD); d([0x55])  # 16bpp RGB565

            # Display function / inversion / frame rate — values from datasheet.
            c(0xB4); d([0x01])           # DIC: 1-dot inversion
            c(0xB6); d([0x80, 0x02, 0x3B])
            c(0xB7); d([0xC6])           # Entry mode set
            c(0xC0); d([0xF0, 0x35])     # PWR1
            c(0xC1); d([0x06])           # PWR2
            c(0xC2); d([0xA7])           # PWR3
            c(0xC5); d([0x18])           # VCOM control
            time.sleep(0.120)

            # Gamma — generic values that work for most ST7796S panels.
            c(0xE0); d([0xF0, 0x09, 0x0B, 0x06, 0x04, 0x15, 0x2F, 0x54,
                        0x42, 0x3C, 0x17, 0x14, 0x18, 0x1B])
            c(0xE1); d([0xF0, 0x09, 0x0B, 0x06, 0x04, 0x03, 0x2D, 0x43,
                        0x42, 0x3B, 0x16, 0x14, 0x17, 0x1B])
            time.sleep(0.120)

            # Re-lock vendor commands.
            c(_CMD_CSCON); d([0x3C])
            c(_CMD_CSCON); d([0x69])
            time.sleep(0.120)

            c(_CMD_NORON)
            time.sleep(0.010)
            c(_CMD_DISPON)
            time.sleep(0.020)
        logger.info("ST7796S[%s] init complete", cfg.name)

    def _set_window(self, x0: int, y0: int, x1: int, y1: int) -> None:
        self._write_cmd(_CMD_CASET)
        self._write_data([(x0 >> 8) & 0xFF, x0 & 0xFF, (x1 >> 8) & 0xFF, x1 & 0xFF])
        self._write_cmd(_CMD_RASET)
        self._write_data([(y0 >> 8) & 0xFF, y0 & 0xFF, (y1 >> 8) & 0xFF, y1 & 0xFF])
        self._write_cmd(_CMD_RAMWR)

    def _blit_rows(self, pixel_bytes: bytes) -> None:
        """Push ``pixel_bytes`` (RGB565-BE, exactly width*height*2 bytes) to
        the panel, splitting into row-aligned chunks that each fit in one
        spidev ioctl. Each chunk has its own CASET/RASET/RAMWR so the chip
        knows exactly where it lands and CS-toggling between ioctls is benign.
        """
        w = self.config.width
        h = self.config.height
        bytes_per_row = w * 2
        expected = bytes_per_row * h
        if len(pixel_bytes) != expected:
            raise ValueError(
                f"pixel_bytes len {len(pixel_bytes)} != expected {expected}"
            )

        rows_per_chunk = self._rows_per_chunk
        with self._lock:
            offset = 0
            row = 0
            while row < h:
                chunk_rows = min(rows_per_chunk, h - row)
                chunk_bytes = chunk_rows * bytes_per_row
                self._set_window(0, row, w - 1, row + chunk_rows - 1)
                self._set_dc(True)
                self._select(True)
                self._spi.writebytes2(pixel_bytes[offset:offset + chunk_bytes])
                self._select(False)
                row += chunk_rows
                offset += chunk_bytes

    def display(self, surface: Any) -> None:
        """Push the entire *surface* (a pygame.Surface) to the panel.

        Surface must be ``width × height`` in 24/32-bit pixel format. The
        method converts to big-endian RGB565 and ships it via row-aligned
        SPI chunks (each within spidev's bufsiz).
        """
        rgb565 = _surface_to_rgb565_be(surface)
        self._blit_rows(rgb565)

    def fill(self, rgb565_be: bytes) -> None:
        """Fill the panel with a solid color (used for smoke tests / blank)."""
        w = self.config.width
        h = self.config.height
        if len(rgb565_be) == 2:
            buf = rgb565_be * (w * h)
        else:
            buf = rgb565_be
        self._blit_rows(buf)


# ---- pygame → RGB565 conversion (numpy fast-path with pure-python fallback) ----


def _surface_to_rgb565_be(surface: Any) -> bytes:
    """Convert a pygame.Surface to big-endian RGB565 bytes for the panel."""
    try:
        import numpy as np  # local import so non-Pi environments don't need it
        import pygame  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "ST7796S.display requires numpy and pygame on the Pi"
        ) from e

    raw = pygame.image.tobytes(surface, "RGB")
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
    r = arr[:, 0].astype(np.uint16)
    g = arr[:, 1].astype(np.uint16)
    b = arr[:, 2].astype(np.uint16)
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    # ST7796S in 16bpp expects high byte first on the wire.
    return rgb565.astype(">u2").tobytes()


def open_spi(bus: int = 0, device: int = 0, hz: int = 16_000_000) -> Any:
    """Open the SPI bus with hardware CS disabled (we manage all three CS pins manually)."""
    import spidev  # local import — only available on Pi

    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = hz
    spi.mode = 0
    try:
        spi.no_cs = True
    except (OSError, AttributeError):
        logger.warning(
            "spidev.no_cs not supported; the kernel will toggle CE%d on every "
            "transfer — that's fine as long as no panel is wired to that pin.",
            device,
        )
    logger.info(
        "Opened /dev/spidev%d.%d at %d Hz (spidev bufsiz=%d)",
        bus,
        device,
        hz,
        _read_spidev_bufsiz(),
    )
    return spi
