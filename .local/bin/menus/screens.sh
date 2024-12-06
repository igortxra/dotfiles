#!/bin/zsh

profiles=$(autorandr --list)

if [ -z $profiles ]; then
  dunstify -a System "Screens" "No autorandr profile found."
else
  profile=$(echo $profiles | rofi -dmenu -p "Screen Profiles")
  if [ -z $profile ]; then
    exit
  fi
  
  # Load screen profile
  autorandr --load $profile
  
  # Restore wallpaper
  . $HOME/.fehbg
  
  # Reload qtile
  qtile cmd-obj -o cmd -f restart

  # Send notification
  dunstify -a System "Screens" "Changing to profile: $profile"
fi

