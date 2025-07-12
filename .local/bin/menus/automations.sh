#!/bin/zsh

automations_dir=$HOME/Automations
automations=$(find $automations_dir -mindepth 1 -maxdepth 1 -type d | xargs basename)

if [ -z $automations ]; then
  dunstify -a System "Automations" "No automation found."
else
  automation=$(echo $automations | rofi -dmenu -p "Automations")

  if [ -z $automation ]; then
    exit
  fi

  # Send notification
  dunstify -a System "Automations" "Executing $automation ..."
  exec "$automations_dir/$automation/run.sh"

  fi

fi

