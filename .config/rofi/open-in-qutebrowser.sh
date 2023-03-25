#!/bin/bash

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
    -p "Qutebrowser" \
		-theme "$HOME/.config/rofi/config.rasi" \
    -location 0 \
		-theme-str 'window {width: 600px; height: 50; padding: 0;}' \
    -theme-str 'listview {border: 0px; scrollbar: 0;}' \
    -yoffset -50 \
    -kb
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

