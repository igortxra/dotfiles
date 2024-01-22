#!/bin/zsh

# List all possible config files and dirs
config_dirs=$(ls -d1 ~/.config/* && find $HOME -maxdepth 1 -type f)

# Use rofi to choose one
selected=$(echo $config_dirs | rofi -dmenu)


if [[ -d $selected ]]; then
  # If chosen is directory
  kitty --hold --directory $selected --execute nvim +Neotree $(ls $selected | head -1)

elif [[ -f $selected ]]; then
  # If chosen is file
  kitty --hold --directory $(dirname $selected) --execute nvim +Neotree $(basename $selected)

else
    exit 1
fi
