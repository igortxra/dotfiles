#!/bin/sh

rofi -show calc -modi calc -no-show-match -no-sort \
  -theme "$HOME/.config/rofi/config.rasi" \
  -location 0 \
  -theme-str 'window {width: 400px; height: 290px; padding: 0;}' \
  -theme-str 'listview {border: 0px; scrollbar: 0;}' \
  -yoffset -50 \
  -kb-element-next j \
  -kb-element-prev k 

