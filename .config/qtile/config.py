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
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.utils import guess_terminal
from libqtile.lazy import lazy

#############
# "GLOBALS" #
#############

# COLOR NAMES
BLACK = '#111111'
WHITE = '#ffffff'
BLUE = '#87a1ed'
BLUE_REGULAR = "#274472"
BLUE_PASTEL = '#89b4fa'
BLUE_PASTEL1 = '#45475a'
BLUE_PASTEL2 = '#585b70'
BLUE_DARK = '#1e1e2e'
GREY = '#333333'
GREY_LIGHT = '#555555'
GREY_PASTEL = '#a6adc8'
RED = '#cb2424'
YELLOW = '#ffc002'
YELLOW_PASTEL = '#c9b57c'
YELLOW_DARK = '#57551E'
GREEN='#40a02b'
GREEN_PASTEL = 'a6e3a1'
GREEN_DARK = '#1e5553'
PURPLE = '#4343f4'
PURPLE_SOFT = '#66669c'

# COLORS CLASSES
BAR_BACKGROUND=BLUE_DARK
WIDGET_BG=PURPLE_SOFT
WIDGET_FG=WHITE
GROUPBOX_ACTIVE=WHITE
GROUPBOX_INACTIVE=GREY
GROUPBOX_THIS_SCREEN_BORDER=PURPLE
GROUPBOX_OTHER_SCREEN_BORDER=PURPLE_SOFT
GROUPBOX_THIS_CURRENT_SCREEN_BORDER=PURPLE
GROUPBOX_OTHER_CURRENT_SCREEN_BORDER=PURPLE_SOFT
WINDOW_FOCUSED_BORDER = WHITE
WINDOW_BORDER = BLACK

# UNICODES
UNICODE_NET = ''
UNICODE_AUDIO = ''
UNICODE_BRIGHTNESS = ''
UNICODE_BATTERY = ''
UNICODE_UPDATES = ''
UNICODE_NO_UPDATES = ''
UNICODE_CLOCK = ""
UNICODE_CURRENT_SCREEN = "   "
UNICODE_NOT_CURRENT_SCREEN= ""
UNICODE_AGENDA = ""

# NAMES
BACKLIGHT_NAME='intel_backlight'
GROUP_1_NAME = "  HOME ₁"
GROUP_2_NAME = "  CODE ₂"
GROUP_3_NAME = "  TERM ₃"
GROUP_4_NAME = "  FOLDER ₄"
GROUP_5_NAME = "  DOCS ₅"
GROUP_6_NAME = "  VIDEO ₆"
GROUP_7_NAME = "  NOTES ₇"
GROUP_8_NAME = "阮 MUSIC ₈"
GROUP_9_NAME = "  CHAT ₉"

# SCRIPTS
HOME = os.path.expanduser('~')
SCRIPT_AUTOSTART = f'{HOME}/.config/qtile/autostart.sh'
SCRIPT_POWER_MENU = f"{HOME}/.config/rofi/powermenu/type-2/powermenu.sh &"
SCRIPT_APP_MENU =  f"{HOME}/.config/rofi/launchers/type-3/launcher.sh &"
SCRIPT_SCREENSHOT = f"{HOME}/.config/rofi/applets/bin/screenshot.sh &"
SCRIPT_WALLPAPER = f"{HOME}/.fehbg"

# COMMANDS
CMD_LOCK_SCREEN = "betterlockscreen -l blur"
CMD_SET_BRIGHTNESS = "brightnessctl s {}%"
CMD_WIFI_MENU = "iwgtk"
CMD_FILE_MANAGER = "alacritty -e ranger"
CMD_MONITOR_ONLYNOTEBOOK = "autorandr --change onlynotebook"
CMD_MONITOR_ONLYEXTERNAL = "autorandr --change onlyexternal"
CMD_MONITOR_DUAL = "autorandr --change dualmonitor"
CMD_BRIGHTNESS_UP = 'xbacklight -inc 5'
CMD_BRIGHTNESS_DOWN = 'xbacklight -dec 5'
CMD_AUDIO_MIC_MUTE = 'pactl set-source-mute @DEFAULT_SOURCE@ toggle'
CMD_AUDIO_MUTE = 'pactl set-sink-mute @DEFAULT_SINK@ toggle'
CMD_AUDIO_UP = 'pactl set-sink-volume @DEFAULT_SINK@ +2%'
CMD_AUDIO_DOWN = 'pactl set-sink-volume @DEFAULT_SINK@ -2%'
CMD_OPEN_AGENDA = 'qutebrowser ":quickmark-load ag"' # Needs qutebrowser 'ag' quickmark mapped 


###################
# Utils functions #
###################

def bold(text: str):
    """ Return text between bold tags """
    return f'<b>{text}</b>'

def go_to_group(name: str, key: str):
    """ Go to group but keeping it predefined screen """
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return
        if key in '6789':
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

#########
# HOOKS #
#########

@hook.subscribe.startup_once
def autostart():
    """ Executes a script on qtile startup """
    subprocess.Popen([SCRIPT_AUTOSTART])

@hook.subscribe.screens_reconfigured
async def _():
    """ Update groupbox config depending on screens length """
    if len(qtile.screens) > 1:
        groupbox1.visible_groups = [GROUP_1_NAME, GROUP_2_NAME, GROUP_3_NAME, GROUP_4_NAME, GROUP_5_NAME]
        groupbox1.hide_unused = False
    else:
        groupbox1.visible_groups = [GROUP_1_NAME, GROUP_2_NAME, GROUP_3_NAME, GROUP_4_NAME, GROUP_5_NAME, GROUP_6_NAME, GROUP_7_NAME, GROUP_8_NAME, GROUP_9_NAME]
    if hasattr(groupbox1, 'bar'):
        groupbox1.bar.draw()

##################
# KEYS/SHORTCUTS #
##################

mod = "mod4"  # Super (or Windows) key
ALT = "mod1"
terminal = guess_terminal()

keys = [

    # KEYS: BASIC
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),

    Key([mod, "control"], "r",
        lazy.reload_config(),
        desc="Reload the config"),

    Key([mod], "Return", 
        lazy.spawn(terminal), 
        desc="Launch terminal"),
 
    Key([mod], "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    Key([mod, ALT], 'l', 
        lazy.screen.next_group(), 
        desc='Next group'),
    
    Key([mod, ALT], 'h',
        lazy.screen.prev_group(), 
        desc='Next group'),

    Key([mod], "Tab",
        lazy.next_layout(),
        desc='Next layout'),

    Key([mod, "shift"], "Tab",
        lazy.prev_layout(),
        desc="Previous layout"),


    # KEYS: DEVICE CONTROL
    Key([], "XF86MonBrightnessUp",   lazy.spawn(CMD_BRIGHTNESS_UP), desc='Increase brightness'),
    Key([], "XF86MonBrightnessDown", lazy.spawn(CMD_BRIGHTNESS_DOWN), desc='Decrease brightness'),

    Key([], "XF86AudioMicMute",     lazy.spawn(CMD_AUDIO_MIC_MUTE), desc='Mute microphone'),
    Key([], "XF86AudioMute",        lazy.spawn(CMD_AUDIO_MUTE), desc='Mute audio'),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(CMD_AUDIO_UP), desc='Increase audio volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn(CMD_AUDIO_DOWN), desc='Decrease audio volume'),

    # KEYS: WINDOWS
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to left"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    
    Key([mod], "g", lazy.layout.grow(),
        lazy.layout.increase_nmaster(), 
        desc="Grow main panel (Useful for specific layouts)"),
    
    Key([mod, "shift"], "g",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink main panel (Useful for specific layouts)"),

    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"),

    # KEYS: SCREEN
    Key([mod], 'm', 
        lazy.next_screen(), 
        desc='Change focused screen'),
 
    Key([mod, 'control'], '0', lazy.spawn(CMD_MONITOR_ONLYNOTEBOOK), desc='Use only notebook screen' ),
    Key([mod, 'control'], '1', lazy.spawn(CMD_MONITOR_ONLYEXTERNAL), desc='Use only external screen'),
    Key([mod, 'control'], '2', lazy.spawn(CMD_MONITOR_DUAL), desc='Use both screens, notebook and external'),
    Key([mod, 'control'], 'w', lazy.spawn(SCRIPT_WALLPAPER), desc='Update wallpaper position'),

    KeyChord([mod], "b", [
        Key([], "k", lazy.hide_show_bar(position='top'), desc="Show/Hide top bar"),
        Key([], "j", lazy.hide_show_bar(position='bottom'), desc='Show/Hide bottom bar')],
        mode="BAR MODE"),

    # KEYS: MENUS / PROGRAMS/ LAUNCHERS
    KeyChord([mod], "o", [
        KeyChord([], "a", [
                Key([], "g", lazy.spawn(CMD_OPEN_AGENDA))],
                mode='OPEN A')],
        mode='OPEN'
    ),

    Key([mod], "space",
        lazy.spawn(SCRIPT_APP_MENU),
        desc="Launch app menu"),

    Key([mod], "p",
        lazy.spawn(SCRIPT_POWER_MENU),
        desc="Launch power menu"),

    Key([], "Print",
        lazy.spawn(SCRIPT_SCREENSHOT),
        desc='Launch screenshot menu'),

    # File manager
    Key([mod], "e", 
        lazy.spawn(CMD_FILE_MANAGER),
        desc='Launch file manager'),
]

#####################
# GROUPS/WORKSPACES #
#####################
workspaces = [
        {"name": GROUP_1_NAME, "key": "1","layout": "monadtall", "matches": []},
        {"name": GROUP_2_NAME, "key": "2","layout": "monadtall", "matches": []},
        {"name": GROUP_3_NAME, "key": "3","layout": "matrix", "matches": []},
        {"name": GROUP_4_NAME, "key": "4","layout": "columns", "matches": []},
        {"name": GROUP_5_NAME, "key": "5","layout": "max", "matches": [Match(wm_class='libreoffice')]},
        {"name": GROUP_6_NAME, "key": "6","layout": "columns", "matches": []},
        {"name": GROUP_7_NAME, "key": "7","layout": "columns", "matches": []},
        {"name": GROUP_8_NAME, "key": "8","layout": "max", "matches": []},
        {"name": GROUP_9_NAME, "key": "9","layout": "max", "matches": [Match(wm_class='discord')]}]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    layouts = workspace["layout"] if "layout" in workspace else None
    group = Group(workspace["name"], matches=matches, layout=layouts)
    groups.append(group)

    keys.append(Key([mod], workspace["key"],
                lazy.function(go_to_group(workspace['name'], workspace['key'])),
                desc="Go to specified group"))
    
    keys.append(Key([mod, "shift"], workspace["key"],
                lazy.window.togroup(workspace["name"]),
                lazy.group[workspace["name"]].toscreen(),
                desc="Move window to specified group"))

    for i in range(MONITORS):
        keys.append(Key([mod, "shift"], "m", 
                    move_window_to_another_screen(),
                    desc="Move window to current group of another screen"))

###########
# LAYOUTS #
###########

# Default theme for layouts
layout_theme = dict(
    border_width=2,
    border_focus=WINDOW_FOCUSED_BORDER,
    border_normal=WINDOW_BORDER,
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
    borderwidth=1,
    **widget_defaults)


main_top_widgets = [
    
    widget.Clipboard(background=WIDGET_BG, max_width=100, fmt='Copied: {}', **widget_defaults),

    widget.Spacer(), 
    
    # Music
    widget.Mpris2(
        name="spotify",
        display_metadata=['xesam:title', 'xesam:artist'],
        scroll_chars=None,
        objname="org.mpris.MediaPlayer2.spotify",
        scroll_interval=0,
        background=GREEN_PASTEL,
        foreground=BLACK,
        fmt='  {}',
        paused_text='Paused: {track}'),
    widget.Spacer(2),

    # DISK
    widget.DF(partition='/', background=WIDGET_BG, fmt=bold('DISK') + '   {}', visible_on_warn=False, format="{s}{m} Total | {f}{m} Free", **widget_defaults),
    widget.Spacer(2),

    # CPU
    widget.TextBox(bold('CPU'), background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.CPU(format='{freq_current}GHz {load_percent}%', background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Spacer(2),

    # Memory
    widget.TextBox(bold('RAM'), background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Memory(format='{MemUsed: .3f}{mm} |{MemTotal: .3f}{mm}', measure_mem='G', background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Spacer(2),

    # Internet
    widget.TextBox(bold(UNICODE_NET), background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Wlan(
        format='{essid} {percent:2.0%}',
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        mouse_callbacks={
            "Button1": lazy.spawn(CMD_WIFI_MENU)
        },
        **widget_defaults),
    widget.Spacer(2),
    
    # Volume control
    widget.TextBox(bold(UNICODE_AUDIO), background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Volume(background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Spacer(2),

    # Brightness/Backlight control
    widget.TextBox(UNICODE_BRIGHTNESS, background=WIDGET_BG, foreground=WIDGET_FG, **widget_defaults),
    widget.Backlight(
        backlight_name=BACKLIGHT_NAME,
        change_command=CMD_SET_BRIGHTNESS,
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        **widget_defaults),

] # main_top_widgets END



main_bottom_widgets = [
    
    widget.Chord(background=GREEN),
    widget.Spacer(5),

    widget.CurrentLayoutIcon(
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        scale=0.8,
        **widget_defaults),
    widget.WindowCount(background=GREY, show_zero=True),

    groupbox1,
    widget.Spacer(5),
   
    widget.Prompt(prompt="RUN: ", background=WIDGET_BG, foreground=WIDGET_FG),

    widget.Systray(icon_size=15, padding=15),

    widget.Spacer(),

    widget.CurrentScreen(
        active_text=bold(UNICODE_CURRENT_SCREEN),
        inactive_text=UNICODE_NOT_CURRENT_SCREEN,
        active_color=WHITE,
        inactive_color=GREY_PASTEL),

    widget.Spacer(),

    widget.CheckUpdates(
        display_format=UNICODE_UPDATES + " {updates}",
        colour_have_updates=YELLOW,
        colour_no_updates=GREEN,
        no_update_string=f"{UNICODE_NO_UPDATES}  0"),
    widget.Spacer(5),

    widget.Clock(
            format=f"{UNICODE_AGENDA}  %d/%m/%Y  %H:%M", 
            background=WIDGET_BG, 
            foreground=WIDGET_FG),
    widget.Spacer(2),

    widget.Battery(
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        low_background=RED,
        low_foreground=WHITE,
        low_percentage=0.40,
        notify_below=40,
        charge_char=f' ',
        discharge_char='',
        show_short_text=True,
        format=UNICODE_BATTERY + '  {percent:2.0%} {char}'),
] # main_bottom_widgets END


secondary_bottom_widgets = [

    widget.CurrentLayoutIcon(
        background=WIDGET_BG,
        foreground=WIDGET_FG,
        scale=0.8,
        **widget_defaults),
    widget.WindowCount(background=GREY, show_zero=True),
    widget.Spacer(length=2),

    widget.GroupBox(
        active=GROUPBOX_ACTIVE,
        inactive=GROUPBOX_INACTIVE,
        this_screen_border=GROUPBOX_THIS_SCREEN_BORDER,
        other_screen_border=GROUPBOX_OTHER_SCREEN_BORDER,
        this_current_screen_border=GROUPBOX_THIS_CURRENT_SCREEN_BORDER,
        other_current_screen_border=GROUPBOX_OTHER_CURRENT_SCREEN_BORDER,
        highlight_method='block',
        disable_drag=True,
        hide_unused=False,
        visible_groups=[GROUP_6_NAME, GROUP_7_NAME, GROUP_8_NAME, GROUP_9_NAME],
        borderwidth=1,
        **widget_defaults),
    
    widget.Sep(foreground=BAR_BACKGROUND), 

    widget.Spacer(),

    widget.CurrentScreen(
        active_text=bold(UNICODE_CURRENT_SCREEN),
        inactive_text=UNICODE_NOT_CURRENT_SCREEN,
        active_color=WHITE,
        inactive_color=GREY_PASTEL),

    widget.Spacer(),

    widget.Sep(foreground=BAR_BACKGROUND),
] # secondary_bottom_widgets END

#######################
# SCREEN: TASK BAR #
#######################

bar_style = dict(
    background=BAR_BACKGROUND,
    border_color=BAR_BACKGROUND,
    border_width=[0, 0, 0, 0],
    margin=[0, 0, 0, 0])

screens = []
for monitor in range(MONITORS):
    if monitor == 0:
        # Primary monitor
        screens.append(Screen(
            top=bar.Bar(widgets=main_top_widgets, size=20, **bar_style),
            bottom=bar.Bar(widgets=main_bottom_widgets, size=20, **bar_style)))
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
