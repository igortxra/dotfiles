#!/bin/sh

# Keyboard numlock activation
numlockx on &

# Remap caps to super
setxkbmap -option caps:super

# Update screens
autorandr --change

# Set wallpaper
~/.fehbg &

# Send welcome notification
notify-send "Welcome, IgorTxra"

# udiskie
udiskie &

# Fancy visuals (E.g: enable opacity)
picom &
