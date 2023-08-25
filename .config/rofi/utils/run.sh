#!/bin/sh

# Options
reload_picom='Reload Picom'
reload_wallpaper='Reload Wallpaper'
capslock_as_super='CapsLock as Super'
restore_caps_lock='Restore CapsLock'

# Rofi CMD
rofi_cmd() {
	rofi \
	    -dmenu -p "Utils" -config $HOME/.config/rofi/utils/config.rasi
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e "$reload_picom\n$reload_wallpaper\n$capslock_as_super\n$restore_caps_lock" | rofi_cmd
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
    $reload_picom)
			/bin/sh {HOME}/shell_scripts/reload_picom.sh &
    ;;
    $reload_wallpaper)
			nitrogen --restore	
    ;;
    $capslock_as_super)
			setxkbmap -option caps:super
    ;;
    $restore_caps_lock)
			setxkbmap -option
    ;;
esac
