"""Thin wrapper around `nmcli` for wifi scan + connect.

NetworkManager ships by default on Raspberry Pi OS Bookworm
(see PI_SETUP.md), so `nmcli` is available on every supported
deployment target. On any non-Linux host (or any host without
`nmcli` installed) the public functions either no-op or return an
empty/failure value so callers don't need platform checks.

All subprocess calls pass arguments as a list (never `shell=True`) so
SSIDs and passwords containing shell metacharacters are safe.
"""

from __future__ import annotations

import logging
import platform
import shutil
import subprocess

logger = logging.getLogger(__name__)

_SCAN_TIMEOUT_SEC = 15
_CONNECT_TIMEOUT_SEC = 30


def is_available() -> bool:
    """True iff we're on Linux and `nmcli` is on PATH."""
    return platform.system() == "Linux" and shutil.which("nmcli") is not None


def scan_ssids() -> list[tuple[str, int, str]]:
    """Return nearby wifi networks as `(ssid, signal_pct, security)`.

    Deduped by SSID (keeping the highest-signal entry). Empty SSIDs
    (hidden networks) are dropped. Returns `[]` on any failure.
    """
    if not is_available():
        return []
    try:
        result = subprocess.run(
            [
                "nmcli", "-t", "-e", "no",
                "-f", "SSID,SIGNAL,SECURITY",
                "device", "wifi", "list", "--rescan", "auto",
            ],
            capture_output=True,
            text=True,
            timeout=_SCAN_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        logger.warning("nmcli wifi scan timed out after %ss", _SCAN_TIMEOUT_SEC)
        return []
    except OSError:
        logger.exception("nmcli wifi scan failed to launch")
        return []

    if result.returncode != 0:
        logger.warning("nmcli wifi scan exit=%s stderr=%s", result.returncode, result.stderr.strip())
        return []

    # -t terse mode separates fields with `:`. Colons inside fields are
    # backslash-escaped by nmcli; split on unescaped colons.
    by_ssid: dict[str, tuple[int, str]] = {}
    for line in result.stdout.splitlines():
        fields = _split_terse(line)
        if len(fields) < 3:
            continue
        ssid, signal_raw, security = fields[0], fields[1], fields[2]
        if not ssid:
            continue
        try:
            signal = int(signal_raw)
        except ValueError:
            signal = 0
        prev = by_ssid.get(ssid)
        if prev is None or signal > prev[0]:
            by_ssid[ssid] = (signal, security or "--")

    return sorted(
        ((ssid, sig, sec) for ssid, (sig, sec) in by_ssid.items()),
        key=lambda row: row[1],
        reverse=True,
    )


def connect(ssid: str, password: str) -> tuple[bool, str]:
    """Apply `(ssid, password)` via `nmcli`. Returns `(ok, message)`.

    Creates (or reuses) a NetworkManager connection profile, so the
    credentials persist across reboots automatically.
    """
    if not is_available():
        return (False, "WiFi config requires Linux/NetworkManager")
    if not ssid:
        return (False, "SSID is empty")

    args = ["nmcli", "device", "wifi", "connect", ssid]
    if password:
        args += ["password", password]
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=_CONNECT_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        return (False, f"Timed out after {_CONNECT_TIMEOUT_SEC}s")
    except OSError as exc:
        return (False, f"nmcli launch failed: {exc}")

    if result.returncode == 0:
        return (True, f"Connected: {ssid}")
    # nmcli's useful error message is usually on stderr, sometimes stdout.
    msg = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
    # Trim NetworkManager's noisy prefix to keep the line short on screen.
    msg = msg.replace("Error: ", "")
    return (False, msg)


def _split_terse(line: str) -> list[str]:
    """Split an `nmcli -t` line on unescaped `:` separators."""
    fields: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            buf.append(line[i + 1])
            i += 2
            continue
        if ch == ":":
            fields.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    fields.append("".join(buf))
    return fields
