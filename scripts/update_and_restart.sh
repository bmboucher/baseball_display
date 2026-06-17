#!/usr/bin/env bash
# Pull baseball_display from origin and restart the systemd service if
# HEAD actually moved. If pyproject.toml is one of the changed files,
# also re-run `pip install -e .` in the venv before restarting.
#
# Designed to run from /etc/cron.d/ as root. See PI_SETUP.md §9.
#
# Usage:
#   update_and_restart.sh [REPO_DIR] [SERVICE_NAME]
# Defaults:
#   REPO_DIR=/home/pi/baseball_display
#   SERVICE_NAME=baseball-display.service

set -euo pipefail

REPO_DIR=${1:-/home/pi/baseball_display}
SERVICE_NAME=${2:-baseball-display.service}
VENV_PIP="$REPO_DIR/.venv/bin/pip"

log() {
    logger -t baseball-display-update "$@"
    echo "$@" >&2
}

cd "$REPO_DIR"

# Determine the repo owner so `git pull` runs as that user (avoids
# polluting the working tree with root-owned files).
REPO_USER=$(stat -c '%U' "$REPO_DIR/.git")

old_head=$(sudo -u "$REPO_USER" git rev-parse HEAD)
if ! sudo -u "$REPO_USER" git pull --ff-only --quiet; then
    log "git pull failed; leaving $SERVICE_NAME alone"
    exit 1
fi
new_head=$(sudo -u "$REPO_USER" git rev-parse HEAD)

if [ "$old_head" = "$new_head" ]; then
    log "no changes (HEAD=$old_head); skipping restart"
    exit 0
fi

log "updated $old_head -> $new_head"

# If dependencies changed, refresh the venv before restarting so the
# service comes up with the new wheel set.
if sudo -u "$REPO_USER" git diff --name-only "$old_head" "$new_head" \
        | grep -qE '^(pyproject\.toml|setup\.py|setup\.cfg)$'; then
    log "pyproject.toml/setup files changed; running pip install -e .[raspberry-pi]"
    sudo -u "$REPO_USER" "$VENV_PIP" install -e "$REPO_DIR"'[raspberry-pi]' --quiet
fi

log "restarting $SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
