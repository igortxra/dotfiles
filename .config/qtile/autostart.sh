#!/bin/sh

# Fancy visuals (E.g: enable opacity)
picom --backend glx &

# Keyboard numlock activation
numlockx on &

# Remap caps to super
setxkbmap -option caps:super

# Update screens
autorandr --change

# Set wallpaper
# ~/.fehbg &
nitrogen --restore

# Send welcome notification
notify-send "Welcome"

# udiskie
udiskie &

# Clipboard utils
copyq &

# Reload qtile
killall -s SIGUSR1 qtile
