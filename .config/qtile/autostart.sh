#!/bin/sh

# Keyboard numlock activation
numlockx on &

# Remap caps to super
setxkbmap -option caps:super

# Update screen profile
autorandr --change

# Set wallpaper
# ~/.fehbg &
nitrogen --restore

# Send welcome notification - Good to verify notification is working
notify-send "Welcome, IgorTxra"

# udiskie
udiskie &

# Fancy visuals (E.g: enable opacity)
picom --experimental-backend &
