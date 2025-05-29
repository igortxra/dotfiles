#!/bin/bash

# Pega o volume atual
VOLUME=$(pamixer --get-volume)

# Gera barra de progresso
dunstify -r 1 -h string:hlcolor:"#fff" -h int:value:$VOLUME "Volume: $VOLUME%" -t 1000
