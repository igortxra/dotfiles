#!/usr/bin/env python3

import pyudev
import subprocess
import os

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('input')

for device in iter(monitor.poll, None):
    if device.action == 'add' and device.properties.get('ID_INPUT_KEYBOARD') == '1':
        env = os.environ.copy()
        env['DISPLAY'] = ':0'
        env['XAUTHORITY'] = os.path.expanduser('~/.Xauthority')
        subprocess.run(['setxkbmap', '-option', 'caps:super'], env=env)
        subprocess.run(['dunstify', 'Keyboard', 'Caps -> Super'], env=env)
