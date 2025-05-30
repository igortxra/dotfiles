#!/bin/sh
VOLUME=$(playerctl -p spotify volume)
VOLUME_PERCENTAGE=$(echo "$VOLUME * 100" | bc | awk '{ printf "%.2f", $1 }')
dunstify -r 1 -h int:value:$VOLUME_PERCENTAGE -h string:hlcolor:"#fff" "Music Volume" -t 1000
