#!/bin/zsh

root_dir="$HOME/.config/"

# Rofi CMD
rofi_cmd() {
	rofi -dmenu -p $root_dir -theme "$HOME/.config/rofi/configs/config.rasi"
}

configs_dir=$(exa $root_dir --no-icons)

# Pass variables to rofi dmenu
run_rofi() {
	echo -e $configs_dir | rofi_cmd
}

# # Actions
chosen=$(run_rofi)
if [[ $chosen = "" ]]; then
  exit 1;
fi

config_chosen="$root_dir$chosen"
kitty -d "$config_chosen"
