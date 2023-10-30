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
import asyncio
import subprocess
from typing import List

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from colors import Catppuccin

#####################
## Utils functions ##
#####################

def go_to_group(name: str):
    """ Go to group but keeping it in predefined screen"""
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return
        if name in '7890':
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


#############
## GLOBALS ##
#############

# Generics
HOME = os.path.expanduser('~')
TERMINAL = "kitty"
MONITORS = get_monitors()

# Style
WIDGET_FONT = "Iosevka Nerd Font"
COLOR = Catppuccin()

# Apps
APP_NOTES = "obsidian"
APP_FILE_MANAGER = "thunar"
APP_SCREENSHOT = "flameshot gui"
APP_AUDIO_SETTINGS = "pavucontrol"
GITHUB_NOTIFICATIONS = 'qutebrowser ":open gh"'

# Script Paths
AUTOSTART = f'{HOME}/.config/qtile/autostart.sh'
MENU_WIFI = f"{HOME}/.config/rofi/wifi/run.sh &" 
MENU_POWER = f"{HOME}/.config/rofi/powermenu/run.sh &" 
MENU_APP = f"{HOME}/.config/rofi/launcher/run.sh &" 
MENU_BROWSER = f"{HOME}/.config/rofi/qutebrowser/run.sh &"
MENU_PROJECT = f"{HOME}/.config/rofi/projects/run.sh &"
MENU_CONFIGS = f"{HOME}/.config/rofi/configs/run.sh &"
MENU_UTILS = f"{HOME}/.config/rofi/utils/run.sh &" 
MENU_SCREENS = f"{HOME}/.config/rofi/autorandr/run.sh &" 
MENU_CLIPBOARD = "copyq show"
WIDGET_BATTERY = f"{HOME}/.local/bin/statusbar/battery-icon.sh" 
WIDGET_INTERNET = f"{HOME}/.local/bin/statusbar/net.sh" 

# Brightness
BACKLIGHT_NAME = 'intel_backlight'
BRIGHTNESS_UP = 'brightnessctl set 5%+'
BRIGHTNESS_DOWN = 'brightnessctl set 5%-'

# Audio
AUDIO_UP = 'pactl set-sink-volume @DEFAULT_SINK@ +2%'
AUDIO_DOWN = 'pactl set-sink-volume @DEFAULT_SINK@ -2%'
AUDIO_MUTE_UNMUTE = 'pactl set-sink-mute @DEFAULT_SINK@ toggle'
AUDIO_MIC_MUTE = 'pactl set-source-mute @DEFAULT_SOURCE@ toggle'

# Reset
RESET_SCREEN = "autorandr --change onlynotebook"

# Modifier 
SUPER = "mod4"
ALT = "mod1"

####################
## Lazy functions ##
####################

@lazy.function
def move_window_to_next_screen(qtile):
    """ Moves a window to a screen and focuses it, allowing you to move it """
    window = qtile.current_window
    qtile.cmd_next_screen()
    window.togroup(qtile.current_screen.group.name)

##########
## Keys ##
##########

keys = [

    # F Keys
    Key([SUPER], "F4", lazy.spawn(RESET_SCREEN), desc='Reset screen'),

    # Qtile basics
    Key([SUPER], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    # Change Layouts
    Key([SUPER], "Tab", lazy.next_layout(), desc='Next layout'),
    Key([SUPER, "shift"], "Tab", lazy.prev_layout(), desc="Previous layout"),

    # Laptop keys
    Key([], "XF86MonBrightnessUp", lazy.spawn(BRIGHTNESS_UP), desc='Increase brightness'),
    Key([], "XF86MonBrightnessDown", lazy.spawn(BRIGHTNESS_DOWN), desc='Decrease brightness'),
    Key([], "XF86AudioMicMute", lazy.spawn(AUDIO_MIC_MUTE), desc='Mute microphone'),
    Key([], "XF86AudioMute", lazy.spawn(AUDIO_MUTE_UNMUTE), desc='Mute audio'),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(AUDIO_UP), desc='Increase audio volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn(AUDIO_DOWN), desc='Decrease audio volume'),

    # Move focus
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], 'm', lazy.next_screen(), desc='Change focused screen'), 
    Key([SUPER], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([SUPER], "f", lazy.window.disable_floating(), desc="Disable floating behavior for focused window"),
    Key([SUPER], "n", lazy.screen.next_group(skip_empty=True), desc="Go to next group"),
    Key([SUPER], "p", lazy.screen.prev_group(skip_empty=True), desc="Go to previous group"),
    Key([SUPER], "t", lazy.screen.toggle_group(), desc="Open Wi-Fi Menu"),

    # Move window
    Key([SUPER, "shift"], "m", move_window_to_next_screen(), desc="Move window to next screen group"),
    Key([SUPER, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([SUPER, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([SUPER, "shift"], "f", lazy.layout.flip()),
    
    # Window Resizes 
    Key([SUPER, "control"], "h", lazy.layout.grow_left(), desc="Grow window to left"),
    Key([SUPER, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([SUPER, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([SUPER, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),

    # Layout resizes
    Key([SUPER], "r", lazy.layout.reset()),
    Key([SUPER], "g", lazy.layout.maximize()),
    Key([SUPER], "i", lazy.layout.grow()),
    Key([SUPER, "shift"], "i", lazy.layout.shrink()),
 
    # Menus
    Key([SUPER], "space", lazy.spawn(MENU_APP), desc="Open App Menu"),
    Key([SUPER], "c", lazy.spawn(MENU_CONFIGS), desc="Open Configs Menu"),
    Key([SUPER], "o", lazy.spawn(MENU_PROJECT), desc="Open Projects Menu"),
    Key([SUPER, "shift"], "p", lazy.spawn(MENU_POWER), desc="Open Power Menu"),
    Key([SUPER], "s", lazy.spawn(MENU_BROWSER), desc="Open Qutebrowser Menu"),
    Key([SUPER], "u", lazy.spawn(MENU_UTILS), desc="Open Utils Menu"),
    Key([SUPER], "w", lazy.spawn(MENU_WIFI),desc="Open Wi-Fi Menu"),
    Key([SUPER], "t", lazy.screen.toggle_group(), desc="Open Wi-Fi Menu"),
    Key([SUPER], "v", lazy.spawn(MENU_CLIPBOARD), desc="Open Clipboard Menu"),
    Key([SUPER], "a", lazy.spawn(MENU_SCREENS), desc="Open Screen Profile Menu"),
    Key([SUPER, "control"], "s", lazy.spawn("copyq show"), desc="Open Wi-Fi Menu"),
    
    # Launch
    Key([], "Print", lazy.spawn(APP_SCREENSHOT), desc='Launch screenshot'),

    # Settings Menu
    KeyChord([SUPER], "Equal", [
        # Audio submenu
        KeyChord([], "a", [
                Key([], "k", lazy.spawn(AUDIO_UP), desc="Increase audio volume"),
                Key([], "j", lazy.spawn(AUDIO_DOWN), desc="Decrease audio volume"),
                Key([], "m", lazy.spawn(AUDIO_MUTE_UNMUTE), desc="Toggle mute")
            ], 
            name='Audio Volume:    j -> Decrease   k -> Increase   m -> Mute',
            mode=True),

        # Brightness submenu
        KeyChord([], "b", [
                Key([], "k", lazy.spawn(BRIGHTNESS_UP), desc="Increase brightness"),
                Key([], "j", lazy.spawn(BRIGHTNESS_DOWN), desc="Descrease brightness")
            ], 
            name='Brightness:   j -> Decrease   k -> Increase',
            mode=True),

        ],
        name="Configuration:    a -> Audio   b -> Brightness",
        mode=False
    ),
]

#########################
## Groups - Workspaces ##
#########################

groups: List[Group] = [
        Group("1", label="  ₁", layout="monadtall", matches=[Match(wm_class="firefox"),Match(wm_class="qutebrowser")]),
        Group("2", label="  ₂", layout="monadtall", matches=[]),
        Group("3", label="  ₃", layout="monadtall", matches=[]), 
        Group("4", label="  ₄", layout="monadtall", matches=[]), 
        Group("5", label="  ₅", layout="monadtall", matches=[]), 
        Group("6", label="  ₆", layout="monadtall", matches=[]), 
        Group("7", label="  ₇", layout="max", matches=[Match(wm_class="Postman"), Match(wm_class="beekeeper-studio")]), 
        Group("8", label="  ₈", layout="max", matches=[]), # Spotify match are manually defined in hooks
        Group("9", label=" ₉", layout="max", matches=[Match(wm_class="discord")]), 
        Group("0", label="  ₀", layout="max", matches=[Match(wm_class="notion-app"), Match(wm_class="Logseq")]), 
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

#################
## ScratchPads ##
#################

groups.append(
    ScratchPad('scratchpad', [
        DropDown('notes', APP_NOTES, width=0.8, height=0.9, x=0.08, y=0.05, on_focus_lost_hide=False),
        DropDown('file_manager', APP_FILE_MANAGER, width=0.8, height=0.9, x=0.08, y=0.05, on_focus_lost_hide=False),
    ]))

keys.extend([
    Key([SUPER, "shift"], "n", lazy.group["scratchpad"].dropdown_toggle('notes')),
    Key([SUPER], "e", lazy.group["scratchpad"].dropdown_toggle('file_manager'))
])


#############
## Layouts ##
#############

# Default params for layouts
layout_theme = dict(
    border_focus=COLOR.window_focused_border,
    border_normal=COLOR.window_border,
    margin=20,
    padding=2
)

layouts = [
    layout.Max(**layout_theme, border_width=0),
    layout.MonadTall(**layout_theme, border_width=1, single_border_width=0),
    layout.MonadWide(**layout_theme, border_width=1, single_border_width=0, ratio=0.75),
    # layout.Zoomy(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Stack(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Floating(**layout_style),
]

#############
## Widgets ##
#############

decorations=[RectDecoration(group=True, use_widget_background=True, clip=True, radius=5, filled=True, padding_y=0, padding_x=0)]
decorations_github=[RectDecoration(group=True, use_widget_background=True, clip=True, radius=14, filled=True)]

widget_defaults = dict(
    font=WIDGET_FONT,
    fontsize=14,
    padding=8)


icons_defaults = dict(
    font=WIDGET_FONT,
    fontsize=14,
    padding=10)
 

main_groupbox = widget.GroupBox(
    active=COLOR.groupbox_active,
    background=COLOR.groupbox_background,
    inactive=COLOR.groupbox_inactive,
    this_screen_border=COLOR.groupbox_this,
    other_screen_border=COLOR.groupbox_other,
    this_current_screen_border=COLOR.groupbox_this_current,
    other_current_screen_border=COLOR.groupbox_other_current,
    highlight_method='line',
    highlight_color=[COLOR.groupbox_this, COLOR.groupbox_this],
    disable_drag=True,
    hide_unused=True,
    borderwidth=1,
    decorations=decorations,
    padding=12)


secondary_groupbox = widget.GroupBox(
    active=COLOR.groupbox_active,
    background=COLOR.groupbox_background,
    inactive=COLOR.groupbox_inactive,
    this_screen_border=COLOR.groupbox_this,
    other_screen_border=COLOR.groupbox_other,
    this_current_screen_border=COLOR.groupbox_this_current,
    other_current_screen_border=COLOR.groupbox_other_current,
    highlight_method='line',
    highlight_color=[COLOR.groupbox_this, COLOR.groupbox_this],
    disable_drag=True,
    hide_unused=True,
    borderwidth=1,
    decorations=decorations,
    padding=12,
    visible_groups=[
        groups[6].name,
        groups[7].name,
        groups[8].name,
        groups[9].name,
    ])


main_top_widgets = [
    
    widget.Spacer(15),

    widget.TextBox(" ", fontsize=20, foreground="#08F"),

    widget.Spacer(5),

    widget.CurrentLayoutIcon(
        background=COLOR.current_layout.bg,
        foreground=COLOR.current_layout.fg,
        decorations=decorations,
        scale=0.8),

    widget.WindowCount(
         background=COLOR.window_count.bg, 
         foreground=COLOR.window_count.fg, 
         show_zero=True,
         decorations=decorations),

    widget.Spacer(5),

    main_groupbox,

    widget.Spacer(10),
    
    widget.Mpris2(
        name="spotify",
        display_metadata=['xesam:title', 'xesam:artist'],
        scroll_chars=None,
        objname="org.mpris.MediaPlayer2.spotify",
        scroll_interval=0,
        background=COLOR.spotify.bg,
        foreground=COLOR.spotify.fg,
        fmt='{}   ',
        paused_text='   {track}',
        mouse_callbacks={
            "Button3": lazy.function(go_to_group("8"))
        },
        decorations=decorations
    ),

    widget.Spacer(5),

    widget.Clipboard(
        fmt="󰅎  Copied",
        max_width=2,
        background=COLOR.clipboard.bg,
        foreground=COLOR.clipboard.fg,
        decorations=decorations,
        **widget_defaults),

    widget.Spacer(),
 
    widget.Chord(
        font="Iosevka NF ", 
        background=COLOR.chord.bg, 
        foreground=COLOR.chord.fg, 
        fmt=(" ") + "{}" + "   Esc -> Cancel"
    ),
   
    widget.Spacer(),

#     widget.CPU(
#        background=COLOR.cpu.bg,
#        foreground=COLOR.cpu.fg,
#        decorations=decorations
#    ),
#
#    widget.Spacer(5),
# 
#    widget.Memory(
#        format='RAM {MemUsed: .3f}{mm} / {MemTotal: .3f}{mm}',
#        measure_mem='G',
#        background=COLOR.ram.bg,
#        foreground=COLOR.ram.fg,
#        decorations=decorations,
#        **widget_defaults),
#
#   widget.Spacer(5),

    widget.CheckUpdates(
        display_format="  {updates}",
        colour_have_updates=COLOR.check_updates.fg,
        background=COLOR.check_updates.bg,
        no_update_string="",
        decorations=decorations),

    widget.Spacer(5),

    # Internet Widget
    widget.GenPollText(
        func=lambda: subprocess.check_output(WIDGET_INTERNET).decode(),
        update_interval=1, 
        background=COLOR.Green,
        foreground=COLOR.Crust,
        decorations=decorations,
        max_chars=20,
        **widget_defaults
    ),

    widget.Spacer(5),
    
    widget.Volume(
        fmt="  {}",
        background=COLOR.audio.bg,
        foreground=COLOR.audio.fg, 
        mouse_callbacks={
            "Button3": lazy.spawn(APP_AUDIO_SETTINGS)
        },
        decorations=decorations,
        **widget_defaults),

    widget.Spacer(5),
    
    # Battery Widget
    widget.GenPollText(
        func=lambda: subprocess.check_output(WIDGET_BATTERY).decode(),
        update_interval=1, 
        background=COLOR.battery_icon.bg,
        foreground=COLOR.battery_icon.fg,
        decorations=decorations,
        **icons_defaults
    ),
    
    widget.Battery(
        background=COLOR.battery.bg,
        foreground=COLOR.battery.fg,
        low_background=COLOR.battery_low.bg,
        low_foreground=COLOR.battery_low.fg,
        low_percentage=0.40,
        notify_below=20,
        charge_char="  ",
        full_char="  ",
        discharge_char="",
        unknown_char="? ",
        show_short_text=False,
        decorations=decorations,
        format='{char}',
        padding=0
    ),

    widget.Spacer(5),

    widget.Clock(
        format=f"󰥔  %H:%M:%S | %d/%m/%y",
        background=COLOR.clock.bg,
        foreground=COLOR.clock.fg,
        decorations=decorations,
        mouse_callbacks={},
        **widget_defaults
    ),

    widget.Systray(),

    widget.Spacer(10),

    widget.GithubNotifications(
        active_colour=COLOR.github_active,
        inactive_colour=COLOR.github_inactive,
        error_colour=COLOR.github_error,
        background=COLOR.github_background,
        token_file=f"{HOME}/.github-token",
        icon_size=23,
        decorations=decorations_github,
        mouse_callbacks={
            "Button1": lazy.spawn(GITHUB_NOTIFICATIONS)
        },
        padding=2),

    widget.Spacer(25),

]


secondary_top_widgets = [
    widget.Spacer(10),
    
    widget.CurrentLayoutIcon(
        background=COLOR.current_layout.bg,
        foreground=COLOR.current_layout.fg,
        decorations=decorations,
        scale=0.8),

    widget.WindowCount(
         background=COLOR.window_count.bg, 
         foreground=COLOR.window_count.fg, 
         show_zero=True,
         decorations=decorations),

    widget.Spacer(5),

    secondary_groupbox,

    widget.Spacer()
]

#########################
## Screen and monitors ##
#########################

bar_style = dict(
    background=COLOR.bar.bg,
    border_color=COLOR.bar.bg,
    margin=[8, 0, 0, 0],
    border_width=0)

main_bar = bar.Bar(widgets=main_top_widgets, size=25, **bar_style)
secondary_bar = bar.Bar(widgets=secondary_top_widgets, size=25, **bar_style)

screens = []
for monitor in range(MONITORS):

    if monitor == 0:
        # Primary monitor
        screens.append(Screen(top=main_bar))

    else:
        # Secondary monitors
        screens.append(Screen(top=secondary_bar))


###########
## Hooks ##
###########

@hook.subscribe.startup
def startup():
    """ Execute some steps in qtile refresh """
    # Reload groupbox
    reconfigure_groupbox()

    # Configuration that makes possible match bars in picom
    main_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    secondary_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    bottom_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)


@hook.subscribe.screens_reconfigured
def reconfigure_groupbox():
    """ Adapt visible groups depending on number of screens """
    groups_names = [g.name for g in qtile.groups]
    if len(qtile.screens) > 1:
        main_groupbox.visible_groups = groups_names[:6]
    else:
        main_groupbox.visible_groups = groups_names


@hook.subscribe.startup_once
def autostart():
    """ Executes a script on qtile startup """
    subprocess.Popen([AUTOSTART])


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
            client.qtile.cmd_simulate_keypress([SUPER], group.name)

##########
## MORE ##
##########

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
          lazy.screen.prev_group(skip_empty=True)),

    Click([SUPER], "Button5", 
          lazy.screen.next_group(skip_empty=True)),
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
        Match(wm_class="pavucontrol"),  # Wireless configuration
        Match(wm_class="copyq"),  # Wireless configuration
    ],
    **layout_theme
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not
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
