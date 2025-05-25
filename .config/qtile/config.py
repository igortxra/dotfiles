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
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.hook import subscribe

# AUXILIARY FUNCTIONS
def go_to_group(group_name: str):
    def _inner(qtile: Qtile):
        if group_name == "0":
            qtile.groups_map[group_name].toscreen()
            if qtile.current_window is None:
                qtile.spawn("obsidian")

        if group_name == "9":
            qtile.groups_map[group_name].toscreen()
            if qtile.current_window is None:
                qtile.spawn("discord")
        else:
            qtile.groups_map[group_name].toscreen()
    return _inner

def get_number_of_screens():
    """ Get number of connected monitors """
    xr = subprocess.check_output(
        'xrandr --query | grep " connected"', shell=True).decode().split('\n')
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
# -----------------------------------------------------------------------------------------

# WIDGETS
WIDGET_DOTFILES=f"{PATH_SCRIPTS}/widgets/dotfiles-status.sh"
WIDGET_NETWORK=f"{PATH_SCRIPTS}/widgets/network.sh"
WIDGET_CALENDAR = f"{PATH_SCRIPTS}/widgets/calendar.sh"
# -----------------------------------------------------------------------------------------

# DO ACTIONS
SHOW_UPGRADABLE_PACKAGES=f"{PATH_SCRIPTS}/utils/show-upgradable-packages.sh &"
TAKE_SCREENSHOT_FULLSCREEN=f"flameshot full --path {PATH_SCREENSHOTS}"
OPEN_NOTIFICATION="dunstctl context && dunstctl close"
CLOSE_NOTIFICATION="dunstctl close"
MUSIC_NEXT="playerctl --player=spotify next"
MUSIC_PREVIOUS="playerctl --player=spotify previous"
MUSIC_PLAY_PAUSE="playerctl --player=spotify play-pause"
# -----------------------------------------------------------------------------------------

# COLORS
# Catppuccin Mocha Colors - https://github.com/catppuccin/catppuccin

COLOR_FG_1 = "#ffffff"
COLOR_FG_2 = "#f5e0dc"

COLOR_BG_1 = "#111113"
COLOR_BG_2 = "#45475a"

COLOR_RED = "#F38Ba8"
COLOR_PURPLE = "#cba6f7"
COLOR_ORANGE = "#fab387"
COLOR_YELLOW = "#f9e2af"
COLOR_GREEN = "#a6e3a1"
COLOR_FLAMINGO = "#f0c6c6"
COLOR_PINK = "#f5bde6"

COLOR_BAR_BG = COLOR_BG_1 + "77" # 77 for transparency

# COLOR_SURFACE_0="#313244"
# COLOR_SAPPHIRE="#74c7ec"
COLOR_BLUE="#8aadf4"

# -----------------------------------------------------------------------------------------

# AUTOSTART
@subscribe.startup_once
def setup():
    subprocess.Popen([AUTOSTART])
# -----------------------------------------------------------------------------------------

# KEYBINDINGS
SUPER = "mod4"
ALT = "mod1"

keys = [

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Basics
    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([SUPER], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([SUPER], "t", lazy.hide_show_bar("top"), desc="Toggle bar"),
    Key([SUPER], "b", lazy.hide_show_bar("bottom"), desc="Toggle bar"),
    Key([SUPER], 'm', lazy.next_screen(), desc='Change focused screen'), 
 
    # Spawners/Menus
    # Key([SUPER], "e", lazy.spawn(FILE_MANAGER), desc="Spawn file manager"),
    Key([SUPER], "space", lazy.spawn(MENU_APP), desc="Spawn a app launcher"),
    Key([SUPER], "p", lazy.spawn(MENU_POWER), desc="Spawn power menu"),
    Key([SUPER], "s", lazy.spawn(MENU_SCREENS), desc="Spawn screens menu"),
    Key([SUPER], "v", lazy.spawn(MENU_CLIPBOARD), desc="Spawn clipboard menu"),
    Key([SUPER], "equal", lazy.spawn(MENU_UTILS), desc="Spawn utils menu"),
    Key([SUPER], "w", lazy.spawn(MENU_WINDOWS), desc="Spawn windows menu"),
    Key([SUPER], "a", lazy.spawn(MENU_AUTOMATIONS), desc="Spawn automations menu"),

    # Screenshots
    Key([], "Print", lazy.spawn(MENU_SCREENSHOT), desc='Launch screenshot menu'),
    Key(["shift"], "Print", lazy.spawn(TAKE_SCREENSHOT_FULLSCREEN), desc='Launch screenshot fullscreen'),

    # Switch between windows
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),

    Key([SUPER, ALT], "k", lazy.group.prev_window(), desc="Focus next window"),
    Key([SUPER, ALT], "j", lazy.group.next_window(), desc="Focus next window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    Key([SUPER, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([SUPER, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Floating Windows
    Key([SUPER], "f", lazy.window.toggle_floating(), desc="Toggle window floating"),
    Key([SUPER], "c", lazy.window.center(), desc="Center float window"),
    Key([SUPER, ALT], "b", lazy.window.move_to_bottom(), desc="Move float window to bottom"),
    Key([SUPER, ALT], "f", lazy.window.bring_to_front(), desc="Move float window to front"),

    # Resize windows
    Key([], "F10", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([SUPER], "i", lazy.layout.grow(), desc="Increase window size"),
    Key([SUPER], "d", lazy.layout.shrink(), desc="Decrease window size"),
    Key([SUPER], "g", lazy.layout.maximize(), desc="Maximize Window"),
    Key([SUPER], "r", lazy.layout.reset(), desc="Reset Windows Size"),
    
    # Notifications
    Key([SUPER, "shift"], "n", lazy.spawn(OPEN_NOTIFICATION), desc="Open notification context"),
    Key([SUPER], "n", lazy.spawn(CLOSE_NOTIFICATION), desc="Close notification context"),

    # Music Control 
    Key([SUPER], "period", lazy.spawn(MUSIC_NEXT), desc='Next music track'),
    Key([SUPER], "comma", lazy.spawn(MUSIC_PREVIOUS), desc='Previous music track'),
    Key([SUPER], "semicolon", lazy.spawn(MUSIC_PLAY_PAUSE), desc='Toggle play/pause music track'),
]
# -----------------------------------------------------------------------------------------

# GROUPS
groups = [
    Group(name="1", label="1",  layout="monadtall"),
    Group(name="2", label="2",  layout="monadwide"),
    Group(name="3", label="3",  layout="monadwide"),
    Group(name="4", label="4",  layout="monadtall"),
    Group(name="5", label="5",  layout="monadtall"),
    Group(name="6", label="6",  layout="monadtall"),
    # Qgis Group
    Group(name="7", label="7", matches=[Match(wm_class="qgis")], layout="max"),
    # Spotify Group
    Group(name="8", label="8", matches=[Match(wm_class="spotify")], layout="max"),
    # Discord Group
    Group(name="9", label=" ", matches=[Match(wm_class="discord")], layout="max", exclusive=True, spawn="discord"),
    Group(name="0", label=" ", matches=[Match(wm_class="obsidian")], layout="max", exclusive=True, spawn="obsidian")
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
    layout.Max(border_focus=COLOR_PURPLE, margin=20, border_width=1, border_on_single=True),
    layout.MonadTall(border_focus=COLOR_PURPLE, margin=20, single_border_width=1, border_width=2, border_on_single=True),
    layout.MonadWide(border_focus=COLOR_PURPLE, margin=20, single_border_width=1, border_width=2, ratio=0.75, border_on_single=True),
    layout.Matrix(border_focus=COLOR_PURPLE, margin=10, single_border_width=1, border_width=2, border_on_single=True),

    ## Not Used Layouts.
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
    background=COLOR_BAR_BG,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_BG_2,
    highlight_color=[COLOR_BAR_BG, COLOR_BAR_BG],
    highlight_method='block',
    urgent_alert_method='border',
    urgent_border=COLOR_ORANGE,
    urgent_text=COLOR_BLUE,
    this_screen_border="#333", # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR_BG, # Border or line colour for group on other screen when unfocused.
    this_current_screen_border=COLOR_PURPLE, # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR_BG, # Border or line colour for group on other screen when focused.
    block_highlight_text_color=COLOR_FG_1,
    padding_x=0,
    padding_y=0,
    margin_y=3,
    fontsize=20,
    font="Liberation Mono"
)

# Groupbox for the secondary screens
widget_groupbox_secondary = widget.GroupBox(
    active="#999",
    background=COLOR_BAR_BG,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_BG_2,
    highlight_color=[COLOR_BAR_BG, COLOR_BAR_BG],
    highlight_method='block',
    urgent_alert_method='border',
    urgent_border=COLOR_ORANGE,
    urgent_text=COLOR_BLUE,
    this_screen_border="#333", # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR_BG, # Border or line colour for group on other screen when unfocused.
    this_current_screen_border=COLOR_PURPLE, # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR_BG, # Border or line colour for group on other screen when focused.
    block_highlight_text_color=COLOR_FG_1,
    padding_x=0,
    padding_y=0,
    margin_y=3,
    fontsize=20,
    font="Liberation Mono"
)
# -----------------------------------------------------------------------------------------

# BARS and WIDGETS
bar_primary = bar.Bar(
    widgets=[
        widget.CurrentLayoutIcon(scale=0.7),
        
        widget.Spacer(14),

        widget_groupbox_main,

        widget.Spacer(20),

        widget.Mpris2(
            name="spotify",
            display_metadata=['xesam:title', 'xesam:artist'],
            scroll_chars=None,
            objname="org.mpris.MediaPlayer2.spotify",
            scroll_interval=0,
            background=None,
            foreground=COLOR_ORANGE,
            fmt='{}   ',
            paused_text='   {track}',
            padding=10,
        ),

                
        widget.Spacer(10),
        widget.Clipboard(
            fmt=" 󰅎  Copied ",
            max_width=2,
            foreground=COLOR_GREEN,
            background=None,
            timeout=1,
        ),

        widget.Spacer(),
        widget.Clock(
            format="%Y-%m-%d 󰣇  %a %I:%M:%S %p", 
            background=None, 
            foreground=COLOR_PURPLE,
            mouse_callbacks={
                "Button1": lazy.spawn(WIDGET_CALENDAR + " curr"),
                "Button4": lazy.spawn(WIDGET_CALENDAR + " prev"),
                "Button5": lazy.spawn(WIDGET_CALENDAR + " next"),
            },
            fontsize=18,
            font="Liberation Mono"
        ),

        widget.Spacer(),

        widget.GenPollText(
            func=lambda: subprocess.check_output(WIDGET_DOTFILES, shell=True).decode(),
            update_interval=1, 
            foreground=COLOR_GREEN,
            background=None,
            max_chars=20,
            padding=5,
            # mouse_callbacks={
            #     "Button3": lazy.spawn(MENU_NETWORK)
            # },
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
            foreground=COLOR_FG_1,
            background=COLOR_BAR_BG,
            low_background=COLOR_BAR_BG,
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
    ],
    size=25,
    margin=[-5,0,0,0],
    background=COLOR_BAR_BG,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR_BG,
)

bar_secondary = bar.Bar(
    widgets=[
        widget.CurrentLayoutIcon(scale=0.7),
        widget.Spacer(14),
        widget_groupbox_secondary,
        widget.Spacer(),
    ], 
    size=25,
    margin=[-5,0,0,0],
    background=COLOR_BAR_BG,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR_BG,
)

bar_top = bar.Bar(
    widgets=[
                widget.TextBox(""),
                widget.Spacer(),
                
                widget.CheckUpdates(
                    display_format="  {updates}",
                    colour_have_updates=COLOR_YELLOW,
                    colour_no_updates=COLOR_GREEN,
                    no_update_string=" ",
                    mouse_callbacks={
                        "Button1": lazy.spawn(SHOW_UPGRADABLE_PACKAGES)
                    }
                ),

                
                widget.Spacer(20),
                widget.DF(
                    partition="/home/igortxra", 
                    format='  Free: {uf}{m}',
                    visible_on_warn=False,
                    background=None,
                    foreground=COLOR_FLAMINGO
                ),

                widget.Spacer(20),
                widget.Memory(padding=5, fmt=" {}", format="{MemUsed: .0f} /{MemTotal: .0f} ({mm})", measure_mem="G", background=None, foreground=COLOR_PURPLE),
                
                widget.Spacer(20),
                widget.CPU(fmt="󰍛 {}", background=None, foreground=COLOR_PINK),

                widget.Spacer(20),
                widget.GenPollText(
                    func=lambda: subprocess.check_output(WIDGET_NETWORK).decode(),
                    update_interval=1, 
                    foreground=COLOR_GREEN,
                    background=None,
                    max_chars=50,
                    padding=5,
                    mouse_callbacks={
                        "Button1": lazy.spawn(MENU_NETWORK_TERMINAL),
                        "Button3": lazy.spawn(MENU_NETWORK)
                    },
                ),


                widget.Spacer(20),
                widget.Wallpaper(
                    label="󰸉 ",
                    directory=f"{PATH_HOME}/Wallpapers"
                ),

                widget.Spacer(),

                widget.Systray(padding=20, icon_size=18),
                widget.Spacer(20),

    ], 
    size=23,
    margin=[0,0,0,0],
    background=COLOR_BAR_BG,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR_BG,
)

bars = [bar_primary, bar_secondary]
# -----------------------------------------------------------------------------------------

# SCREENS
screens = []
for i in range(SCREEN_COUNT):
    s = Screen(bottom=bars[i])
    if int(i) == 0:
        s.top=bar_top
    screens.append(s)
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
