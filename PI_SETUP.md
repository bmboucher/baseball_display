# Raspberry Pi Setup — Three SPI Panels (ST7796S)

Tested target: **Raspberry Pi OS Bookworm (64-bit, Lite)** on a Pi 4. The
display is three ST7796S SPI panels at 480×320 wired to one Pi, plus two
rotary encoders for input.

## 1. Hardware pinout (BCM numbering)

| Function              | BCM pin | Notes                                       |
|-----------------------|--------:|---------------------------------------------|
| SPI MOSI              | 10      | shared by all three panels (SPI0 MOSI)      |
| SPI MISO              | 9       | shared (often unused by display)            |
| SPI SCLK              | 11      | shared (SPI0 SCLK)                          |
| Panel 1 CS (left)     | 8       | SPI0 CE0                                    |
| Panel 2 CS (right)    | 7       | SPI0 CE1                                    |
| Panel 3 CS (diamond)  | 0       | software CS — needs an extra spidev overlay |
| LCD D/C (LCD_RS)      | 1       | shared by all three panels                  |
| LCD reset (LCD_RST)   | 5       | shared by all three panels                  |
| Backlight (LED)       | 25      | drives all three panels; HIGH = on          |
| X encoder switch      | 24      | rotary press → ENTER (click left)           |
| X encoder A (CLK)     | 22      | rotation → LEFT/RIGHT                       |
| X encoder B (DT)      | 23      |                                             |
| Y encoder switch      | 17      | rotary press → SPACE (click right)          |
| Y encoder A (CLK)     | 18      | rotation → UP/DOWN                          |
| Y encoder B (DT)      | 27      |                                             |

Encoders use the Pi's internal pull-ups (configured in `pi_input.py`); wire
the common pin to GND.

## 2. Base OS prep

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git
sudo raspi-config nonint do_spi 0   # enable SPI
```

Disable the HDMI console getty so it doesn't fight us for /dev/fb0:

```bash
sudo systemctl disable --now getty@tty1.service
```

(Optional, fully headless) disable the HDMI output entirely — saves ~25 mA:

```bash
sudo sh -c 'echo "hdmi_blanking=2" >> /boot/firmware/config.txt'
```

## 3. fbtft kernel driver + three framebuffer devices

`fbtft` ships with mainline Raspberry Pi OS kernels (no DKMS build needed).
We expose each panel as its own `/dev/fbN` node by adding device-tree
overlays to `/boot/firmware/config.txt`.

> The third panel uses `cs=2`, which is **not** a hardware SPI0 CE pin; we
> enable a software-chip-select overlay so kernel SPI treats GPIO0 as CS2.

Append to `/boot/firmware/config.txt`:

```ini
dtparam=spi=on

# Re-map SPI0 to use GPIO0 as a software CE2 in addition to CE0/CE1.
# This makes /dev/spidev0.0, /dev/spidev0.1 and /dev/spidev0.2 available
# with CS pins on GPIO8, GPIO7 and GPIO0 respectively.
dtoverlay=spi0-3cs,cs0_pin=8,cs1_pin=7,cs2_pin=0

# Panel 1 (left)  — SPI0 CE0 / GPIO8
dtoverlay=fbtft,spi0-0,name=fb_st7796s,width=480,height=320,rotate=0,bgr=1,fps=30,speed=32000000,dc_pin=1,reset_pin=5,led_pin=25

# Panel 2 (right) — SPI0 CE1 / GPIO7
dtoverlay=fbtft,spi0-1,name=fb_st7796s,width=480,height=320,rotate=0,bgr=1,fps=30,speed=32000000,dc_pin=1,reset_pin=5

# Panel 3 (diamond) — SPI0 CE2 / GPIO0
dtoverlay=fbtft,spi0-2,name=fb_st7796s,width=480,height=320,rotate=0,bgr=1,fps=30,speed=32000000,dc_pin=1,reset_pin=5
```

Notes:
- Only the first overlay declares `led_pin`. The kernel driver toggles that
  GPIO as backlight; declaring it in all three would try to claim GPIO25 three
  times.
- `bgr=1` swaps red/blue if the panel's color order is BGR. Flip if colors
  look wrong.
- `speed=32000000` (32 MHz) is conservative; many ST7796S boards run at
  48–64 MHz. Raise it once everything is working.
- `rotate=0/90/180/270` if a panel needs to be rotated in hardware.

Reboot, then verify all three framebuffer devices appear:

```bash
sudo reboot
# after login:
ls -l /dev/fb*
#   crw-rw---- 1 root video 29, 0 ... /dev/fb0   ← HDMI / KMS (ignored)
#   crw-rw---- 1 root video 29, 1 ... /dev/fb1   ← left
#   crw-rw---- 1 root video 29, 2 ... /dev/fb2   ← right
#   crw-rw---- 1 root video 29, 3 ... /dev/fb3   ← diamond

fbset -fb /dev/fb1   # should print 480x320, 16 bpp
```

Quick sanity check — paint each panel white:

```bash
sudo sh -c 'cat /dev/urandom > /dev/fb1' & sleep 0.3; kill %1
sudo sh -c 'cat /dev/urandom > /dev/fb2' & sleep 0.3; kill %1
sudo sh -c 'cat /dev/urandom > /dev/fb3' & sleep 0.3; kill %1
```

If any panel stays blank: re-check the wiring for that CS pin and DC/RST,
verify it shows up in `dmesg | grep fb_st7796s`, and try lowering `speed`.

## 4. Install the application

```bash
git clone <repo-url> ~/baseball_display
cd ~/baseball_display
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[raspberry-pi]'    # the extra pulls in RPi.GPIO
```

Add your user to the `video`, `gpio`, and `spi` groups so the service can
write to `/dev/fbN` and toggle GPIO without root:

```bash
sudo usermod -aG video,gpio,spi $USER
# log out and back in for group changes to take effect
```

## 5. Configure baseball_display for multi-process + framebuffer output

Create `~/baseball_display/settings.json`:

```json
{
  "refresh_rate": 10,
  "multi_process": true,
  "screen_fbdevs": {
    "left":    "/dev/fb1",
    "right":   "/dev/fb2",
    "diamond": "/dev/fb3"
  }
}
```

(Each child sets `SDL_VIDEODRIVER=fbcon` + `SDL_FBDEV=<path>` before
`pygame.init()` — see `multiproc.py:_render_worker`.)

Env-var overrides are also honored, useful for ad-hoc testing without
editing the JSON:

```bash
export BASEBALL_DISPLAY_MULTI_PROCESS=1
export BASEBALL_DISPLAY_FBDEV_LEFT=/dev/fb1
export BASEBALL_DISPLAY_FBDEV_RIGHT=/dev/fb2
export BASEBALL_DISPLAY_FBDEV_DIAMOND=/dev/fb3
```

Run it manually first to verify:

```bash
cd ~/baseball_display
source .venv/bin/activate
python -m baseball_display
```

You should see logs like:

```
Multi-process mode enabled
Pi GPIO input enabled: X encoder -> LEFT/RIGHT + RETURN, Y encoder -> UP/DOWN + SPACE
Pi GPIO input adapter active; parent runs without pygame
Spawned render child left (pid=…, fbdev=/dev/fb1)
Spawned render child right (pid=…, fbdev=/dev/fb2)
Spawned render child diamond (pid=…, fbdev=/dev/fb3)
```

…and the three panels light up. Twist the encoders to navigate.

If a panel stays black but logs show "Spawned render child …":
- It usually means `SDL_VIDEODRIVER=fbcon` isn't supported in your pygame's
  bundled SDL. Run `python -c "import pygame; pygame.init(); import os; os.environ['SDL_VIDEODRIVER']='fbcon'; print(pygame.display.get_driver())"`.
- If `fbcon` isn't available, the simplest fix is `sudo apt install python3-pygame` to use the system pygame (which is built against the system SDL with fbcon), and recreate the venv with `--system-site-packages`.

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
# fbcon driver needs raw framebuffer access; user is in `video`+`gpio`+`spi`
# groups so root is not required.
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

Stop / restart for development:

```bash
sudo systemctl stop baseball-display.service
sudo systemctl restart baseball-display.service
```

## 7. Troubleshooting cheatsheet

| Symptom                                        | Likely cause / fix                                                      |
|------------------------------------------------|--------------------------------------------------------------------------|
| `/dev/fb1` etc. missing                        | `dmesg \| grep fb_st7796s` for driver errors; recheck `config.txt` overlays |
| One panel blank, others fine                   | Wrong CS pin or DC/RST not wired; `dmesg` should show timeout / NACK     |
| Colors swapped (red↔blue)                      | Flip `bgr=1` on the affected overlay                                     |
| Tearing / flicker                              | Drop `speed=` (32 MHz → 24 MHz) or `fps=` (30 → 20)                      |
| Encoders backwards                             | Swap `clk_pin` / `dt_pin` for that encoder in `pi_input.py`              |
| `Permission denied` on `/dev/fb1`              | User not in `video` group; `groups` should list it                       |
| Service starts before HDMI gone, screen tears  | Add `After=getty@tty1.service` and ensure that getty is disabled         |
| Render child dies on startup                   | Run manually with `journalctl -u baseball-display -n 200`; usually a missing pygame/SDL driver |

## 8. Updating the app

```bash
cd ~/baseball_display
git pull
sudo systemctl restart baseball-display.service
```
