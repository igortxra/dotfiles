#!/bin/zsh

# Rofi CMD
rofi_cmd() {
	rofi -dmenu -p "Screen Profiles" -theme "$HOME/.config/rofi/autorandr/config.rasi"
}

sceen_profiles=$(autorandr --list)

# Pass variables to rofi dmenu
run_rofi() {
	echo -e $sceen_profiles | rofi_cmd
}

chosen_screen_profile=$(run_rofi)

autorandr --change $chosen_screen_profile
