#!/bin/zsh

root_dir="$HOME/github/"

# Rofi CMD
rofi_cmd() {
	rofi -dmenu -p $root_dir -theme "$HOME/.config/rofi/projects/config.rasi"
}

projects_dir=$(exa $root_dir --no-icons)

# Pass variables to rofi dmenu
run_rofi() {
	echo -e $projects_dir | rofi_cmd
}

# # Actions
chosen=$(run_rofi)
if [[ $chosen = "" ]]; then
  exit 1;
fi

project_chosen="$root_dir$chosen"
kitty -d "$project_chosen"
