#!/bin/sh

# Keyboard numlock activation
numlockx on &

# Remap caps to super
setxkbmap -option caps:super

# Fancy visuals (E.g: enable opacity)
picom &

# Set wallpaper
~/.fehbg &
