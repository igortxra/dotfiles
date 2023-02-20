#!/bin/sh

# Keyboard numlock activation
numlockx on &

# Remap caps to super
setxkbmap -option caps:super

# Fancy visuals (E.g: enable opacity)
picom &

# Update screens
autorandr --change

# Set wallpaper
~/.fehbg &

# Send welcome notification
notify-send "Welcome, IgorTxra"

# udiskie
udiskie &
