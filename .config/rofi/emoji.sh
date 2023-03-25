#!/bin/sh

rofi -modi emoji -show emoji \
  -theme "$HOME/.config/rofi/config.rasi" \
  -location 0 \
  -theme-str 'window {width: 400px; height: 400px; padding: 0;}' \
  -theme-str 'listview {border: 0px; scrollbar: 0;}' \
  -yoffset -50 \
  -kb-element-next j \
  -kb-element-prev k 

