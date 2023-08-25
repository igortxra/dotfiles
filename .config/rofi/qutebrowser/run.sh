#!/bin/bash

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
    -p " " -theme "$HOME/.config/rofi/qutebrowser/config.rasi"
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e | rofi_cmd
}

# Actions
chosen=$(run_rofi)
if [[ $chosen = "" ]]; then
  exit 1;
fi

qutebrowser ":open $chosen"

