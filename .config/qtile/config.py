
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
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    KeyChord,
    Match,
    Screen,
    ScratchPad,
    DropDown,
)
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.hook import subscribe


# AUXILIARY FUNCTIONS
def go_to_group(group_name: str):
    def _inner(qtile: Qtile):
        qtile.groups_map[group_name].toscreen()

    return _inner


def get_number_of_screens():
    """Get number of connected monitors"""
    cmd_get_active_screens = 'xrandr --query | grep " connected"'
    xr = (
        subprocess.check_output(cmd_get_active_screens, shell=True).decode().split("\n")
    )
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


SCREEN_COUNT = get_number_of_screens()
# -----------------------------------------------------------------------------------------

# BASIC APPLICATIONS
TERMINAL = "kitty"
FILE_MANAGER = "thunar"
DEFAULT_FONT = "Iosevka Nerd Font"
# -----------------------------------------------------------------------------------------

# PATHS
PATH_HOME = path.expanduser("~")
PATH_SCRIPTS = f"{PATH_HOME}/.local/bin"
PATH_ICONS = f"{PATH_HOME}/.icons/qtile/"
PATH_ICON_BATTERY = f"{PATH_ICONS}/battery/"
PATH_ICON_AUDIO = f"{PATH_ICONS}/audio/"
# -----------------------------------------------------------------------------------------

# INIT SCRIPT
AUTOSTART = f"{PATH_SCRIPTS}/AUTOSTART"
# -----------------------------------------------------------------------------------------

# COLORS
colors = [
    "#0f1228",
    "#414d9c",
    "#423fa6",
    "#404fa7",
    "#8a55dd",
    "#5966be",
    "#5f69bf",
    "#c5c5c7",
    "#404c94",
    "#414d9c",
    "#423fa6",
    "#404fa7",
    "#8a55dd",
    "#5966be",
    "#5f69bf",
    "#c5c5c7",
]

cache = f"{PATH_HOME}/.cache/wal/colors"

def load_colors(cache):
    global colors
    try:
        with open(cache, "r") as file:
            colors = [file.readline().strip() for _ in range(16)]
    except FileNotFoundError:
        pass

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
MENU_APP = f"{PATH_SCRIPTS}/OPEN_APP_MENU &"
MENU_CLIPBOARD = f"{PATH_SCRIPTS}/OPEN_CLIPBOARD_MENU &"
MENU_POWER = f"{PATH_SCRIPTS}/OPEN_POWER_MENU &"
MENU_WALLPAPER = f"{PATH_SCRIPTS}/OPEN_WALLPAPER_MENU &"
MENU_THEME = f"{PATH_SCRIPTS}/OPEN_THEME_MENU &"
MENU_SCREENS = f"{PATH_SCRIPTS}/OPEN_SCREENS_MENU &"
MENU_AUTOMATIONS = f"{PATH_SCRIPTS}/OPEN_AUTOMATIONS_MENU &"
MENU_WINDOWS = f"{PATH_SCRIPTS}/OPEN_WINDOW_MENU &"
MENU_NETWORK = f"{PATH_SCRIPTS}/OPEN_NETWORK_MENU &"
# -----------------------------------------------------------------------------------------

# WIDGETS
WIDGET_DOTFILES = f"{PATH_SCRIPTS}/WIDGET_DOTFILES"
WIDGET_NETWORK = f"{PATH_SCRIPTS}/WIDGET_NETWORK"
# -----------------------------------------------------------------------------------------

# ACTIONS
CALENDAR_SHOW = f"{PATH_SCRIPTS}/CALENDAR_SHOW &"
SCREENSHOT = f"{PATH_SCRIPTS}/SCREENSHOT &"
SCREENSHOT_FULLSCREEN = f"{PATH_SCRIPTS}/SCREENSHOT_FULLSCREEN"
NOTIFICATION_OPEN = f"{PATH_SCRIPTS}/NOTIFICATION_OPEN"
NOTIFICATION_CLOSE = f"{PATH_SCRIPTS}/NOTIFICATION_CLOSE"
NOTIFICATION_POP = f"{PATH_SCRIPTS}/NOTIFICATION_HISTORY"
MEDIA_NEXT = f"{PATH_SCRIPTS}/MEDIA_NEXT"
MEDIA_PREVIOUS = f"{PATH_SCRIPTS}/MEDIA_PREVIOUS"
MEDIA_PLAY = f"{PATH_SCRIPTS}/MEDIA_PLAY"
MEDIA_VOL_UP = f"{PATH_SCRIPTS}/MEDIA_VOL_UP"
MEDIA_VOL_DOWN = f"{PATH_SCRIPTS}/MEDIA_VOL_DOWN"
MEDIA_VOL_SHOW = f"{PATH_SCRIPTS}/MEDIA_VOL_SHOW"
VOL_UP = f"{PATH_SCRIPTS}/VOLUME_UP"
VOL_DOWN = f"{PATH_SCRIPTS}/VOLUME_DOWN"
VOL_MUTE = f"{PATH_SCRIPTS}/VOLUME_MUTE"
VOL_SHOW = f"{PATH_SCRIPTS}/VOLUME_SHOW"
BRIGHTNESS_UP = f"{PATH_SCRIPTS}/BRIGHTNESS_UP"
BRIGHTNESS_DOWN = f"{PATH_SCRIPTS}/BRIGHTNESS_DOWN"
NOTES = "obsidian"

# -----------------------------------------------------------------------------------------

# Hooks and custom functions


@subscribe.startup_once
def setup():
    subprocess.Popen([AUTOSTART])


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
    #
    Key(
        [], "XF86MonBrightnessUp", lazy.spawn(BRIGHTNESS_UP), desc="Increase Brightness"
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn(BRIGHTNESS_DOWN),
        desc="Decrease Brightness",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn(VOL_UP),
        lazy.spawn(VOL_SHOW),
        desc="Raise Volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn(VOL_DOWN),
        lazy.spawn(VOL_SHOW),
        desc="Lower Volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn(VOL_MUTE),
        lazy.spawn(VOL_SHOW),
        desc="Toggle Audio Mute",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn(MEDIA_PLAY),
        lazy.spawn(VOL_SHOW),
        desc="Toggle Play/Pause music",
    ),
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Basic
    Key([SUPER], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([SUPER], "Backspace", lazy.window.kill(), desc="Kill focused window"),
    Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([SUPER], "o", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Controls
    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER, "control"], "t", lazy.hide_show_bar("top"), desc="Toggle bar"),
    Key([SUPER, "control"], "b", lazy.hide_show_bar("bottom"), desc="Toggle bar"),
    # Change Focus
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    Key([SUPER], "m", lazy.next_screen(), desc="Change focused screen"),

    # Column Layout
    Key([SUPER, "control"], "j", lazy.layout.grow_down()),
    Key([SUPER, "control"], "k", lazy.layout.grow_up()),
    Key([SUPER, "control"], "h", lazy.layout.grow_left()),
    Key([SUPER, "control"], "l", lazy.layout.grow_right()),
    Key([SUPER], "s", lazy.layout.toggle_split()),
    Key([SUPER, "shift", "control"], "h", lazy.layout.swap_column_left()),
    Key([SUPER, "shift", "control"], "l", lazy.layout.swap_column_right()),
    Key([SUPER], "n", lazy.layout.normalize()),

    # Move windows
    Key(
        [SUPER, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [SUPER, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Resize
    Key(
        [],
        "F10",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([SUPER], "i", lazy.layout.grow(), desc="Increase window size"),
    Key([SUPER], "d", lazy.layout.shrink(), desc="Decrease window size"),
    Key([SUPER], "g", lazy.layout.maximize(), desc="Maximize Window"),
    Key([SUPER], "r", lazy.layout.reset(), desc="Reset Windows Size"),
    # Spawners/Menus
    Key([SUPER], "e", lazy.spawn(FILE_MANAGER), desc="Spawn file manager"),
    Key([SUPER], "space", lazy.spawn(MENU_APP), desc="Spawn a app launcher"),
    Key([SUPER], "a", lazy.spawn(MENU_AUTOMATIONS), desc="Spawn automations menu"),
    Key([SUPER], "w", lazy.spawn(MENU_WINDOWS), desc="Spawn windows menu"),
    Key([SUPER, "control"], "s", lazy.spawn(MENU_SCREENS), desc="Spawn screens menu"),
    Key([SUPER], "v", lazy.spawn(MENU_CLIPBOARD), desc="Spawn clipboard menu"),
    Key([SUPER], "p", lazy.spawn(MENU_POWER), desc="Spawn power menu"),
    Key([SUPER], "equal", lazy.spawn(MENU_WALLPAPER), desc="Spawn wallpaper menu"),
    Key([SUPER], "t", lazy.spawn(MENU_THEME), desc="Spawn theme menu"),
    # Screenshots
    Key([], "Print", lazy.spawn(SCREENSHOT), desc="Launch screenshot menu"),
    Key(
        ["shift"],
        "Print",
        lazy.spawn(SCREENSHOT_FULLSCREEN),
        desc="Launch screenshot fullscreen",
    ),
    # Floating Windows
    Key(
        [SUPER, ALT],
        "f",
        lazy.window.toggle_floating(),
        lazy.window.center(),
        desc="Toggle window floating",
    ),
    Key([SUPER, ALT], "c", lazy.window.center(), desc="Center float window"),
    Key([SUPER, ALT], "tab", lazy.group.next_window(), desc="Focus next window"),
    Key(
        [SUPER, ALT, "shift"], "tab", lazy.group.prev_window(), desc="Focus prev window"
    ),
    Key(
        [SUPER, ALT],
        "h",
        lazy.window.resize_floating(dw=-20, dh=0),
        desc="decrease width by 20",
    ),
    Key(
        [SUPER, ALT],
        "j",
        lazy.window.resize_floating(dw=0, dh=20),
        desc="increase height by 20",
    ),
    Key(
        [SUPER, ALT],
        "k",
        lazy.window.resize_floating(dw=0, dh=-20),
        desc="decrease height by 20",
    ),
    Key(
        [SUPER, ALT],
        "l",
        lazy.window.resize_floating(dw=20, dh=0),
        desc="increase width by 20",
    ),
    Key(
        [SUPER, ALT, "shift"],
        "h",
        lazy.window.move_floating(dx=-20, dy=0),
        desc="move floating left",
    ),
    Key(
        [SUPER, ALT, "shift"],
        "j",
        lazy.window.move_floating(dx=0, dy=20),
        desc="move floating down",
    ),
    Key(
        [SUPER, ALT, "shift"],
        "k",
        lazy.window.move_floating(dx=0, dy=-20),
        desc="move flaoting up",
    ),
    Key(
        [SUPER, ALT, "shift"],
        "l",
        lazy.window.move_floating(dx=20, dy=0),
        desc="move floating right",
    ),
    # Music Control
    Key([SUPER], "period", lazy.spawn(MEDIA_NEXT), desc="Next music track"),
    Key([SUPER], "comma", lazy.spawn(MEDIA_PREVIOUS), desc="Previous music track"),
    Key(
        [SUPER],
        "semicolon",
        lazy.spawn(MEDIA_PLAY),
        desc="Toggle play/pause music track",
    ),
    # Music Volume Control
    Key(
        [SUPER, "shift"],
        "period",
        lazy.spawn(MEDIA_VOL_UP),
        desc="Music Volume Up",
    ),
    Key(
        [SUPER, "shift"],
        "comma",
        lazy.spawn(MEDIA_VOL_DOWN),
        desc="Music Volume Down",
    ),
    # Volume Control
    KeyChord(
        [SUPER, "control"],
        "v",
        [
            Key([], "k", lazy.spawn(VOL_UP)),
            Key([], "j", lazy.spawn(VOL_DOWN)),
            Key([], "m", lazy.spawn(VOL_MUTE)),
        ],
        name="Volume",
        mode=True,
    ),
    # Notifications Control
    KeyChord(
        [SUPER, "control"],
        "n",
        [
            Key(
                [],
                "Return",
                lazy.spawn(NOTIFICATION_OPEN),
                lazy.spawn(NOTIFICATION_CLOSE),
            ),
            Key([], "Backspace", lazy.spawn(NOTIFICATION_CLOSE)),
            Key([], "j", lazy.spawn(NOTIFICATION_POP)),
        ],
        name="Notifications",
        mode=False,
    ),
]
# -----------------------------------------------------------------------------------------

# GROUPS
groups = [
    Group(name="1", label="1", layout="monadtall"),
    Group(name="2", label="2", layout="monadtall"),
    Group(name="3", label="3", layout="monadtall"),
    Group(name="4", label="4", layout="monadtall"),
    Group(name="5", label="5", layout="monadtall"),
    Group(name="6", label="6", layout="monadtall"),
    Group(name="7", label="7", layout="monadtall"),
    Group(name="8", label="8", matches=[Match(wm_class="spotify")], layout="monadtall"),
    Group(name="9", label="9", matches=[Match(wm_class="discord")], layout="monadtall",
    ),
]

for group in groups:
    # Super + <group name> = switch to group
    keys.append(
        Key(
            [SUPER],
            group.name,
            lazy.function(go_to_group(group.name)),
            desc="Switch to group {}".format(group.name),
        )
    )

    # Super + shift + letter of group = move focused window to group
    keys.append(
        Key(
            [SUPER, "shift"],
            group.name,
            lazy.window.togroup(group.name, switch_group=False),
            desc=f"Move focused window to group {group.name}",
        ),
    )

groups.append(
    ScratchPad(
        name="notes",
        dropdowns=[
            DropDown(
                "notes",
                NOTES,
                x=0.10,
                y=0.10,
                width=0.8,
                height=0.8,
                opacity=1.0,
            )
        ],
    )
)

keys.append(Key([SUPER], "0", lazy.group["notes"].dropdown_toggle("notes")))

# -----------------------------------------------------------------------------------------


# LAYOUTS
layouts = [
    layout.Max(
        border_focus=COLOR_PRIMARY, margin=20, border_width=3, border_on_single=True
    ),
    layout.MonadTall(
        border_focus=COLOR_PRIMARY,
        margin=10,
        single_border_width=1,
        border_width=3,
        border_on_single=True,
),

    layout.Columns(
        border_focus=COLOR_PRIMARY,
        border_focus_stack=COLOR_4,
        border_normal=COLOR_BG_1,
        border_normal_stack=COLOR_BG_1,
        margin=[3,3,10,3],
        single_border_width=1,
        border_width=3,
        border_on_single=True,
    ),
    ## Not Used Layouts.
    # layout.MonadWide(
    #     border_focus=COLOR_PRIMARY,
    #     margin=10,
    #     single_border_width=1,
    #     border_width=3,
    #     ratio=0.70,
    #     border_on_single=True,
    # ),
    #
    # layout.Matrix(
    #     border_focus=COLOR_PRIMARY,
    #     margin=10,
    #     single_border_width=1,
    #     border_width=2,
    #     border_on_single=True,
    # ),
    # layout.Stack(margin=10, num_stacks=2),
    # layout.Bsp(margin=10),
    # layout.RatioTile(margin=10),
    # layout.Tile(margin=10),
    # layout.TreeTab(
    #     panel_width=300,
    #     font="Isoveka Nerd",
    #     vspace=4,
    #     active_bg=COLOR_PRIMARY,
    #     sections=[""],
    #     bg_color=COLOR_BG_1,
    #     inactive_bg=COLOR_BG_1,
    #     border_width=0,
    #     margin_left=40,
    #     place_right=True,
    # ),
    # layout.VerticalTile(margin=10),
    # layout.Zoomy(margin=10),
]
# -----------------------------------------------------------------------------------------

widget_defaults = dict(
    font=DEFAULT_FONT,
    fontsize=14,
)

# GROUPBOX WIDGETS
# Groupbox for the primary screen
widget_groupbox_main = widget.GroupBox(
    active="#FFF",
    background=COLOR_BAR,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_INACTIVE,
    highlight_color=[COLOR_BAR, COLOR_BAR],
    highlight_method="block",
    urgent_alert_method="border",
    urgent_border=COLOR_RED,
    urgent_text=COLOR_PRIMARY,
    this_screen_border="#333",  # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR,  # Border or line colour for group on other screen when unfocused.
    this_current_screen_border="#555",  # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR,  # Border or line colour for group on other screen when focused.
    block_highlight_text_color="#fff",
    padding_x=0,
    padding_y=0,
    margin_y=3,
    font=DEFAULT_FONT,
)

# Groupbox for the secondary screens
widget_groupbox_secondary = widget.GroupBox(
    active="#fff",
    background=COLOR_BAR,
    borderwidth=2,
    center_aligned=True,
    disable_drag=True,
    fmt=" {} ",
    hide_unused=True,
    inactive=COLOR_INACTIVE,
    highlight_color=[COLOR_BAR, COLOR_BAR],
    highlight_method="block",
    urgent_alert_method="border",
    urgent_border=COLOR_RED,
    urgent_text=COLOR_PRIMARY,
    this_screen_border="#333",  # Border or line colour for group on this screen when unfocused.
    other_screen_border=COLOR_BAR,  # Border or line colour for group on other screen when unfocused.
    this_current_screen_border="#555",  # Border or line colour for group on this screen when focused.
    other_current_screen_border=COLOR_BAR,  # Border or line colour for group on other screen when focused.
    block_highlight_text_color="#fff",
    padding_x=0,
    padding_y=0,
    margin_y=3,
    font=DEFAULT_FONT,
)

# -----------------------------------------------------------------------------------------

widgets = [
    widget.Spacer(10),
    widget.DF(
        partition="/home/igortxra",
        format="  {uf}{m}",
        visible_on_warn=False,
        background=None,
        foreground=COLOR_FG_2,
    ),
    widget.Spacer(10),
    widget.Memory(
        padding=5,
        fmt=" {}",
        format="{MemUsed: .2f}{mm}",
        measure_mem="G",
        background=None,
        foreground=COLOR_FG_2,
    ),
    widget.Spacer(10),
    widget.CPU(
        format="{load_percent}%", fmt=" {}", background=None, foreground=COLOR_FG_2
    ),
    widget.Spacer(10),
    widget.Sep(),
    widget.Spacer(10),
    widget.GenPollText(
        func=lambda: subprocess.check_output(WIDGET_DOTFILES, shell=True).decode(),
        update_interval=1,
        foreground=COLOR_FG_2,
        background=None,
        max_chars=20,
        padding=10,
    ),

    widget.Spacer(10),
    widget.GenPollText(
        func=lambda: subprocess.check_output(WIDGET_NETWORK).decode(),
        update_interval=1,
        foreground=COLOR_FG_2,
        background=None,
        max_chars=50,
        padding=10,
        mouse_callbacks={
            "Button1": lazy.spawn(MENU_NETWORK),
            "Button3": lazy.spawn(MENU_NETWORK),
        },
    ),

    widget.Spacer(10),
    widget.CheckUpdates(
        display_format="󰏔 {updates}",
        colour_have_updates=COLOR_YELLOW,
        colour_no_updates=COLOR_FG_2,
        no_update_string=" ",
        distro="Arch_yay",
        padding=10,
        update_interval=60
    ),

    widget.Spacer(10),
    widget.Sep(),
    widget.Systray(margin=10, padding=10, icon_size=14),

    # widget.Prompt(),

    widget.Spacer(10),
    widget.Spacer(),
    widget.CurrentLayout(mode="icon", scale=0.7),
    # widget.Spacer(14),
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

    widget.Mpris2(
        name="Media Icon",
        format="",
        objname="org.mpris.MediaPlayer2.spotify",
        background=COLOR_BG_1,
        foreground="#28b259",
        fmt=" ",
        paused_text="{}",
        padding=5,
        scroll=False
    ),
    widget.Mpris2(
        name="Media",
        width=200,
        format="{xesam:title} - {xesam:artist}",
        objname="org.mpris.MediaPlayer2.spotify",
        background="#28b259",
        foreground=COLOR_BG_1,
        fmt=" {}  ",
        paused_text=" {track}",
        padding=10,
    ),

    widget.Spacer(20),

    widget.Spacer(10),

    widget.Volume(
        fmt=" {}",
        theme_path=PATH_ICON_AUDIO,
        foreground=COLOR_FG_2,
        background=None,
        padding=10,

    ),
    widget.BatteryIcon(
    theme_path=PATH_ICON_BATTERY,
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
        format="",
        update_interval=2,
        padding=10,
        font="Liberation Mono",
    ),
    widget.Spacer(10),
    widget.Spacer(15),
    widget.Clock(
        format="%H:%M",
        background=None,
        foreground=COLOR_FG_1,
        mouse_callbacks={
            "Button1": lazy.spawn(CALENDAR_SHOW),
        },
        # font="Liberation Mono",
    ),
]


# BARS and WIDGETS
bar_primary = bar.Bar(
    widgets=widgets,
    size=20,
    margin=[0, 0, 0, 0],
    background=COLOR_BAR,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR,
)

bar_secondary = bar.Bar(
    widgets=[
        widget.Sep(foreground=COLOR_BAR),
        widget.Spacer(),
        widget.CurrentLayout(icon_first=True, scale=0.7),
        widget.Spacer(14),
        widget_groupbox_secondary,
        widget.Spacer(),
        widget.Sep(foreground=COLOR_BAR),
    ],
    size=25,
    margin=[-5, 0, 0, 0],
    background=COLOR_BAR,
    border_width=[4, 20, 4, 20],
    border_color=COLOR_BAR,
)

bars = [bar_primary, bar_secondary]
# -----------------------------------------------------------------------------------------

# SCREENS
screens = []
main_screen = Screen(bottom=bar_primary)
screens.append(main_screen)
for _ in range(SCREEN_COUNT):
    screens.append(Screen(bottom=bar_secondary))
# -----------------------------------------------------------------------------------------

# MOUSE
mouse = [
    Drag(
        [SUPER],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [SUPER],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
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
        Match(wm_class="thunar"),  # File explorer
        Match(wm_class="galculator"),  # Galculator
        Match(wm_class="nm-connection-editor"),  # Network Manager Connection Editor
        Match(wm_class="feh"),  # Image Viewer
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

# -------------------------------------
