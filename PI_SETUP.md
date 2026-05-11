# Raspberry Pi Setup — Three SPI Panels (ST7796S)

Tested target: **Raspberry Pi OS Bookworm (64-bit, Lite)** on a Pi 4. Three
ST7796S 480×320 SPI panels share one SPI bus with separate chip selects,
plus two rotary encoders for input.

This setup uses a **pure-Python ST7796S driver** (see
`baseball_display/st7796s.py`) rather than the kernel `fbtft` framebuffer.
Reasons: stock Pi OS kernels don't ship an `fb_st7796s` driver and
`fb_ili9486` doesn't issue the vendor `CSCON` command ST7796S panels need
to accept pixel writes. Driving SPI from Python lets us send the correct
init sequence and sidesteps the kernel-overlay rabbit hole entirely.

## 1. Hardware pinout (BCM numbering)

| Function              | BCM pin | Notes                                                |
|-----------------------|--------:|------------------------------------------------------|
| SPI MOSI              | 10      | shared by all three panels (SPI0 MOSI)               |
| SPI MISO              | 9       | shared (often unused by display)                     |
| SPI SCLK              | 11      | shared (SPI0 SCLK)                                   |
| Panel 1 CS (left)     | 8       | manually driven by the Python driver                 |
| Panel 2 CS (right)    | 7       | manually driven by the Python driver                 |
| Panel 3 CS (diamond)  | 0       | manually driven by the Python driver                 |
| LCD D/C (LCD_RS)      | 1       | shared by all three panels                           |
| LCD reset (LCD_RST)   | 5       | shared; the parent pulses it once at startup         |
| Backlight (LED)       | 25      | shared backlight; driven HIGH at startup             |
| X encoder switch      | 24      | rotary press → ENTER (click left)                    |
| X encoder A (CLK)     | 22      | rotation → LEFT/RIGHT                                |
| X encoder B (DT)      | 23      |                                                      |
| Y encoder switch      | 17      | rotary press → SPACE (click right)                   |
| Y encoder A (CLK)     | 18      | rotation → UP/DOWN                                   |
| Y encoder B (DT)      | 27      |                                                      |

Encoders use the Pi's internal pull-ups; wire each encoder's common pin to GND.

## 2. Base OS prep

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git
# Build deps for rpi-lgpio's underlying lgpio C extension (no prebuilt
# wheel on PyPI for aarch64). Skipping these makes the later
# `pip install` fail with "command 'swig' failed: No such file or directory".
sudo apt install -y swig python3-dev liblgpio-dev
sudo raspi-config nonint do_spi 0   # enable SPI
```

Disable the HDMI console getty (cleaner boot, frees the framebuffer):

```bash
sudo systemctl disable --now getty@tty1.service
```

(Optional, fully headless) disable HDMI output entirely:

```bash
sudo sh -c 'echo "hdmi_blanking=2" >> /boot/firmware/config.txt'
```

## 3. Enable SPI — that's it

`/boot/firmware/config.txt` only needs **one** display-related line for
this setup. **Make sure there are no leftover `dtoverlay=fbtft…`,
`dtoverlay=piscreen…`, `dtoverlay=mhs35…`, or `dtoverlay=baseball-…`
lines from earlier troubleshooting** — those would steal the SPI bus or
wrongly init the panels. The relevant tail of `config.txt` should look
like:

```ini
[all]
enable_uart=1
hdmi_blanking=2

dtparam=spi=on
```

Reboot if you changed anything, then verify:

```bash
ls /dev/spidev*    # should show /dev/spidev0.0 and /dev/spidev0.1
```

Raise the spidev kernel module's max transfer size so we can ship 300 KiB
frames in a single write (default is 4096 bytes):

```bash
# Make the change permanent
echo "options spidev bufsiz=65536" | sudo tee /etc/modprobe.d/spidev.conf
# Apply now without reboot
sudo modprobe -r spidev && sudo modprobe spidev
cat /sys/module/spidev/parameters/bufsiz   # should print 65536
```

## 4. Install the application

```bash
git clone <repo-url> ~/baseball_display
cd ~/baseball_display
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[raspberry-pi]'    # pulls rpi-lgpio + spidev + numpy
```

If your `.venv` already had the old `RPi.GPIO` package, uninstall it first
so `rpi-lgpio` can provide the `RPi.GPIO` module instead. On modern Pi OS
kernels, the legacy `RPi.GPIO` can't register edge-detect callbacks and
rotary encoders end up using a laggy polling fallback.

```bash
pip uninstall -y RPi.GPIO
pip install -e '.[raspberry-pi]'
```

Add your user to `gpio` and `spi` so the service can drive pins and the
SPI bus without root:

```bash
sudo usermod -aG gpio,spi $USER
# log out and back in for group changes to take effect
```

## 5. Configure multi-process mode

Create `~/baseball_display/settings.json`:

```json
{
  "refresh_rate": 10,
  "multi_process": true
}
```

The default panel wiring (matching the table above) is baked into
`settings.py` — you only need to override `panels` in JSON if your wiring
differs. Example for swapping rotation on the left panel:

```json
{
  "multi_process": true,
  "panels": {
    "left":    { "cs_pin": 8, "led_pin": 25, "rotation": 180 },
    "right":   { "cs_pin": 7 },
    "diamond": { "cs_pin": 0 }
  }
}
```

Test manually:

```bash
cd ~/baseball_display
source .venv/bin/activate
python -m baseball_display
```

Expected log lines:

```
Multi-process mode enabled
Initialized panel 'left'    on CS=GPIO8
Initialized panel 'right'   on CS=GPIO7
Initialized panel 'diamond' on CS=GPIO0
Pi GPIO input enabled: X encoder -> LEFT/RIGHT + RETURN, Y encoder -> UP/DOWN + SPACE
Pi GPIO input adapter active; parent runs without pygame
Spawned render child left (pid=…, cs_pin=8)
Spawned render child right (pid=…, cs_pin=7)
Spawned render child diamond (pid=…, cs_pin=0)
Starting parent loop...
```

…and all three panels should light up with the actual scoreboard content.
Twist the encoders to navigate menus.

## 6. Auto-start on boot via systemd

Create `/etc/systemd/system/baseball-display.service`:

```ini
[Unit]
Description=Baseball Display (three-panel SPI jumbotron)
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/baseball_display
Environment=BASEBALL_DISPLAY_MULTI_PROCESS=1
ExecStart=/home/pi/baseball_display/.venv/bin/python -m baseball_display
Restart=on-failure
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

(Replace `pi` with your actual username if different.)

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now baseball-display.service
journalctl -u baseball-display.service -f
```

Stop / restart during development:

```bash
sudo systemctl stop baseball-display.service
sudo systemctl restart baseball-display.service
```

## 7. Troubleshooting

| Symptom                                       | Likely cause / fix                                                                          |
|-----------------------------------------------|---------------------------------------------------------------------------------------------|
| `Permission denied: '/dev/spidev0.0'`         | User not in `spi` group; `groups` should list it. Log out/in after `usermod`.               |
| All panels blank / white                      | Backlight on GPIO25 not toggled HIGH — wiring issue, or `led_pin` not declared on a panel.  |
| One panel works, others blank                 | Verify wiring of the broken panel's CS GPIO to the correct line in section 1.               |
| Panel showing garbled / wrong colors          | Try `"bgr": false` in that panel's JSON, or different `rotation` values (0/90/180/270).     |
| `spidev.writebytes2: Argument list too long`  | bufsiz still 4096; redo step 3's modprobe edit + reload, confirm `/sys/.../bufsiz` is 65536. |
| Encoders backwards                            | Swap `clk_pin`/`dt_pin` for that encoder in `pi_input.py`.                                  |
| Render child dies on startup                  | `journalctl -u baseball-display -n 200` — usually a missing module or wrong settings.json.  |
| Two children fight for the bus (slow / tear)  | Confirm `spi_lock` is being shared (default). Don't disable it manually.                    |

## 8. How rendering works (so debug is easier)

- Parent process owns input + state + MLB HTTP. It does **not** init pygame and does **not** touch SPI in the steady-state loop (it only does the one-time panel reset + init at startup).
- Three child processes each render one panel:
  - `SDL_VIDEODRIVER=dummy` → pygame draws to an off-screen 480×320 surface, no window.
  - After each draw, the child converts the surface to big-endian RGB565 with numpy and ships it as one ~300 KiB SPI burst via `spidev.writebytes2`.
  - A shared `multiprocessing.Lock` serializes SPI bus + shared-GPIO access across the three children. Default clock is 16 MHz (the practical ceiling on three-panel breadboard fanout — above ~20 MHz the shared MOSI line shows bit errors and panels render noise). Each 480×320 frame is ~150 µs at 16 MHz, so 30 fps × 3 panels is still <2% bus utilization.
- The publish/subscribe model from `multiproc.py` is unchanged from the previous fbtft version: parent publishes a pickled snapshot when state changes; children fetch on version bump.

## 9. Updating the app

Manually:

```bash
cd ~/baseball_display
git pull
sudo systemctl restart baseball-display.service
```

### Automatic nightly self-update

`scripts/update_and_restart.sh` pulls `origin/main`, checks whether HEAD
moved, optionally re-runs `pip install -e .` if `pyproject.toml` changed,
and restarts the systemd service. Designed to run from cron as root.

```bash
# Make the script executable
chmod +x ~/baseball_display/scripts/update_and_restart.sh

# Install the cron job to run daily at 02:00 America/New_York
sudo tee /etc/cron.d/baseball-display-update > /dev/null <<'EOF'
# Pull baseball_display from origin and restart the service if HEAD moves.
# Times are interpreted in the CRON_TZ below; New York handles EST/EDT correctly.
CRON_TZ=America/New_York
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

0 2 * * * root /home/pi/baseball_display/scripts/update_and_restart.sh >> /var/log/baseball-display-update.log 2>&1
EOF

# Reload cron's view of /etc/cron.d
sudo systemctl reload cron
```

(Replace `/home/pi/baseball_display` with your actual repo path if
different.)

The script logs to syslog with tag `baseball-display-update`, so you can
follow what it's been doing with:

```bash
sudo journalctl -t baseball-display-update -f
```

Or check the file log:

```bash
sudo tail -f /var/log/baseball-display-update.log
```

To test it without waiting until 2 AM:

```bash
sudo /home/pi/baseball_display/scripts/update_and_restart.sh
```

Notes:

- The `git pull` runs as the repo's owning user (auto-detected via `stat`)
  so the working tree doesn't end up with root-owned files. Only the
  `systemctl restart` call actually needs root.
- If `git pull` fails (uncommitted local changes, conflicts, network
  hiccup), the script logs and exits without restarting — the service
  stays up on the old code.
- The service's `Restart=on-failure` handles the case where the new code
  is broken and crashes on boot: systemd will keep retrying.
