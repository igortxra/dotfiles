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

import asyncio
import os
import subprocess
from typing import List

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import (Click, Drag, DropDown, Group, Key, KeyChord,
                             Match, ScratchPad, Screen)
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from colors import get_theme

###################################################################################################
# GLOBALS #########################################################################################

colors = get_theme("dracula")
#colors = get_theme("catppuccin")

# Globals
WIDGET_FONT = "Font Awesome 6 Bold"
BACKLIGHT_NAME = 'intel_backlight'

# Unicodes - https://fontawesome.com/search
UNICODE_NET = ''
UNICODE_AUDIO = ''
UNICODE_BRIGHTNESS = ''
UNICODE_BATTERY = ''
UNICODE_CHARGING = ' '
UNICODE_UPDATES = ''
UNICODE_NO_UPDATES = ''
UNICODE_CLOCK = ""
UNICODE_AGENDA = ""
UNICODE_CLIPBOARD = " Copied"
UNICODE_RAM = ""
UNICODE_CPU = ""

# Scripts
HOME = os.path.expanduser('~')
SCRIPT_AUTOSTART = f'{HOME}/.config/qtile/autostart.sh'
SCRIPT_POWER_MENU = f"{HOME}/.config/rofi/powermenu.sh &" 
SCRIPT_APP_MENU = f"{HOME}/.config/rofi/launcher.sh &" 
SCRIPT_OPEN_IN_QUTEBROWSER = f"{HOME}/.config/rofi/open-in-qutebrowser.sh &"
SCRIPT_OPEN_PROJECT = f"{HOME}/.config/rofi/open-project.sh &"
SCRIPT_CALC = f"{HOME}/.config/rofi/calc.sh &" 
SCRIPT_EMOJI = f"{HOME}/.config/rofi/emoji.sh &" 
SCRIPT_WALLPAPER = f"{HOME}/.fehbg"

# Commands
CMD_REMAP_CAPS = "setxkbmap -option caps:super"
CMD_OPEN_CALENDAR = "kitty --class calcurse  -o confirm_os_window_close=0 --execute calcurse"
CMD_SCREENSHOT = "flameshot gui"
CMD_TODO_LIST = "todour"
CMD_LOCK_SCREEN = "betterlockscreen -l blur"
CMD_WIFI_MENU = "iwgtk"
CMD_FILE_MANAGER = "thunar"
CMD_MONITOR_ONLYNOTEBOOK = "autorandr --change onlynotebook"
CMD_MONITOR_ONLYEXTERNAL = "autorandr --change onlyexternal"
CMD_MONITOR_DUAL = "autorandr --change dualmonitor"

CMD_BRIGHTNESS_UP = 'brightnessctl set 5%+'
CMD_BRIGHTNESS_DOWN = 'brightnessctl set 5%-'

CMD_AUDIO_MIC_MUTE = 'pactl set-source-mute @DEFAULT_SOURCE@ toggle'
CMD_AUDIO_MUTE_UNMUTE = 'pactl set-sink-mute @DEFAULT_SINK@ toggle'
CMD_AUDIO_UP = 'pactl set-sink-volume @DEFAULT_SINK@ +2%'
CMD_AUDIO_DOWN = 'pactl set-sink-volume @DEFAULT_SINK@ -2%'

###################################################################################################
# Utils functions #################################################################################


def send_notification(title: str = "Message", msg: str = "", expire=2000):
    """ Return a notfication command """
    return f"notify-send '{title}' '{msg}' --expire-time={expire}"


def bold(text: str):
    """ Return text between bold tags """
    return f'<b>{text}</b>'


def go_to_group(name: str):
    """ Go to group but keeping it predefined screen """
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return
        if name in '789':
            qtile.focus_screen(1)
            qtile.groups_map[name].cmd_toscreen()
        else:
            qtile.focus_screen(0)
            qtile.groups_map[name].cmd_toscreen()
    return _inner


def get_monitors():
    """ Get number of connected monitors """
    xr = subprocess.check_output(
        'xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors
MONITORS = get_monitors()

@lazy.function
def move_window_to_next_screen(qtile):
    """ Moves a window to a screen and focuses it, allowing you to move it """
    window = qtile.current_window
    qtile.cmd_next_screen()
    window.togroup(qtile.current_screen.group.name)


###############################################################################
# Keys ########################################################################
# Obs: ALMOST all keys are specified in this section ##########################


SUPER = "mod4"
ALT = "mod1"
TERMINAL = "kitty"
# TERMINAL = guess_terminal()

keys = [

    Key([SUPER, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),

    Key([SUPER, "control"], "r",
        lazy.reload_config(),
        desc="Reload the config"),

    Key([SUPER], "Return",
        lazy.spawn(TERMINAL),
        desc="Launch terminal"),

    Key([SUPER], "Tab",
        lazy.next_layout(),
        desc='Next layout'),

    Key([SUPER, "shift"], "Tab",
        lazy.prev_layout(),
        desc="Previous layout"),

    # Laptop keys
    Key([], "XF86MonBrightnessUp", 
        lazy.spawn(CMD_BRIGHTNESS_UP), 
        desc='Increase brightness'),

    Key([], "XF86MonBrightnessDown", 
        lazy.spawn(CMD_BRIGHTNESS_DOWN), 
        desc='Decrease brightness'),

    Key([], "XF86AudioMicMute", 
        lazy.spawn(CMD_AUDIO_MIC_MUTE), 
        desc='Mute microphone'),

    Key([], "XF86AudioMute", 
        lazy.spawn(CMD_AUDIO_MUTE_UNMUTE),
        desc='Mute audio'),

    Key([], "XF86AudioRaiseVolume",
        lazy.spawn(CMD_AUDIO_UP),
        desc='Increase audio volume'),

    Key([], "XF86AudioLowerVolume", 
        lazy.spawn(CMD_AUDIO_DOWN), 
        desc='Decrease audio volume'),

    # Move focus
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], 'm', lazy.next_screen(), desc='Change focused screen'), 

    # Move window
    Key([SUPER, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([SUPER, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([SUPER, "shift"], "m", move_window_to_next_screen(), desc="Move window to next screen group"),

    # Resive window
    Key([SUPER, "control"], "h",
        lazy.layout.grow_left(),
        desc="Grow window to left"),

    Key([SUPER, "control"], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"),

    Key([SUPER, "control"], "k", 
        lazy.layout.grow_up(),
        desc="Grow window up"),

    Key([SUPER, "control"], "l", 
        lazy.layout.grow_right(),
        desc="Grow window right"),

    Key([SUPER], "g", 
        lazy.layout.grow_main(),
        desc="Grow main panel (Useful for specific layouts)"),

    Key([SUPER, "shift"], "g",
        lazy.layout.shrink_main(),
        desc="Shrink main panel (Useful for specific layouts)"),

    Key([SUPER], "w",
        lazy.window.kill(),
        desc="Kill focused window"),
    
    # Launchers
    Key([SUPER], "space",
        lazy.spawn(SCRIPT_APP_MENU),
        desc="Launch app menu"),
 
    Key([SUPER], "e", 
        lazy.spawn(CMD_FILE_MANAGER),
        desc="Open a file manager"),

    Key([], "Print",
        lazy.spawn(CMD_SCREENSHOT),
        desc='Launch screenshot'),

    # Menus
    Key([SUPER], "q", 
        lazy.spawn(SCRIPT_OPEN_IN_QUTEBROWSER), 
        desc="Open qutebrowser shortcut"),

    Key([SUPER], "o", 
        lazy.spawn(SCRIPT_OPEN_PROJECT), 
        desc="Open projects menu (A custom script for open a dir in a text editor)"),

    Key([SUPER], "p",
        lazy.spawn(SCRIPT_POWER_MENU),
        desc="Launch power menu"),

    Key([SUPER], "c",
        lazy.spawn(SCRIPT_CALC),
        desc="Launch calculator"),

    Key([SUPER, "shift"], "Equal",
        lazy.spawn(SCRIPT_EMOJI),
        desc="Launch emoji list"),

    # Settings
    Key([SUPER], "b",
        lazy.hide_show_bar(position="top"),
        desc="Toggle bar"),

    Key([SUPER], "0", 
        lazy.spawn(CMD_REMAP_CAPS), 
        desc="Remap caps to act as super"),

    Key([SUPER, 'control'], 'w',
        lazy.spawn(SCRIPT_WALLPAPER),
        lazy.spawn(send_notification("Screens", "Wallpaper fixed", 4000)),
        desc='Update wallpaper (Used when screen layout change and the wallpaper brake)'),

    Key([SUPER], "f", 
        lazy.window.disable_floating(),
        desc="Disable floating behavior for focused window"),

    # Settings / Screen layout
    Key([SUPER, 'control'], '0',
        lazy.spawn(CMD_MONITOR_ONLYNOTEBOOK),
        lazy.spawn(
            send_notification("Screens", "Using only notebook screen", 4000)),
        desc='Use only notebook screen'),

    Key([SUPER, 'control'], '1',
        lazy.spawn(CMD_MONITOR_ONLYEXTERNAL),
        lazy.spawn(
            send_notification("Screens", "Using only external screen", 4000)),
        desc='Use only external screen'),

    Key([SUPER, 'control'], '2',
        lazy.spawn(CMD_MONITOR_DUAL),
        lazy.spawn(send_notification("Screens", "Using both screens", 4000)),
        desc='Use both screens, notebook and external'),

    # Settings Menu
    KeyChord([SUPER], "Equal", [

        # Audio submenu
        KeyChord([], "a", [
            Key([], "j", lazy.spawn(CMD_AUDIO_DOWN)),
            Key([], "k", lazy.spawn(CMD_AUDIO_UP)),
            Key([], "m", lazy.spawn(CMD_AUDIO_MUTE_UNMUTE))
        ], mode='Audio'),

        # Brightness submenu
        KeyChord([], "b", [
            Key([], "j", lazy.spawn(CMD_BRIGHTNESS_DOWN)),
            Key([], "k", lazy.spawn(CMD_BRIGHTNESS_UP))
        ], mode='Brightness'),

        # Wi-fi submenu
        Key([], "w", lazy.spawn(CMD_WIFI_MENU)),

    ], mode='Settings'),

]

###############################################################################
# Groups - Workspaces
# Obs.: Group Keys MUST be in the same lenght as groups

groups: List[Group] = [
        Group("1", label=" ₁", layout="monadtall", matches=[Match(wm_class="Firefox"), Match(wm_class="qutebrowser")]),
        Group("2", label=" ₂", layout="max", matches=[Match(title="nvim")]),
        Group("3", label=" ₃", layout="monadtall", matches=[Match(wm_class="Postman")]), 
        Group("4", label=" ₄", layout="monadtall", matches=[]), 
        Group("5", label=" ₅", layout="monadtall", matches=[]),    
        Group("6", label=" ₆", layout="monadtall", matches=[]), 
        Group("7", label=" ₇", layout="monadtall", matches=[]), 
        Group("8", label=" ₈", layout="max", matches=[]), 
        Group("9", label=" ₉", layout="max", matches=[]), 
]

for group in groups:

    keys.append(
        Key([SUPER], group.name,
            lazy.function(go_to_group(group.name)),
            desc="Go to specified group"))

    keys.append(
        Key([SUPER, "shift"], group.name,
            lazy.window.togroup(group.name),
            lazy.function(go_to_group(group.name)),
            desc="Move window to specified group"))

###############################################################################
# ScratchPads

groups.append(
    ScratchPad('scratchpad', [
        DropDown('terminal', TERMINAL, width=0.6, height=0.7, x=0.2, y=0.15),
        DropDown('todo', CMD_TODO_LIST, width=0.6, height=0.7, x=0.2, y=0.15),
    ]))

keys.extend([
    Key(["control"], "Return", lazy.group["scratchpad"].dropdown_toggle('terminal')),
    Key([SUPER], "t", lazy.group["scratchpad"].dropdown_toggle('todo'))
])


###############################################################################
# Layouts

# Default params for layouts
layout_theme = dict(
    border_width=2,
    border_focus=colors.window_focused_border,
    border_normal=colors.window_border,
    margin=8,
    padding=2)

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
]

###############################################################################
# Widgets

widget_defaults = dict(
    font=WIDGET_FONT,
    fontsize=11,
    padding=10)

icons_defaults = dict(
    font=WIDGET_FONT,
    fontsize=11,
    padding=0)
 

groupbox_main = widget.GroupBox(
    active=colors.groupbox_active,
    inactive=colors.groupbox_inactive,
    this_screen_border=colors.groupbox_this,
    other_screen_border=colors.groupbox_other,
    this_current_screen_border=colors.groupbox_this_current,
    other_current_screen_border=colors.groupbox_other_current,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=3,
    **widget_defaults)

groupbox_secondary = widget.GroupBox(
    active=colors.groupbox_active,
    inactive=colors.groupbox_inactive,
    this_screen_border=colors.groupbox_this,
    other_screen_border=colors.groupbox_other,
    this_current_screen_border=colors.groupbox_this_current,
    other_current_screen_border=colors.groupbox_other_current,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=3,
    visible_groups=[
        groups[6].name,
        groups[7].name,
        groups[8].name
    ],
    **widget_defaults)

main_top_widgets = [
    
    widget.Spacer(10),

    widget.CurrentLayoutIcon(
        background=colors.current_layout.bg,
        foreground=colors.current_layout.fg,
        scale=0.8,
        **widget_defaults),

    # widget.WindowCount(
    #     background=colors.window_count.bg, 
    #     foreground=colors.window_count.fg, 
    #     show_zero=True),

    widget.Spacer(5),
    groupbox_main,

    widget.Spacer(20),
    
    widget.Mpris2(
        name="spotify",
        display_metadata=['xesam:title', 'xesam:artist'],
        scroll_chars=None,
        objname="org.mpris.MediaPlayer2.spotify",
        scroll_interval=0,
        background=colors.spotify.bg,
        foreground=colors.spotify.fg,
        fmt='{}   ',
        paused_text='  {track}',
        mouse_callbacks={
            "Button3": lazy.function(go_to_group("8"))
        },
    ),

    widget.Spacer(5),

    widget.Clipboard(
        fmt=bold(UNICODE_CLIPBOARD),
        max_width=2,
        background=colors.clipboard.bg,
        foreground=colors.clipboard.fg,
        **widget_defaults),

    widget.Spacer(),

    widget.Chord(
        font="Fira Code", # TEMP
        background=colors.chord.bg, 
        foreground=colors.chord.fg, 
        fmt=bold(" -> ") + "{}"),

    widget.Spacer(),

    # CPU
    widget.WidgetBox(
        text_closed="  ",
        fontsize=14,
        close_button_location="right",
        text_open="    ",
        widgets=[
            widget.TextBox(
                bold(f'{UNICODE_CPU}'),
                background=colors.cpu_graph.bg,
                foreground=colors.cpu_graph.fg,
                **icons_defaults),
            widget.CPU(
                background=colors.cpu_graph.bg,
                foreground=colors.cpu_graph.fg,
            ),
            widget.CPUGraph(
                type='line',
                background=colors.cpu_graph.bg,
                border_color=colors.cpu_graph.fg,
                border_width=0,
                line_width=2,
                margin_y=3,
                fill_color=colors.cpu_graph.fg,
                graph_color=colors.cpu_graph.fg
            ),

            widget.Spacer(20),

            # Memory
            widget.TextBox(
                bold(f'{UNICODE_RAM} RAM'),
                background=colors.ram.bg,
                foreground=colors.ram.fg,
                **icons_defaults),
            widget.Memory(
                format='{MemUsed: .3f}{mm} / {MemTotal: .3f}{mm}',
                measure_mem='G',
                background=colors.ram.bg,
                foreground=colors.ram.fg,
                **widget_defaults),
            widget.MemoryGraph(
                type='line',
                background=colors.ram.bg,
                border_color=colors.ram.fg,
                border_width=0,
                margin_y=3,
                line_width=1,
                fill_color=colors.ram.fg,
                graph_color=colors.ram.fg)
        ]
    ),

    widget.Spacer(10),

    widget.CheckUpdates(
        display_format=bold(UNICODE_UPDATES + " {updates} updates"),
        colour_have_updates=colors.check_updates.fg,
        background=colors.check_updates.bg,
        no_update_string=UNICODE_NO_UPDATES),

    widget.Spacer(20),

    # Internet
    widget.TextBox(
        bold(UNICODE_NET),
        background=colors.wifi.bg,
        foreground=colors.wifi.fg,
        **icons_defaults),
    widget.Wlan(
        format='{percent:2.0%}',
        background=colors.wifi.bg,
        foreground=colors.wifi.fg,
        mouse_callbacks={
            "Button1": lazy.spawn(CMD_WIFI_MENU)
        },
        **widget_defaults),

    widget.Spacer(15),

    widget.TextBox(
        bold(UNICODE_AUDIO), 
        background=colors.audio.bg, 
        foreground=colors.audio.fg,
        **icons_defaults),
    widget.Volume(
        background=colors.audio.bg,
        foreground=colors.audio.fg, 
        **widget_defaults),

    widget.Spacer(5),

    widget.Battery(
        background=colors.battery.bg,
        foreground=colors.battery.fg,
        low_background=colors.battery_low.bg,
        low_foreground=colors.battery_low.fg,
        low_percentage=0.40,
        notify_below=40,
        charge_char=UNICODE_CHARGING,
        discharge_char='',
        show_short_text=True,
        format=UNICODE_BATTERY + '  {percent:2.0%} {char}'),

       
    widget.Spacer(5),

    widget.Clock(
        format=f"{UNICODE_AGENDA} %d/%m/%Y %H:%M",
        background=colors.clock.bg,
        foreground=colors.clock.fg,
        mouse_callbacks={
            "Button1": lazy.spawn(CMD_OPEN_CALENDAR)
        }),

    widget.Spacer(10),

]  # main_top_widgets END

secondary_widgets = [
    widget.Spacer(10),
    widget.CurrentLayoutIcon(
        background=colors.current_layout.bg,
        foreground=colors.current_layout.fg,
        scale=0.8,
        **widget_defaults),
    groupbox_secondary,
    widget.Spacer(),
]

bottom_widgets = [
    widget.WindowName(),
]


###############################################################################
# Screen and monitors

bar_style = dict(
    background=colors.bar.bg,
    border_color=colors.bar.bg,
    margin=[5, 10, 0, 10],
    border_width=2)

main_bar = bar.Bar(widgets=main_top_widgets, size=23, **bar_style)
secondary_bar = bar.Bar(widgets=secondary_widgets, size=23, **bar_style)

screens = []
for monitor in range(MONITORS):

    if monitor == 0:
        # Primary monitor
        screens.append(Screen(top=main_bar))

    else:
        # Secondary monitors
        screens.append(Screen(top=secondary_bar))

###################################################################################################
# Hooks ###########################################################################################
@hook.subscribe.screens_reconfigured
def reconfigure_groupbox():
    """ Adapt visible groups depending on number of screens """
    groups_names = [g.name for g in qtile.groups]
    if len(qtile.screens) > 1:
        groupbox_main.visible_groups = groups_names[0:6]
    else:
        groupbox_main.visible_groups = groups_names


@hook.subscribe.startup
def startup():
    """ Execute some steps in qtile refresh """
    reconfigure_groupbox()

@hook.subscribe.startup_once
def autostart():
    """ Executes a script on qtile startup """
    subprocess.Popen([SCRIPT_AUTOSTART])


@hook.subscribe.client_new
async def move_spotify(client):
    """ Move spotify window to its group """
    await asyncio.sleep(0.1)
    if 'Spotify' in client.name:
        client.qtile.cmd_simulate_keypress([SUPER, "shift"], "8")


@hook.subscribe.client_new
def modify_window(client):
    """ Focus in the group where the new client will be moved by Match """
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            # A way to call go_to_group() because its impossible call directly
            client.qtile.cmd_simulate_keypress([SUPER], group.name)


@hook.subscribe.client_name_updated
def move_to_a_match_a_group(client):
    """ Focus in the group where the new client will be moved by Match when client name changes """
    for group in groups:
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            # A way to call go_to_group() because its impossible call directly
            client.qtile.cmd_simulate_keypress([SUPER, "shift"], group.name)


###############################################################################
# MORE

# Drag floating layouts.
mouse = [
    Drag([SUPER], "Button1", 
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),

    Drag([SUPER], "Button3", 
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),

    Click([SUPER], "Button2", 
          lazy.window.bring_to_front()),

    Click([SUPER], "Button4", 
          lazy.screen.prev_group()),

    Click([SUPER], "Button5", 
          lazy.screen.next_group()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X
        # client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="iwgtk"),  # Wireless configuration
        Match(wm_class="thunar"),  # Wireless configuration
        Match(wm_class="calcurse"),  # Wireless configuration
    ],
    **layout_theme
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
