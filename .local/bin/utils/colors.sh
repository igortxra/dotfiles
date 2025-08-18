#!/usr/bin/env bash

# Dunst
ln -sf ~/.cache/wal/dunst/dunstrc ~/.config/dunst/dunstrc
dunstctl reload

# Qutebrowser
ln -sf ~/.cache/wal/qutebrowser/colors.py ~/.config/qutebrowser/colors.py
pgrep qutebrowser > /dev/null && qutebrowser ':config-source'

# Flameshot
ln -sf ~/.cache/wal/flameshot/flameshot.ini ~/.config/flameshot/flameshot.ini

# Notify the changes
ln -sf ~/.cache/wal/dunst/dunstrc ~/.config/dunst/dunstrc
dunstify -r 2 "Wallpaper and theme updated!"
