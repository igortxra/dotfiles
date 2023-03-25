#!/bin/sh

# Options
shutdown='   Shutdown'
reboot='   Reboot'
lock='   Lock'
suspend='   Suspend'
logout='   Logout'

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
		-theme "$HOME/.config/rofi/config.rasi" \
    -location 0 \
		-theme-str 'window {width: 200px; height: 260px; padding: 0;}' \
    -theme-str 'inputbar {enabled: false;}' \
    -theme-str 'listview {border: 0px; scrollbar: 0;}' \
    -yoffset -50 \
    -kb-element-next j \
    -kb-element-prev k 
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e "$lock\n$suspend\n$logout\n$reboot\n$shutdown" | rofi_cmd
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
    $shutdown)
		systemctl poweroff
        ;;
    $reboot)
		systemctl reboot
        ;;
    $lock)
		betterlockscreen -l
        ;;
    $suspend)
    mpc -q pause
    amixer set Master mute
    systemctl suspend
        ;;
    $logout)
		qtile exit
        ;;
esac
