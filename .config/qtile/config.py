# Copyright (c) 2010 Aldo Cortesi

# Copyright (c) 2010, 2014 dequis
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

import subprocess
from os import path

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.hook import subscribe

# AUXILIARY FUNCTIONS
def go_to_group(group_name: str):
    def _inner(qtile: Qtile):
        qtile.groups_map[group_name].toscreen()
    return _inner

def get_number_of_screens():
    """ Get number of connected monitors """
    cmd_get_active_screens = 'xrandr --query | grep " connected"'
    xr = subprocess .check_output(cmd_get_active_screens, shell=True) .decode() .split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors

SCREEN_COUNT = get_number_of_screens()
# -----------------------------------------------------------------------------------------

# BASIC APPLICATIONS
TERMINAL = "kitty"
# FILE_MANAGER = "thunar"
FILE_MANAGER = "ranger"
FONT = "Iosevka Nerd Font"
# -----------------------------------------------------------------------------------------

# PATHS
PATH_HOME = path.expanduser("~")
PATH_SCRIPTS = f"{PATH_HOME}/.local/bin"
PATH_SCREENSHOTS = f"{PATH_HOME}/Screenshots"
# -----------------------------------------------------------------------------------------

# INIT SCRIPT
AUTOSTART = f"{PATH_SCRIPTS}/autostart.sh"
# -----------------------------------------------------------------------------------------

# COLORS
colors = []
cache=f'{PATH_HOME}/.cache/wal/colors'
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(16):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()

load_colors(cache)

# FIXED COLORS
COLOR_BAR = "#11111199"
COLOR_RED = "#FF0000"
COLOR_YELLOW = "#FFFF00"

# MAIN COLORS
COLOR_PRIMARY = colors[2]
COLOR_SECONDARY = colors[1]
COLOR_4 = colors[4]

# FOREGROUNDS
COLOR_FG_1 = colors[-1]
COLOR_FG_2 = colors[-2]

# BACKGROUNDS
COLOR_BG_1 = colors[0]
COLOR_BG_2 = colors[1]
COLOR_BG_3 = colors[2]

# STATUS
COLOR_INACTIVE = colors[7]

# -----------------------------------------------------------------------------------------

# MENUS
MENU_APP = f"{PATH_SCRIPTS}/menus/apps.sh &"
MENU_CLIPBOARD = f"{PATH_SCRIPTS}/menus/clipboard.sh &"
MENU_POWER = f"{PATH_SCRIPTS}/menus/power.sh &"
MENU_UTILS=f"{PATH_SCRIPTS}/menus/utils.sh &"
MENU_SCREENSHOT=f"flameshot gui"
MENU_SCREENS=f"{PATH_SCRIPTS}/menus/screens.sh &"
MENU_AUDIO="pwvucontrol"
MENU_NETWORK="nm-connection-editor"
MENU_NETWORK_TERMINAL='kitty --hold tldr nmcli'
MENU_WINDOWS="rofi -show window"
MENU_AUTOMATIONS=f"{PATH_SCRIPTS}/menus/automations.sh &"
MENU_WALLPAPER=f"{PATH_SCRIPTS}/menus/wallpaper.sh &"
MENU_APP_IMAGES=f"{PATH_SCRIPTS}/menus/appimages.sh &"
# -----------------------------------------------------------------------------------------

# WIDGETS
WIDGET_DOTFILES=f"{PATH_SCRIPTS}/widgets/dotfiles-status.sh"
WIDGET_NETWORK=f"{PATH_SCRIPTS}/widgets/network.sh"
WIDGET_CALENDAR = f"{PATH_SCRIPTS}/widgets/calendar.sh" # -----------------------------------------------------------------------------------------

# DO ACTIONS
SHOW_UPGRADABLE_PACKAGES=f"{PATH_SCRIPTS}/utils/show-upgradable-packages.sh &"
TAKE_SCREENSHOT_FULLSCREEN=f"flameshot full --path {PATH_SCREENSHOTS}"
OPEN_NOTIFICATION="dunstctl context && dunstctl close"
CLOSE_NOTIFICATION="dunstctl close"
POP_NOTIFICATION="dunstctl history-pop"
MUSIC_NEXT="playerctl --player=spotify next"
MUSIC_PREVIOUS="playerctl --player=spotify previous"
MUSIC_PLAY_PAUSE="playerctl --player=spotify play-pause"
MUSIC_VOLUME_UP="playerctl -p spotify volume 0.1+"
MUSIC_VOLUME_DOWN="playerctl -p spotify volume 0.1-"
SHOW_MUSIC_VOLUME=f"{PATH_SCRIPTS}/utils/notify-music-volume.sh"
SHOW_VOLUME=f"{PATH_SCRIPTS}/utils/notify-volume.sh"
SYSTEM_METRICS="kitty --name btop --hold btop -p 1"
# -----------------------------------------------------------------------------------------

# HOOKS

@subscribe.startup_once
def setup():
    subprocess.Popen([AUTOSTART])

@subscribe.client_new 
def new_clinet(client):
    if "thunar" in client.get_wm_class():
        client.set_position_floating(500,500)
        client.set_size_floating(800,400)

@lazy.function
def resize_floating_window(qtile, width: int = 0, height: int = 0):
    w = qtile.current_window
    if w.floating:
        w.cmd_set_size_floating(w.width + width, w.height + height)


# -----------------------------------------------------------------------------------------

# KEYBINDINGS
SUPER = "mod4"
ALT = "mod1"

keys = [

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # BASIC
    Key([SUPER], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([SUPER], "Backspace", lazy.window.kill(), desc="Kill focused window"),
    Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts"),


    # CONTROLS
    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER, "control"], "t", lazy.hide_show_bar("top"), desc="Toggle bar"),
    Key([SUPER, "control"], "b", lazy.hide_show_bar("bottom"), desc="Toggle bar"),
    Key([SUPER, "control"], "c", lazy.spawn(SYSTEM_METRICS)),


    # Change Focus
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    Key([SUPER], 'm', lazy.next_screen(), desc='Change focused screen'), 
    
    # Move windows
    Key([SUPER, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([SUPER, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Resize
    Key([], "F10", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([SUPER], "i", lazy.layout.grow(), desc="Increase window size"),
    Key([SUPER], "d", lazy.layout.shrink(), desc="Decrease window size"),
    Key([SUPER], "g", lazy.layout.maximize(), desc="Maximize Window"),
    Key([SUPER], "r", lazy.layout.reset(), desc="Reset Windows Size"),

    # Spawners/Menus
    # Key([SUPER], "e", lazy.spawn(FILE_MANAGER), desc="Spawn file manager"),
    Key([SUPER], "space", lazy.spawn(MENU_APP), desc="Spawn a app launcher"),
    Key([SUPER], "o", lazy.spawn(MENU_APP_IMAGES), desc="Spawn a app image launcher"),
    Key([SUPER], "a", lazy.spawn(MENU_AUTOMATIONS), desc="Spawn automations menu"),
    Key([SUPER], "w", lazy.spawn(MENU_WINDOWS), desc="Spawn windows menu"),
    Key([SUPER], "s", lazy.spawn(MENU_SCREENS), desc="Spawn screens menu"),
    Key([SUPER], "v", lazy.spawn(MENU_CLIPBOARD), desc="Spawn clipboard menu"),
    Key([SUPER], "p", lazy.spawn(MENU_POWER), desc="Spawn power menu"),
    Key([SUPER], "equal", lazy.spawn(MENU_WALLPAPER), desc="Spawn wallpaper menu"),

    # Screenshots
    Key([], "Print", lazy.spawn(MENU_SCREENSHOT), desc='Launch screenshot menu'),
    Key(["shift"], "Print", lazy.spawn(TAKE_SCREENSHOT_FULLSCREEN), desc='Launch screenshot fullscreen'),

    # Floating Windows
    Key([SUPER, ALT], "f", lazy.window.toggle_floating(), lazy.window.center(), desc="Toggle window floating"),
    Key([SUPER, ALT], "c", lazy.window.center(), desc="Center float window"),
    Key([SUPER, ALT], "tab", lazy.group.next_window(), desc="Focus next window"),
    Key([SUPER, ALT, "shift"], "tab", lazy.group.prev_window(), desc="Focus prev window"),
    Key([SUPER, ALT], "h", lazy.window.resize_floating(dw=-20, dh=0), desc='decrease width by 20'),
    Key([SUPER, ALT], "j", lazy.window.resize_floating(dw=0, dh=20), desc='increase height by 20'),
    Key([SUPER, ALT], "k", lazy.window.resize_floating(dw=0, dh=-20), desc='decrease height by 20'),
    Key([SUPER, ALT], "l", lazy.window.resize_floating(dw=20, dh=0), desc='increase width by 20'),
    Key([SUPER, ALT, "shift"], "h", lazy.window.move_floating(dx=-20, dy=0), desc='move floating left'),
    Key([SUPER, ALT, "shift"], "j", lazy.window.move_floating(dx=0, dy=20), desc='move floating down'),
    Key([SUPER, ALT, "shift"], "k", lazy.window.move_floating(dx=0, dy=-20), desc='move flaoting up'),
    Key([SUPER, ALT, "shift"], "l", lazy.window.move_floating(dx=20, dy=0), desc='move floating right'),


    # Music Control 
    Key([SUPER], "period", lazy.spawn(MUSIC_NEXT), desc='Next music track'),
    Key([SUPER], "comma", lazy.spawn(MUSIC_PREVIOUS), desc='Previous music track'),
    Key([SUPER], "semicolon", lazy.spawn(MUSIC_PLAY_PAUSE), desc='Toggle play/pause music track'),

    # Music Volume Control
    Key([SUPER, "shift"], "period", lazy.spawn(MUSIC_VOLUME_UP), lazy.spawn(SHOW_MUSIC_VOLUME), desc='Music Volume Up'),
    Key([SUPER, "shift"], "comma", lazy.spawn(MUSIC_VOLUME_DOWN), lazy.spawn(SHOW_MUSIC_VOLUME), desc='Music Volume Down'),

    # Volume Control
    KeyChord(
        [SUPER, "control"], "v", 
        [
            Key([], "period", lazy.spawn("pamixer --increase 5"), lazy.spawn(SHOW_VOLUME)),
            Key([], "comma", lazy.spawn("pamixer --decrease 5"), lazy.spawn(SHOW_VOLUME)),
            Key([], "semicolon", lazy.spawn("pamixer -t"))
        ], name="Volume", mode=True),

    # Notifications Control
    KeyChord(
        [SUPER], "n", 
        [
            Key([], "Return", lazy.spawn(OPEN_NOTIFICATION), lazy.spawn(CLOSE_NOTIFICATION)),
            Key([], "Backspace", lazy.spawn(CLOSE_NOTIFICATION)),
            Key([], "j", lazy.spawn(POP_NOTIFICATION))
        ],
        name="Notifications",
        mode=False,
        
    )
]
# -----------------------------------------------------------------------------------------

# GROUPS
groups = [
    Group(name="1", label="1",  layout="monadtall"),
    Group(name="2", label="2",  layout="monadtall"),
    Group(name="3", label="3",  layout="monadtall"),
    Group(name="4", label="4",  layout="monadtall"),
    Group(name="5", label="5",  layout="monadtall"),
    Group(name="6", label="6",  layout="monadtall"),
    # Qgis Group
    Group(name="7", label="7", matches=[Match(wm_class="qgis")], layout="monadtall"),
    # Spotify Group
    Group(name="8", label="8", matches=[Match(wm_class="spotify")], layout="monadtall"),
    # Discord Group
    Group(name="9", label=" ", matches=[Match(wm_class="discord")], layout="monadtall", exclusive=True, spawn="discord"),
    Group(name="0", label=" ", matches=[Match(wm_class="obsidian")], layout="monadtall", exclusive=True, spawn="obsidian")
]

for group in groups:

    # Super + <group name> = switch to group
    keys.append(
        Key([SUPER], group.name,
        lazy.function(go_to_group(group.name)),
        desc="Switch to group {}".format(group.name),
        ))
    
    # Super + shift + letter of group = move focused window to group
    keys.append(
        Key(
            [SUPER, "shift"], group.name,
            lazy.window.togroup(group.name, switch_group=False),
            desc=f"Move focused window to group {group.name}"
        ),
    )
# -----------------------------------------------------------------------------------------

groups.append(
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("terminal", "kitty --override confirm_os_window_close=0" , x=0.25, y=0.2, width=0.5, height=0.6, opacity=0.9),
        DropDown("file_manager", "kitty --override confirm_os_window_close=0 --execute ranger" , x=0.25, y=0.2, width=0.5, height=0.6, opacity=0.9),
        DropDown("quick_edit", "kitty --name quick-edit -e nvim +':Telescope find_files hidden=True'" , x=0.1, y=0.1, width=0.8, height=0.8, opacity=0.9)

    ]),
)

keys.append(Key([], 'F1', lazy.group['scratchpad'].dropdown_toggle('terminal')))
keys.append(Key([], 'F2', lazy.group['scratchpad'].dropdown_toggle('file_manager')))
keys.append(Key([], 'F3', lazy.group['scratchpad'].dropdown_toggle('quick_edit')))

# LAYOUTS
layouts = [
    layout.Max(border_focus=COLOR_PRIMARY, margin=20, border_width=0, border_on_single=True),
    layout.Max(border_focus=COLOR_PRIMARY, margin=[100, 200, 100, 200], border_width=0, border_on_single=True),
    layout.MonadTall(border_focus=COLOR_PRIMARY, margin=20, single_border_width=1, border_width=2, border_on_single=True),
    layout.MonadWide(border_focus=COLOR_PRIMARY, margin=20, single_border_width=1, border_width=2, ratio=0.70, border_on_single=True),

    ## Not Used Layouts.
    # layout.Matrix(border_focus=COLOR_BASE, margin=10, single_border_width=1, border_width=2, border_on_single=True),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]
# -----------------------------------------------------------------------------------------

widget_defaults = dict(
    font=FONT,
    fontsize=16,
    padding=3,
)

# GROUPBOX WIDGETS
# Groupbox for the primary screen
widget_groupbox_main = widget.GroupBox(
    active="#999",
    background=COLOR_BAR,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_INACTIVE,
    highlight_color=[COLOR_BAR, COLOR_BAR],
    highlight_method='block',
    urgent_alert_method='border',
    urgent_border=COLOR_RED,
    urgent_text=COLOR_PRIMARY,
    this_screen_border="#333", # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR, # Border or line colour for group on other screen when unfocused.
    this_current_screen_border=COLOR_PRIMARY, # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR, # Border or line colour for group on other screen when focused.
    block_highlight_text_color=COLOR_FG_2,
    padding_x=0,
    padding_y=0,
    margin_y=3,
    fontsize=20,
    font="Liberation Mono"
)

# Groupbox for the secondary screens
widget_groupbox_secondary = widget.GroupBox(
    active="#999",
    background=COLOR_BAR,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_INACTIVE,
    highlight_color=[COLOR_BAR, COLOR_BAR],
    highlight_method='block',
    urgent_alert_method='border',
    urgent_border=COLOR_RED,
    urgent_text=COLOR_PRIMARY,
    this_screen_border="#333", # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR, # Border or line colour for group on other screen when unfocused.
    this_current_screen_border=COLOR_PRIMARY, # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR, # Border or line colour for group on other screen when focused.
    block_highlight_text_color=COLOR_FG_2,
    padding_x=0,
    padding_y=0,
    margin_y=3,
    fontsize=20,
    font="Liberation Mono"
)

# -----------------------------------------------------------------------------------------

clock_widget = widget.Clock(
    format="%a %d - %H:%M", 
    background=None, 
    foreground=COLOR_FG_1,
    mouse_callbacks={
        "Button1": lazy.spawn(WIDGET_CALENDAR + " curr"),
        "Button4": lazy.spawn(WIDGET_CALENDAR + " prev"),
        "Button5": lazy.spawn(WIDGET_CALENDAR + " next"),
    },
    fontsize=18,
    font="Liberation Mono")

widgets = [
        widget.Clock(
            format="%a %d - %H:%M", 
            background=None, 
            foreground=COLOR_FG_1,
            mouse_callbacks={
                "Button1": lazy.spawn(WIDGET_CALENDAR + " curr"),
                "Button4": lazy.spawn(WIDGET_CALENDAR + " prev"),
                "Button5": lazy.spawn(WIDGET_CALENDAR + " next"),
            },
            fontsize=18,
            font="Liberation Mono"
        ),

        widget.Spacer(),

        widget.CurrentLayoutIcon(scale=0.7),
        
        widget.Spacer(14),

        widget_groupbox_main,

        widget.Spacer(20),

        widget.Spacer(10),
        widget.Chord(
            fmt=" {} ",
            name_transform=lambda n: n.upper(),
            foreground=COLOR_FG_1,
            background=COLOR_PRIMARY,
        ),

        widget.Spacer(),

        widget.Clipboard(
            fmt=" 󰅎  Copied ",
            max_width=2,
            foreground=COLOR_FG_1,
            background=None,
            timeout=2,
        ),

        widget.Spacer(10),
        widget.Mpris2(
            name="spotify",
            display_metadata=['xesam:title', 'xesam:artist'],
            scroll_chars=None,
            objname="org.mpris.MediaPlayer2.spotify",
            scroll_interval=0,
            background=COLOR_PRIMARY,
            foreground=COLOR_FG_2,
            fmt='{}   ',
            paused_text='   {track}',
            padding=10,
        ),

        widget.Spacer(20),

        widget.Volume(
            fmt="󱄠",
            foreground=COLOR_FG_2,
            background=None,
            mouse_callbacks={
                "Button3": lazy.spawn(MENU_AUDIO)
            },
            padding=5,
            fontsize=18
        ),
        widget.Spacer(2),
        widget.Volume(
            fmt="{}",
            foreground=COLOR_FG_2,
            background=None,
            mouse_callbacks={
                "Button3": lazy.spawn(MENU_AUDIO)
            },
            padding=5,
            font="Liberation Mono"
        ),
        widget.Spacer(10),
        widget.BatteryIcon(
            theme_path="/usr/share/icons/Tela-circle-black/22/panel/",
            update_interval=2,
        ),
        widget.Battery(
            foreground=COLOR_FG_2,
            background=COLOR_BAR,
            low_background=COLOR_BAR,
            low_foreground=COLOR_RED,
            low_percentage=0.40,
            notify_below=30,
            charge_char="",
            full_char="",
            discharge_char="",
            unknown_char="",
            show_short_text=False,
            format='{percent:2.0%}',
            update_interval=2,
            padding=1,
            font="Liberation Mono"
        ),
    ]


# BARS and WIDGETS
bar_primary = bar.Bar(
    widgets=widgets,
    size=25,
    margin=[-5,0,0,0],
    background=COLOR_BAR,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR,
)

bar_secondary = bar.Bar(
    widgets=[
        widget.Sep(foreground=COLOR_BAR),
        widget.Spacer(),
        widget.CurrentLayoutIcon(scale=0.7),
        widget.Spacer(14),
        widget_groupbox_secondary,
        widget.Spacer(),
        widget.Sep(foreground=COLOR_BAR),
    ]
    ,
    size=25,
    margin=[-5,0,0,0],
    background=COLOR_BAR,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR,
)

bar_top = bar.Bar(
    widgets=[
        widget.Spacer(20),
        widget.GenPollText(
            func=lambda: subprocess.check_output(WIDGET_DOTFILES, shell=True).decode(),
            update_interval=1, 
            foreground=COLOR_FG_2,
            background=None,
            max_chars=20,
            padding=5,
        ),

        # widget.Spacer(20),
        # widget.Wallpaper(
        #     label="󰸉 ",
        #     directory=f"{PATH_HOME}/Wallpapers",
        #     foreground=COLOR_BASE,
        # ),

        widget.Spacer(20),
        widget.CheckUpdates(
            display_format="  {updates}",
            colour_have_updates=COLOR_YELLOW,
            colour_no_updates=COLOR_PRIMARY,
            no_update_string=" ",
            mouse_callbacks={
                "Button1": lazy.spawn(SHOW_UPGRADABLE_PACKAGES)
            }
        ),

        widget.Spacer(),

        widget.DF(
            partition="/home/igortxra", 
            format='  {uf}{m}',
            visible_on_warn=False,
            background=None,
            foreground=COLOR_FG_2
        ),

        widget.Spacer(20),
        widget.Memory(padding=5, fmt=" {}", format="{MemUsed: .2f}{mm}", measure_mem="G", background=None, foreground=COLOR_FG_2),
        
        widget.Spacer(20),
        widget.CPU(format='{load_percent}%', fmt=" {}", background=None, foreground=COLOR_FG_2),

        widget.Spacer(20),
        widget.GenPollText(
            func=lambda: subprocess.check_output(WIDGET_NETWORK).decode(),
            update_interval=1, 
            foreground=COLOR_FG_2,
            background=None,
            max_chars=50,
            padding=5,
            mouse_callbacks={
                "Button1": lazy.spawn(MENU_NETWORK_TERMINAL),
                "Button3": lazy.spawn(MENU_NETWORK)
            },
        ),

        widget.Spacer(),

        widget.Spacer(40),

        widget.Systray(padding=20, icon_size=18),
        widget.Spacer(20),

    ], 
    size=23,
    margin=[0,0,0,0],
    background=COLOR_BAR,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR,
)

bars = [bar_primary, bar_secondary]
# -----------------------------------------------------------------------------------------

# SCREENS
screens = []
main_screen = Screen(bottom=bar_primary, top=bar_top)
screens.append(main_screen)
for _ in range(SCREEN_COUNT):
    screens.append(Screen(bottom=bar_secondary))
# -----------------------------------------------------------------------------------------

# MOUSE
mouse = [
    Drag([SUPER], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([SUPER], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([SUPER], "Button1", lazy.window.bring_to_front()),
]
# -----------------------------------------------------------------------------------------

# MORE
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="thunar"),  # File explorer
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="galculator"),  # Galculator
        Match(wm_class="com.vixalien.sticky"),  # Sticky Notes
        Match(wm_class="nm-connection-editor"), # Network Manager Connection Editor
        Match(wm_class="pwvucontrol"), # Audio Settings
        Match(wm_class="VirtualBox"), # VirtualBox
        Match(wm_class="feh"), # Image Viewer
        Match(wm_class="Chromium-browser"), # For automations i created
        Match(wm_class="btop"), # For automations i created
    ],
    border_width=1,
    border_focus="#ffffff",

)
auto_fullscreen = True
focus_on_window_activation = "focus"
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

# -----------------------------------------------------------------------------------------
