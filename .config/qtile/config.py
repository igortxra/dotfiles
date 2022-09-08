# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

#############
# "GLOBALS" #
#############

# COLOR NAMES
BLACK = '#111122'
WHITE = '#ffffff'
GRAY = '#666666'
LIGHT_GREY = '#555555'
RED = '#cb2424'
GREEN = '#00aa00'
DARK_GREEN = '#499129'
BLUE = '#1185dc'
MIDNIGHT_BLUE= "#41729F"
BLUE_GREY= "#5885AF"
DARK_BLUE = "#274472"
BABY_BLUE = "#C3E0E5"
YELLOW = '#eba109'

# COLORS AS SHORTCUTS
PRIMARY=DARK_BLUE
SECONDARY=MIDNIGHT_BLUE
GROUPBOX=DARK_BLUE
BAR_BACKGROUND=BLACK

# UNICODES
NET_UNICODE = ''
AUDIO_UNICODE = ''
BRIGHTNESS_UNICODE = ''
BATTERY_UNICODE = ''
UPDATES_UNICODE = ''
CLOCK_UNICODE=""
ACTIVE_UNICODE=""

# NAMES
BACKLIGHT_NAME='intel_backlight'

# Shell Scripts Paths (with '&')
POWER_MENU_SCRIPT = os.path.expanduser(
    "~/.config/rofi/powermenu/type-2/powermenu.sh &")
APP_MENU_SCRIPT =  os.path.expanduser(
    "~/.config/rofi/launchers/type-3/launcher.sh &")
SCREENSHOT_SCRIPT = os.path.expanduser(
    "~/.config/rofi/applets/bin/screenshot.sh &")

# COMMANDS
CMD_LOCK_SCREEN = "betterlockscreen -l blur"
CMD_SET_BRIGHTNESS = "brightnessctl s {}%"
CMD_WIFI_MENU = "iwgtk"
CMD_FILE_MANAGER = "alacritty -e ranger"
CMD_MONITOR_ONLYNOTEBOOK = "autorandr --change onlynotebook"
CMD_MONITOR_ONLYEXTERNAL = "autorandr --change onlyexternal"
CMD_MONITOR_DUAL = "autorandr --change dualmonitor"

#########
# HOOKS #
#########

@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([autostart_script])

###################
# Utils functions #
###################

def get_monitors():
    xr = subprocess.check_output(
        'xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors

##################
# KEYS/SHORTCUTS #
##################

mod = "mod4"  # Super (or Windows) key
terminal = guess_terminal()

keys = [

    # Brightness control
    Key([], "XF86MonBrightnessUp",   lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

    # Volume control
    Key([], "XF86AudioMicMute",     lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),
    Key([], "XF86AudioMute",        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),

    # Move focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Kill focused window
    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"),

    # Spawn Terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Next/Previous layout
    Key([mod, "control"], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([mod, "control", "shift"], "Tab",
        lazy.prev_layout(),
        desc="Toggle between layouts"),

    # Run command
    Key([mod], "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Shift window location
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Quit Qtile
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),

    # Restart Qtile
    Key([mod, "control"], "r",
        lazy.reload_config(),
        desc="Reload the config"),

    # Show/Hide screen bars
    Key([mod], "b",
        lazy.hide_show_bar(position='all'),
        desc="Toggle bars"),

    # Switch between monitors
    Key([mod], 'm', lazy.next_screen(), desc='Next monitor'),

    # Next/previous group
    Key([mod], 'Tab', lazy.screen.next_group(), desc='Next group'),
    Key([mod, 'shift'], 'Tab', lazy.screen.prev_group(), desc='Next group'),

    # Resize window
    Key([mod], "Left", lazy.layout.grow_left()),
    Key([mod], "Up", lazy.layout.grow_up()),
    Key([mod], "Down", lazy.layout.grow_down()),
    Key([mod], "Right", lazy.layout.grow_right()),
    # For monadTall
    Key([mod, "control"], "Left",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster()),
    Key([mod, "control"], "Right",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster()),

    # Launcher / applets / tools
    Key([mod], "p",
        lazy.spawn(POWER_MENU_SCRIPT),
        desc="Launch power menu"),

    # App menu
    Key([mod], "space",
        lazy.spawn(APP_MENU_SCRIPT),
        desc="Launch app menu"),

    # Screenshot
    Key([], "Print", lazy.spawn(SCREENSHOT_SCRIPT)),

    # File manager
    Key([mod],"e", lazy.spawn(CMD_FILE_MANAGER)),

    # Monitors modifiers
    Key([mod, 'control'], '0', lazy.spawn(CMD_MONITOR_ONLYNOTEBOOK)),
    Key([mod, 'control'], '1', lazy.spawn(CMD_MONITOR_ONLYEXTERNAL)),
    Key([mod, 'control'], '2', lazy.spawn(CMD_MONITOR_DUAL))
]
#####################
# GROUPS/WORKSPACES #
#####################
workspaces = [
        {"name": "  ₁", "key": "1","layout": "columns", "matches": []},
        {"name": "  ₂", "key": "2","layout": "monadtall", "matches": []},
        {"name": "  ₃", "key": "3","layout": "matrix", "matches": []},
        {"name": "  ₄", "key": "4","layout": "columns", "matches": []},
        {"name": "  ₅", "key": "5","layout": "columns", "matches": []},
        {"name": "  ₆", "key": "6","layout": "columns", "matches": []},
        {"name": "  ₇", "key": "7","layout": "max", "matches": [Match(wm_class='libreoffice')]},
        {"name": "阮 ₈", "key": "8","layout": "max", "matches": []},
        {"name": "  ₉", "key": "9","layout": "max", "matches": [Match(wm_class='discord')]}]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    layouts = workspace["layout"] if "layout" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout=layouts))

    # Move focus to group
    keys.append(Key([mod], workspace["key"],
                lazy.group[workspace["name"]].toscreen()))

    # Move window to group
    keys.append(Key([mod, "shift"], workspace["key"],
                lazy.window.togroup(workspace["name"]),
                lazy.group[workspace["name"]].toscreen()))

###########
# LAYOUTS #
###########

# Default theme for layouts
layout_theme = dict(
    border_width=2,
    border_focus=BLUE,
    border_normal=BLACK,
    margin=5,
    padding=10)

layouts = [
    layout.Max(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.Stack(num_stacks=2, **layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

###################
# SCREEN: WIDGETS #
###################

widget_defaults = dict(
    font="Font Awesome",
    fontsize=12,
    padding=5)

main_bottom_widgets = [

    # Widget Box
     widget.WidgetBox(
        text_closed="  ",
        text_open="  ",
        background=PRIMARY,
        widgets=[
            widget.Spacer(length=2),

            # CPU
            widget.TextBox("CPU", background=GREY),
            widget.CPU(background=LIGHT_GREY, format='{freq_current}GHz {load_percent}%'),
            widget.Spacer(length=2),

            # Memory
            widget.TextBox("RAM", background=GREY, **widget_defaults),
            widget.Memory(background=LIGHT_GREY, format='{MemUsed: .3f}{mm} |{MemTotal: .3f}{mm}', measure_mem='G'),
            widget.Spacer(length=2),

            # Internet
            widget.TextBox(NET_UNICODE, background=GREY),
            widget.Wlan(
                background=LIGHT_GREY,
                mouse_callbacks={
                    "Button1": lazy.spawn(CMD_WIFI_MENU)
                },
                format='{essid} {percent:2.0%}',
                **widget_defaults),

            widget.Spacer(length=2),
        ],
        **widget_defaults
    ),

    # Prompt
    widget.Spacer(length=2),
    widget.Prompt(prompt="RUN: ", background=PRIMARY),

    # Systray Icons
    widget.Systray(icon_size=15, padding=15),

    widget.Spacer(),

    # Current Screen
    widget.CurrentScreen(
        active_text=ACTIVE_UNICODE,
        inactive_text=ACTIVE_UNICODE,
        active_color=BLUE,
        inactive_color=GREY),
    widget.Sep(foreground=BAR_BACKGROUND),

    # Layout
    widget.CurrentLayoutIcon(
        background=SECONDARY,
        scale=0.8,
        **widget_defaults),
    widget.WindowCount(background=GREY, show_zero=True),
    widget.Spacer(length=2),

    # Groups
    widget.GroupBox(
        active=WHITE,
        inactive=LIGHT_GREY,
        this_screen_border=GREY,
        other_screen_border=GREY,
        this_current_screen_border=GROUPBOX,
        other_current_screen_border=GREY,
        highlight_method='block',
        disable_drag=True,
        borderwidth=1,
        **widget_defaults),
    widget.Sep(foreground=BAR_BACKGROUND),

    widget.Spacer(),

    # Updates
    widget.CheckUpdates(
        display_format=UPDATES_UNICODE + " {updates}",
        colour_have_updates=YELLOW,
        colour_no_updates=WHITE,
        no_update_string=f"  0"),
    widget.Spacer(length=2),

    # Volume control
    widget.TextBox(AUDIO_UNICODE, background=PRIMARY),
    widget.Volume(background=PRIMARY, **widget_defaults),

    # Brightness/Backlight control
    widget.Spacer(length=2),
    widget.TextBox(BRIGHTNESS_UNICODE, background=SECONDARY, **widget_defaults),
    widget.Backlight(
        backlight_name=BACKLIGHT_NAME,
        change_command=CMD_SET_BRIGHTNESS,
        background=SECONDARY,
        **widget_defaults),
    widget.Spacer(length=2),

    # Battery
    widget.TextBox(BATTERY_UNICODE, background=PRIMARY),
    widget.Battery(
        background=PRIMARY,
        low_background=RED,
        low_foreground=WHITE,
        low_percentage=0.40,
        notify_below=40,
        charge_char=f' ',
        discharge_char='',
        show_short_text=True,
        format='{percent:2.0%} {char}'),
    widget.Spacer(length=2),

    # Clock
    widget.TextBox(CLOCK_UNICODE, background=GREY),
    widget.Clock(format="%H:%M", background=LIGHT_GREY, foreground=WHITE),
    widget.Spacer(length=2),

    # Clock
    widget.TextBox("", background=GREY),
    widget.Clock(format="%D", background=LIGHT_GREY, foreground=WHITE),
    widget.Spacer(length=2),


]

secondary_bottom_widgets = [

    widget.Spacer(),

    # Current Screen
    widget.CurrentScreen(
        active_text=ACTIVE_UNICODE,
        inactive_text=ACTIVE_UNICODE,
        active_color=BLUE,
        inactive_color=GREY),
    widget.Sep(foreground=BAR_BACKGROUND),

    # Layout
    widget.CurrentLayoutIcon(
        background=SECONDARY,
        scale=0.8,
        **widget_defaults),
    widget.WindowCount(background=GREY, show_zero=True),
    widget.Spacer(length=2),

    # Groups
    widget.GroupBox(
        active=WHITE,
        inactive=LIGHT_GREY,
        this_screen_border=GREY,
        other_screen_border=GREY,
        this_current_screen_border=GROUPBOX,
        other_current_screen_border=GREY,
        highlight_method='block',
        disable_drag=True,
        borderwidth=1,
        **widget_defaults),
    widget.Sep(foreground=BAR_BACKGROUND),

    widget.Spacer(),

    widget.TextBox("IgorTxra"),
]

#######################
# SCREEN: TASK BAR #
#######################

bar_style = dict(
    background=BAR_BACKGROUND,
    border_color=BAR_BACKGROUND,
        border_width=[0, 0, 0, 0],
    margin=[0, 0, 0, 0])

monitors = get_monitors()
screens = []
for monitor in range(monitors):
    if monitor == 0:
        # Primary monitor
        screens.append(Screen(
            bottom=bar.Bar(widgets=main_bottom_widgets, size=18, **bar_style)))
    else:
        # Secondary monitors
        screens.append(Screen(
            bottom=bar.Bar(widgets=secondary_bottom_widgets, size=18, **bar_style)))

########
# MORE #
########

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
