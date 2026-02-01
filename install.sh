#!/bin/bash

echo "Installing DC - Daily Calender..."
# Install necessary packages
sudo apt install python3 python3-pip

# Setup venv
sudo mkdir -p /opt/dc
sudo python3 -m venv /opt/dc/venv
sudo /opt/dc/venv/bin/pip install pillow

# Install dc
sudo curl -fsSLo /opt/dc/dc https://raw.githubusercontent.com/pptoolbox/dc/main/dc
sudo curl -fsSLo /opt/dc/dc-light.py https://raw.githubusercontent.com/pptoolbox/dc/main/dc-light.py
sudo curl -fsSLo /opt/dc/dc-dark.py https://raw.githubusercontent.com/pptoolbox/dc/main/dc-dark.py
sudo curl -fsSLo /opt/dc/DMMono-Medium.ttf https://github.com/googlefonts/dm-mono/raw/main/exports/DMMono-Medium.ttf
sudo curl -fsSLo /opt/dc/LICENSE https://raw.githubusercontent.com/pptoolbox/dc/main/LICENSE

# First run
sudo mkdir -p /usr/local/wallpapers
/opt/dc/dc

# Config autoupdate
mkdir -p ~/.config/systemd/user
echo "[Unit]
Description=Run dc.py once per day at first login

[Service]
Type=oneshot
ExecStart=/opt/dc/dc" >> ~/.config/systemd/user/dc.service

echo "[Unit]
Description=Daily dc.py run (first login triggers it)

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target" >> ~/.config/systemd/user/dc.timer

systemctl --user daemon-reload
systemctl --user enable --now dc.timer

echo "DC(Daily Calender) installed successfully.."
