#!/bin/bash
VOLUME=$(pamixer --get-volume)
dunstify -r 1 -h string:hlcolor:"#fff" -h int:value:$VOLUME "Volume: $VOLUME%" -t 1000
