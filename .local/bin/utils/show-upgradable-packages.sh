#!/bin/zsh

nid=$(dunstify -t 2000 --printid -a System "Packages to upgrade" "loading...")
dunstify -t 0 -a System "Packages to upgrade" "$(yay -Qu)"
dunstify -C $nid
