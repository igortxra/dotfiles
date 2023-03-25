#!/bin/sh


# Rofi CMD
rofi -show drun \
  -theme "$HOME/.config/rofi/config.rasi" \
  -location 0 \
  -theme-str 'window {width: 800px; height: 600px; padding: 0;}' \
  -kb-element-next j \
  -kb-element-prev k 
