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
import re
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import (Click, Drag, DropDown, Group, Key, KeyChord,
                             Match, ScratchPad, Screen)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

###############################################################################
# Globals
WIDGET_FONT = "Font Awesome"
BACKLIGHT_NAME = 'intel_backlight'

# Basic Colors
BLACK = '#111111'
WHITE = '#ffffff'
GREY = '#333333'

# Dracula colors
bg = "#282A36"
fg = "#F8F8F2"
selection = "#44475A"
selection_transparent = "#44475A80"
comment = "#6272A4"
red = "#FF5555"
orange = "#FFB86C"
yellow = "#F1FA8C"
green = "#50fa7b"
purple = "#BD93F9"
cyan = "#8BE9FD"
pink = "#FF79C6"
bright_red = "#FF6E6E"
bright_green = "#69FF94"
bright_yellow = "#FFFFA5"
bright_blue = "#D6ACFF"
bright_magenta = "#FF92DF"
bright_cyan = "#A4FFFF"
bright_white = "#FFFFFF"
menu = "#21222C"
visual = "#3E4452"
gutter_fg = "#4B5263"
nontext = "#3B4048"

# Colors classes
BAR_BACKGROUND = selection_transparent
WIDGET_BG = selection_transparent
WIDGET_FG = bright_white
GROUPBOX_ACTIVE = WHITE
GROUPBOX_INACTIVE = gutter_fg
GROUPBOX_THIS_SCREEN_BORDER = purple
GROUPBOX_OTHER_SCREEN_BORDER = GREY
GROUPBOX_THIS_CURRENT_SCREEN_BORDER = purple
GROUPBOX_OTHER_CURRENT_SCREEN_BORDER = GREY
WINDOW_FOCUSED_BORDER = bright_white
WINDOW_BORDER = visual

# Unicodes - https://fontawesome.com/v5/cheatsheet
UNICODE_NET = ''
UNICODE_AUDIO = ''
UNICODE_BRIGHTNESS = ''
UNICODE_BATTERY = ''
UNICODE_CHARGING = ' '
UNICODE_UPDATES = ''
UNICODE_NO_UPDATES = ''
UNICODE_CLOCK = ""
UNICODE_AGENDA = ""
UNICODE_CLIPBOARD = " Copied"

# Scripts
HOME = os.path.expanduser('~')
SCRIPT_AUTOSTART = f'{HOME}/.config/qtile/autostart.sh'
SCRIPT_POWER_MENU = f"{HOME}/.config/rofi/powermenu/powermenu.sh &"
SCRIPT_APP_MENU = f"{HOME}/.config/rofi/launcher/launcher.sh &"
SCRIPT_WALLPAPER = f"{HOME}/.fehbg"

# Commands
CMD_SCREENSHOT = "flameshot gui"
CMD_REMAP_CAPS = "setxkbmap -option caps:super"
CMD_LOCK_SCREEN = "betterlockscreen -l blur"  # UNUSED
CMD_WIFI_MENU = "iwgtk"
CMD_FILE_MANAGER = "thunar"
CMD_MONITOR_ONLYNOTEBOOK = "autorandr --change onlynotebook"
CMD_MONITOR_ONLYEXTERNAL = "autorandr --change onlyexternal"
CMD_MONITOR_DUAL = "autorandr --change dualmonitor"
CMD_BRIGHTNESS_UP = 'brightnessctl set 5%+'
CMD_BRIGHTNESS_DOWN = 'brightnessctl set 5%-'
CMD_AUDIO_MIC_MUTE = 'pactl set-source-mute @DEFAULT_SOURCE@ toggle'
CMD_AUDIO_MUTE = 'pactl set-sink-mute @DEFAULT_SINK@ toggle'
CMD_AUDIO_UP = 'pactl set-sink-volume @DEFAULT_SINK@ +2%'
CMD_AUDIO_DOWN = 'pactl set-sink-volume @DEFAULT_SINK@ -2%'

###############################################################################
# Utils functions


def cmd_notification(title: str = "Message", msg: str = "", expire=2000):
    """ Return a notfication command """
    return f"notify-send '{title}' '{msg}' --expire-time={expire}"


def bold(text: str):
    """ Return text between bold tags """
    return f'<b>{text}</b>'


def go_to_group(name: str, key: str):
    """ Go to group but keeping it predefined screen """
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return
        if key in '789':
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


def move_window_to_screen(qtile, window, screen):
    """ Moves a window to a screen and focuses it, allowing you to move it """
    window.togroup(screen.group.name)
    qtile.focus_screen(screen.index)
    screen.group.focus(window, True)


@lazy.function
def move_window_to_another_screen(qtile):
    """ Moves a window to another screen """
    index = qtile.current_screen.index
    index = index - 1 if index > 0 else len(qtile.screens) - 1
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])

###############################################################################
# Hooks


@hook.subscribe.screens_reconfigured
def reconfigure_groupbox():
    """ Adapt visible groups depending on number of screens """
    groups_names = [g.name for g in qtile.groups]
    if len(qtile.screens) > 1:
        groupbox1.visible_groups = groups_names[0:6]
    else:
        groupbox1.visible_groups = groups_names


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
        group_name = groups_definitions[7].get("name")
        client.togroup(group_name)
        targetgroup = client.qtile.groups_map.get(group_name)
        targetgroup.cmd_toscreen(toggle=False)


@hook.subscribe.client_new
def modify_window(client):
    """ Follow window on auto-move done when it matches with a group """
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            # there can be multiple instances of a group
            targetgroup = client.qtile.groups_map[group.name]
            targetgroup.cmd_toscreen(toggle=False)
            break

###############################################################################
# Keys - NOT ALL KEYS ARE SPECIFIED IN THIS SECTIONS


mod = "mod4"  # Super key
ALT = "mod1"  # ALT key
terminal = guess_terminal()

keys = [

    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),

    Key([mod, "control"], "r",
        lazy.reload_config(),
        desc="Reload the config"),

    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"),

    Key([mod], 'n',
        lazy.screen.next_group(),
        desc='Next group'),

    Key([mod], 'b',
        lazy.screen.prev_group(),
        desc='Next group'),

    Key([mod], "Tab",
        lazy.next_layout(),
        desc='Next layout'),

    Key([mod, "shift"], "Tab",
        lazy.prev_layout(),
        desc="Previous layout"),

    Key([], "XF86MonBrightnessUp", lazy.spawn(
        CMD_BRIGHTNESS_UP), desc='Increase brightness'),
    Key([], "XF86MonBrightnessDown", lazy.spawn(
        CMD_BRIGHTNESS_DOWN), desc='Decrease brightness'),
    Key([], "XF86AudioMicMute", lazy.spawn(
        CMD_AUDIO_MIC_MUTE), desc='Mute microphone'),
    Key([], "XF86AudioMute", lazy.spawn(CMD_AUDIO_MUTE), desc='Mute audio'),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        CMD_AUDIO_UP), desc='Increase audio volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        CMD_AUDIO_DOWN), desc='Decrease audio volume'),

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),

    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to left"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window right"),

    Key([mod], "g", lazy.layout.grow_main(),
        desc="Grow main panel (Useful for specific layouts)"),

    Key([mod, "shift"], "g",
        lazy.layout.shrink_main(),
        desc="Shrink main panel (Useful for specific layouts)"),

    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"),

    Key([mod], 'm',
        lazy.next_screen(),
        desc='Change focused screen'),

    Key([mod, 'control'], '0',
        lazy.spawn(CMD_MONITOR_ONLYNOTEBOOK),
        lazy.spawn(
            cmd_notification("Screens", "Using only notebook screen", 4000)),
        desc='Use only notebook screen'),

    Key([mod, 'control'], '1',
        lazy.spawn(CMD_MONITOR_ONLYEXTERNAL),
        lazy.spawn(
            cmd_notification("Screens", "Using only external screen", 4000)),
        desc='Use only external screen'),

    Key([mod, 'control'], '2',
        lazy.spawn(CMD_MONITOR_DUAL),
        lazy.spawn(cmd_notification("Screens", "Using both screens", 4000)),
        desc='Use both screens, notebook and external'),

    Key([mod, 'control'], 'w',
        lazy.spawn(SCRIPT_WALLPAPER),
        lazy.spawn(cmd_notification("Screens", "Wallpaper fixed", 4000)),
        desc='Update wallpaper position'),

    Key([mod], "space",
        lazy.spawn(SCRIPT_APP_MENU),
        desc="Launch app menu"),

    Key([mod], "p",
        lazy.spawn(SCRIPT_POWER_MENU),
        desc="Launch power menu"),

    Key([], "Print",
        lazy.spawn(CMD_SCREENSHOT),
        desc='Launch screenshot menu'),

    # Settings Menu
    KeyChord([mod], "Equal", [

        # Audio submenu
        KeyChord([], "a", [
            Key([], "j", lazy.spawn(CMD_AUDIO_DOWN)),
            Key([], "k", lazy.spawn(CMD_AUDIO_UP)),
            Key([], "m", lazy.spawn(CMD_AUDIO_MUTE))
        ], mode='Audio'),

        # Brightness submenu
        KeyChord([], "b", [
            Key([], "j", lazy.spawn(CMD_BRIGHTNESS_DOWN)),
            Key([], "k", lazy.spawn(CMD_BRIGHTNESS_UP))
        ], mode='Brightness'),

        # Wi-fi submenu
        Key([], "w", lazy.spawn(CMD_WIFI_MENU)),

    ], mode='Settings'),

    Key([mod], "0", lazy.spawn(CMD_REMAP_CAPS)),

    Key([mod], "f", lazy.window.disable_floating()),
]

###############################################################################
# Groups - Workspaces
regex_notion = re.compile(".*Notion.*")
regex_qutebrowser = re.compile(".*qutebrowser.*")
regex_firefox = re.compile(".*Firefox.*")
regex_postman = re.compile(".*Postman.*")
regex_alacritty = re.compile(".*Alacritty.*")
regex_beekeper = re.compile(".*beekeeper.*")

groups_definitions = [
    {"name": " ₁", "key": "1", "layout": "monadtall", "matches": [
        Match(title=regex_qutebrowser), Match(title=regex_firefox)]},
    {"name": " ₂", "key": "2", "layout": "monadtall", "matches": []},
    {"name": " ₃", "key": "3", "layout": "monadtall", "matches": []},
    {"name": " ₄", "key": "4", "layout": "monadtall", "matches": []},
    {"name": " ₅", "key": "5", "layout": "monadtall", "matches": []},
    {"name": " ₆", "key": "6", "layout": "monadtall",
        "matches": [Match(title=regex_postman)]},
    {"name": " ₇", "key": "7", "layout": "max",
        "matches": [Match(title=regex_notion)]},
    {"name": " ₈", "key": "8", "layout": "max", "matches": []},
    {"name": " ₉", "key": "9", "layout": "max", "matches":
        [Match(wm_class='discord')]}]

groups = []
for group_dict in groups_definitions:
    group_name = group_dict.get("name", "")
    group_key = group_dict.get("key", "")

    group = Group(
        name=group_name,
        matches=group_dict.get("matches"),
        layout=group_dict.get("layout"))
    groups.append(group)

    go_to_group_key = Key(
        [mod], group_key,
        lazy.function(go_to_group(group_name, group_key)),
        desc="go to specified group")

    move_to_group_key = Key(
        [mod, "shift"], group_key,
        lazy.window.togroup(group_name),
        lazy.group[group_name].toscreen(),
        desc="move window to specified group")

    keys.append(go_to_group_key)
    keys.append(move_to_group_key)

    for i in range(MONITORS):
        keys.append(
            Key([mod, "shift"], "m",
                move_window_to_another_screen(),
                desc="move window to current group of another screen"))

###############################################################################
# ScratchPads

groups.append(
    ScratchPad('scratchpad', [
        DropDown('terminal', terminal, width=0.6, height=0.7, x=0.2, y=0.15),
        DropDown('files', CMD_FILE_MANAGER, width=0.6,
                 height=0.7, x=0.2, y=0.15),
    ]))

keys.extend([
    Key(["control"], "Return",
        lazy.group["scratchpad"].dropdown_toggle('terminal')),
    Key([mod], "e", lazy.group["scratchpad"].dropdown_toggle('files'))
])


###############################################################################
# Layouts

# Default theme for layouts
layout_theme = dict(
    border_width=2,
    border_focus=WINDOW_FOCUSED_BORDER,
    border_normal=WINDOW_BORDER,
    margin=8,
    padding=2)

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Stack(num_stacks=2, **layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

###############################################################################
# Widgets

widget_defaults = dict(
    font=WIDGET_FONT,
    fontsize=12,
    padding=5)


groupbox1 = widget.GroupBox(
    active=GROUPBOX_ACTIVE,
    inactive=GROUPBOX_INACTIVE,
    this_screen_border=GROUPBOX_THIS_SCREEN_BORDER,
    other_screen_border=GROUPBOX_OTHER_SCREEN_BORDER,
    this_current_screen_border=GROUPBOX_THIS_CURRENT_SCREEN_BORDER,
    other_current_screen_border=GROUPBOX_OTHER_CURRENT_SCREEN_BORDER,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=3,
    **widget_defaults)

groupbox2 = widget.GroupBox(
    active=GROUPBOX_ACTIVE,
    inactive=GROUPBOX_INACTIVE,
    this_screen_border=GROUPBOX_THIS_SCREEN_BORDER,
    other_screen_border=GROUPBOX_OTHER_SCREEN_BORDER,
    this_current_screen_border=GROUPBOX_THIS_CURRENT_SCREEN_BORDER,
    other_current_screen_border=GROUPBOX_OTHER_CURRENT_SCREEN_BORDER,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=3,
    visible_groups=[
        groups_definitions[6].get("name"),
        groups_definitions[7].get("name"),
        groups_definitions[8].get("name"),
    ],
    **widget_defaults)

main_top_widgets = [

    widget.Clipboard(
        fmt=bold(UNICODE_CLIPBOARD),
        max_width=2,
        background=bright_cyan,
        foreground=BLACK,
        **widget_defaults),

    widget.Spacer(5),


    widget.CurrentLayoutIcon(
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        scale=0.8,
        **widget_defaults),

    widget.WindowCount(background=WIDGET_BG, show_zero=True),


    widget.Spacer(5),
    widget.Sep(),
    widget.Spacer(5),

    # Memory
    widget.TextBox(
        bold('RAM'),
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        **widget_defaults),

    widget.Memory(
        format='{MemUsed: .3f}{mm} / {MemTotal: .3f}{mm}',
        measure_mem='G',
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        **widget_defaults),

    widget.Spacer(5),
    widget.Mpris2(
        name="spotify",
        display_metadata=['xesam:title', 'xesam:artist'],
        scroll_chars=None,
        objname="org.mpris.MediaPlayer2.spotify",
        scroll_interval=0,
        background=bright_green,
        foreground=BLACK,
        fmt='{}  ',
        paused_text=' {track}'),


    widget.Spacer(),

    groupbox1,

    widget.Spacer(),

    widget.Chord(background=bright_red, fmt=bold("MODE: ") + "{}"),

    widget.Spacer(10),

    widget.Systray(icon_size=15, padding=15),

    widget.Spacer(20),

    widget.CheckUpdates(
        display_format=bold(UNICODE_UPDATES + " {updates}"),
        colour_have_updates=bright_yellow,
        no_update_string=UNICODE_NO_UPDATES),

    widget.Sep(),

    # Internet
    widget.TextBox(
        bold(UNICODE_NET),
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        **widget_defaults),
    widget.Wlan(
        format='{percent:2.0%}',
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        mouse_callbacks={
            "Button1": lazy.spawn(CMD_WIFI_MENU)
        },
        **widget_defaults),

    widget.Sep(),

    widget.TextBox(bold(UNICODE_AUDIO), background=WIDGET_BG,
                   foreground=WIDGET_FG, **widget_defaults),
    widget.Volume(background=WIDGET_BG,
                  foreground=WIDGET_FG, **widget_defaults),

    widget.Sep(),

    widget.Battery(
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        low_background=bright_red,
        low_foreground=WHITE,
        low_percentage=0.40,
        notify_below=40,
        charge_char=UNICODE_CHARGING,
        discharge_char='',
        show_short_text=True,
        format=UNICODE_BATTERY + '  {percent:2.0%} {char}'),

    widget.Sep(),

    widget.Clock(
        format=f"{UNICODE_AGENDA}  %d/%m/%Y  %H:%M",
        background=WIDGET_BG,
        foreground=WIDGET_FG),

]  # main_top_widgets END

secondary_widgets = [
    widget.Spacer(),
    groupbox2,
    widget.Spacer(),
]

###############################################################################
# Screen and monitors

bar_style = dict(
    background=BAR_BACKGROUND,
    border_color=BAR_BACKGROUND,
    margin=[10, 10, 10, 10])

screens = []
for monitor in range(MONITORS):
    if monitor == 0:
        # Primary monitor
        screens.append(Screen(
            top=bar.Bar(
                widgets=main_top_widgets, size=35, **bar_style)))
    else:
        # Secondary monitors
        screens.append(Screen(
            top=bar.Bar(
                widgets=secondary_widgets, size=30, **bar_style)))

###############################################################################
# MORE

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
