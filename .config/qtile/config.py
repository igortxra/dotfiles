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
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.hook import subscribe


HOME = path.expanduser("~")
AUTOSTART = f"{HOME}/Scripts/autostart.sh"

# Apps and Scripts
APPS = f"{HOME}/Scripts/menus/apps.sh &"
CLIPBOARD = f"{HOME}/Scripts/menus/clipboard.sh &"
POWERMENU = f"{HOME}/Scripts/menus/power.sh &"
PROJECTS = f"{HOME}/Scripts/menus/projects.sh &"
UTILS=f"{HOME}/Scripts/menus/utils.sh &"
CONFIG=f"{HOME}/Scripts/menus/config.sh &"
WIDGET_NETWORK=f"{HOME}/Scripts/widgets/network.sh"
SHOW_UPGRADABLE_PACKAGES=f"{HOME}/Scripts/utils/show-upgradable-packages.sh &"
SCREENSHOT="flameshot gui"
SCREENSHOT_FULLSCREEN="flameshot full"

# Catppuccin Mocha Colors - https://github.com/catppuccin/catppuccin
COLOR_WHITE="#fff"
COLOR_CRUST="#11111b"
COLOR_OVERLAY1="#45475a"
COLOR_RED="#F38Ba8"
COLOR_MAUVE="#cba6f7"
COLOR_PEACH="#fab387"
COLOR_YELLOW="#f9e2af"
COLOR_SURFACE_0="#313244"
COLOR_GREEN="#a6e3a1"
COLOR_SAPPHIRE="#74c7ec"
COLOR_ROSEWATER="#f5e0dc"
COLOR_FLAMINGO="#f0c6c6"
COLOR_PINK="#f5bde6"
COLOR_BLUE="#8aadf4"

@subscribe.startup_once
def setup():
    subprocess.Popen([AUTOSTART])

SUPER = "mod4"
terminal = "kitty"

keys = [

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([SUPER], "space", lazy.spawn(APPS), desc="Spawn a app launcher"),
    Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([SUPER], "c", lazy.spawn(CONFIG), desc="Spawn config menu"),
    Key([SUPER], "o", lazy.spawn(PROJECTS), desc="Spawn power menu"),
    Key([SUPER], "p", lazy.spawn(POWERMENU), desc="Spawn power menu"),
    Key([SUPER], "v", lazy.spawn(CLIPBOARD), desc="Spawn clipboard manager"),
    Key([SUPER], "u", lazy.spawn(UTILS), desc="Spawn utils menu"),
    Key([SUPER], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([], "F10", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([], "Print", lazy.spawn(SCREENSHOT), desc='Launch screenshot'),
    Key(["shift"], "Print", lazy.spawn(SCREENSHOT_FULLSCREEN), desc='Launch screenshot fullscreen'),
    
    # Switch between windows
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    
    # Move windows between left/right columns or move up/down in current stack.
    Key([SUPER, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([SUPER, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([SUPER, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([SUPER, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Resize windows
    Key([SUPER, "control"], "k", lazy.layout.grow(), desc="Grow window"),
    Key([SUPER, "control"], "j", lazy.layout.shrink(), desc="Shrink window"),
    Key([SUPER], "r", lazy.layout.reset(), desc="Reset Windows Size"),
    Key([SUPER], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([SUPER], "g", lazy.layout.maximize(), desc="Maximize Window"),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # Super + letter of group = switch to group
            Key(
                [SUPER],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # Super + shift + letter of group = switch to & move focused window to group
            Key(
                [SUPER, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Max(margin=20, border_width=0),
    layout.MonadTall(border_focus=COLOR_ROSEWATER, margin=20, single_border_width=0, border_width=1),
    layout.MonadWide(border_focus=COLOR_ROSEWATER, margin=20, single_border_width=0, border_width=1),

    # Not Used Layouts.
    # layout.Columns(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Iosevka Nerd Font",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.7),
                widget.Spacer(14),
                widget.GroupBox(
                    this_current_screen_border=COLOR_PEACH,
                    highlight_method="text",
                    active=COLOR_OVERLAY1,
                    hide_unused=True
                ),

                
                widget.Spacer(10),
                
                widget.Sep(),
                
                widget.Spacer(10),
                
                widget.WidgetBox(
                    widgets=[
                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_FLAMINGO),
                        widget.DF(
                            partition="/", 
                            format='  Free: {uf}{m}',
                            visible_on_warn=False,
                            background=COLOR_FLAMINGO,
                            foreground=COLOR_CRUST,
                        ),

                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_FLAMINGO),

                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_MAUVE),
                        widget.Memory(padding=5, fmt=" {}", format="{MemUsed: .0f} /{MemTotal: .0f} ({mm})", measure_mem="G", background=COLOR_MAUVE, foreground=COLOR_CRUST),
                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_MAUVE),
                        
                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_PINK),
                        widget.CPU(fmt="󰍛 {}", background=COLOR_PINK, foreground=COLOR_CRUST),
                        widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_PINK),
                    ],

                    close_button_location="left",
                    text_open=" ",
                    text_closed=" ",
                ),

                widget.Spacer(10),

                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_PEACH),
                widget.Mpris2(
                    name="spotify",
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=None,
                    objname="org.mpris.MediaPlayer2.spotify",
                    scroll_interval=0,
                    background=COLOR_PEACH,
                    foreground=COLOR_CRUST,
                    fmt='{}   ',
                    paused_text='   {track}',
                    mouse_callbacks={
                        # "Button3": lazy.function(go_to_group("8"))
                    },
                ),
                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_PEACH),
                
                widget.Clipboard(
                   fmt=" 󰅎  Copied ",
                   max_width=2,
                   foreground=COLOR_GREEN,
                   background=COLOR_CRUST,
                   timeout=1,
                ),

                widget.Spacer(),

                widget.Systray(padding=10),
                
                widget.Spacer(30),

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

                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_GREEN),
                # Internet Widget
                widget.GenPollText(
                    func=lambda: subprocess.check_output(WIDGET_NETWORK).decode(),
                    update_interval=1, 
                    foreground=COLOR_CRUST,
                    background=COLOR_GREEN,
                    max_chars=20,
                    padding=5
                ),
                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_GREEN),


                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_FLAMINGO),
                widget.Clock(format="%d/%m/%Y - %a %I:%M:%S %p", background=COLOR_FLAMINGO, foreground=COLOR_CRUST),
                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_FLAMINGO),

                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_ROSEWATER),
                widget.Volume(
                    fmt="  {}",
                    foreground=COLOR_CRUST,
                    background=COLOR_ROSEWATER,
                    mouse_callbacks={
                        # "Button3": lazy.spawn(APP_AUDIO_SETTINGS)
                    },
                    padding=5
                ),
                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_ROSEWATER),

                widget.TextBox("", fontsize=20, padding=0, foreground=COLOR_MAUVE),
                widget.Battery(
                    foreground=COLOR_CRUST,
                    background=COLOR_MAUVE,
                    low_background=COLOR_MAUVE,
                    low_foreground=COLOR_CRUST,
                    low_percentage=0.40,
                    notify_below=25,
                    charge_char="  ",
                    full_char="  ",
                    discharge_char="",
                    unknown_char="? ",
                    show_short_text=False,
                    format='󰁹 {percent:2.0%} {char}',
                    update_interval=2,
                    padding=5
                ),
            ],
            23,
            margin=[-5,0,0,0],
            background=COLOR_CRUST,
            border_width=[4, 20, 4, 20],
            border_color=COLOR_CRUST,
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([SUPER], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([SUPER], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([SUPER], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
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
    ],
    border_width=0
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
wmname = "LG3D"
