#!/bin/bash
set -e

echo "Uninstalling DC - Daily Calendar..."

# Stop and disable systemd user timer/service if available
if command -v systemctl >/dev/null 2>&1; then
	systemctl --user stop dc.timer dc.service >/dev/null 2>&1 || true
	systemctl --user disable dc.timer dc.service >/dev/null 2>&1 || true
fi

# Remove systemd user unit files
rm -f ~/.config/systemd/user/dc.timer ~/.config/systemd/user/dc.service || true

# Reload user systemd daemon
if command -v systemctl >/dev/null 2>&1; then
	systemctl --user daemon-reload >/dev/null 2>&1 || true
fi

# Remove /opt/dc and its virtualenv
if [ -d /opt/dc ]; then
	sudo rm -rf /opt/dc
	echo "Removed /opt/dc"
else
	echo "/opt/dc not found"
fi

# Remove /usr/local/share/wallpapers if empty
if [ -d /usr/local/share/wallpapers ]; then
	sudo rm -r /usr/local/share/wallpapers/dc-*.png || true
	echo "Removed wallpapers installed by DC"
fi

echo "DC uninstalled."