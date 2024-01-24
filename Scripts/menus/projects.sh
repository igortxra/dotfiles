#!/bin/zsh

projects_root_dir="$HOME/Github/"

project_paths=$(find $projects_root_dir -mindepth 2 -maxdepth 2 -type d)

opts=$(realpath --relative-to=$projects_root_dir $(echo $project_paths))

chosen=$(echo -e $opts | rofi -dmenu -p "Github Projects")
if [[ $chosen = "" ]]; then
  exit 1;
fi

project_chosen="$projects_root_dir$chosen"
kitty -d "$project_chosen" --detach && kitty --detach -d "$project_chosen" nvim
