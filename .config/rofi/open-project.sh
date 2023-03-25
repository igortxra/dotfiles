#!/bin/zsh

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
    -p "Projects" \
		-theme "$HOME/.config/rofi/config.rasi" \
    -location 0 \
		-theme-str 'window {width: 600px; height: 500px; padding: 0;}' \
    -theme-str 'listview {border: 0px; scrollbar: 0;}' \
    -yoffset -50 \
    -kb
}

root_dir="/home/igortxra/github/"

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
kitty -d "$project_chosen" nvim +NvimTreeToggle
