#!/bin/zsh

dunstify -a System -t 5000 "Saving explicit installed packages" "You can see the result in $HOME/Setup/"
pacman -Qqen > ~/Setup/pkg-list.txt
pacman -Qqem | sed 's/$/ # AUR/' >> ~/Setup/pkg-list.txt
