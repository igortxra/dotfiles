#!/bin/zsh

dunstify -t 0 -a System "Packages to upgrade" "$(yay -Qu)"
