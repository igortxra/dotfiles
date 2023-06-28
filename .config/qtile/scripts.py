from os.path import expanduser

HOME = expanduser('~')

TERMINAL = "kitty"

# Open
OPEN_NOTES = "notion-app"
OPEN_CALENDAR = "" # TOOO
OPEN_FILE_MANAGER = "thunar"
OPEN_SCREENSHOT = "flameshot gui"
OPEN_WIFI = "iwgtk"
OPEN_AUDIO_SETTINGS = "pavucontrol"

# ROFI Menus
MENU_POWER = f"{HOME}/.config/rofi/powermenu.sh &" 
MENU_APP = f"{HOME}/.config/rofi/launcher.sh &" 
MENU_EMOJI = f"{HOME}/.config/rofi/emoji.sh &" 
MENU_CALC = f"{HOME}/.config/rofi/calc.sh &" 
MENU_BROWSER = f"{HOME}/.config/rofi/open-in-qutebrowser.sh &"
MENU_PROJECT = f"{HOME}/.config/rofi/open-project.sh &"

# Screen Profiles
MONITOR_ONLYNOTEBOOK = "autorandr --change onlynotebook"
MONITOR_ONLYEXTERNAL = "autorandr --change onlyexternal"
MONITOR_DUAL = "autorandr --change dualmonitor"

# Brightness
BRIGHTNESS_UP = 'brightnessctl set 5%+'
BRIGHTNESS_DOWN = 'brightnessctl set 5%-'

# Audio
AUDIO_UP = 'pactl set-sink-volume @DEFAULT_SINK@ +2%'
AUDIO_DOWN = 'pactl set-sink-volume @DEFAULT_SINK@ -2%'
AUDIO_MUTE_UNMUTE = 'pactl set-sink-mute @DEFAULT_SINK@ toggle'
AUDIO_MIC_MUTE = 'pactl set-source-mute @DEFAULT_SOURCE@ toggle'

# Config Utils
AUTOSTART = f'{HOME}/.config/qtile/autostart.sh'
REMAP_CAPS = "setxkbmap -option caps:super"
RELOAD_PICOM = f"/bin/sh {HOME}/shell_scripts/reload_picom.sh &" 
RESTORE_WALLPAPER = f"nitrogen --restore"
LOCK_SCREEN = "betterlockscreen -l blur"
