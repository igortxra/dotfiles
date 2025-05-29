#!/bin/sh

# Options
shutdown='shutdown'
reboot='reboot'
lock='lock'
suspend='suspend'
logout='logout'

# Rofi CMD
rofi_cmd() {
	rofi -dmenu -p "Power"
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
        systemctl suspend
        ;;
    $logout)
        qtile cmd-obj -o cmd -f shutdown
        ;;
esac
