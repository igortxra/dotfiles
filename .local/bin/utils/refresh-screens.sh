#!/bin/bash

# Reload screen profile
autorandr --change

# Restore wallpaper
. $HOME/.fehbg

# Reload qtile
qtile cmd-obj -o cmd -f restart

# Send notification
current_profile=$(autorandr --current)
dunstify -a System Screens "Screen changed to profile: $current_profile"

