#!/bin/zsh

profiles=$(autorandr --list)

if [ -z $profiles ]; then
  dunstify -a System "Screens" "No autorandr profile found."
else
  profile=$(echo $profiles | rofi -dmenu -p "Screen Profiles")
  if [ -z $profile ]; then
    exit
  fi
  autorandr --load $profile
  dunstify -a System "Screens" "Changing to profile: $profile"
fi

