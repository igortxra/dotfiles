#!/bin/zsh

projects_root_dir="$HOME/Github/"

# Rofi CMD
rofi_cmd() {
	rofi -dmenu -p $projects_root_dir
}

projects_dir=$(exa $projects_root_dir)

# Pass variables to rofi dmenu
run_rofi() {
	echo -e $projects_dir | rofi_cmd
}

# # Actions
chosen=$(run_rofi)
if [[ $chosen = "" ]]; then
  exit 1;
fi

project_chosen="$projects_root_dir$chosen"
kitty -d "$project_chosen" --detach && kitty --detach -d "$project_chosen" nvim
