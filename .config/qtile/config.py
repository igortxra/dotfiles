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
import subprocess
from typing import List

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.lazy import lazy

import utils, scripts, colors

###################################################################################################
# GLOBALS #########################################################################################

BACKLIGHT_NAME = 'intel_backlight'
WIDGET_FONT = "Font Awesome 6 Bold" # Unicodes - https://fontawesome.com/search
MONITORS = utils.get_monitors()
COLOR = colors.get_theme("catppuccin")
SUPER = "mod4"
ALT = "mod1"

###################################################################################################
# Lazy functions #################################################################################
@lazy.function
def move_window_to_next_screen(qtile):
    """ Moves a window to a screen and focuses it, allowing you to move it """
    window = qtile.current_window
    qtile.cmd_next_screen()
    window.togroup(qtile.current_screen.group.name)

###############################################################################
# Keys ########################################################################
# Obs: ALMOST all keys are specified in this section ##########################

keys = [

    # Qtile basics
    Key([SUPER], "Return", lazy.spawn(scripts.TERMINAL), desc="Launch terminal"),
    Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([SUPER, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    # Change Layouts
    Key([SUPER], "Tab", lazy.next_layout(), desc='Next layout'),
    Key([SUPER, "shift"], "Tab", lazy.prev_layout(), desc="Previous layout"),

    # Laptop keys
    Key([], "XF86MonBrightnessUp", lazy.spawn(scripts.BRIGHTNESS_UP), desc='Increase brightness'),
    Key([], "XF86MonBrightnessDown", lazy.spawn(scripts.BRIGHTNESS_DOWN), desc='Decrease brightness'),
    Key([], "XF86AudioMicMute", lazy.spawn(scripts.AUDIO_MIC_MUTE), desc='Mute microphone'),
    Key([], "XF86AudioMute", lazy.spawn(scripts.AUDIO_MUTE_UNMUTE), desc='Mute audio'),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(scripts.AUDIO_UP), desc='Increase audio volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn(scripts.AUDIO_DOWN), desc='Decrease audio volume'),

    # Move focus
    Key([SUPER], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([SUPER], "j", lazy.layout.down(), desc="Move focus down"),
    Key([SUPER], "k", lazy.layout.up(), desc="Move focus up"),
    Key([SUPER], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([SUPER], 'm', lazy.next_screen(), desc='Change focused screen'), 
    Key([SUPER], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([SUPER], "f", lazy.window.disable_floating(),desc="Disable floating behavior for focused window"),

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
    Key([SUPER], "r", lazy.layout.normalize()),
    Key([SUPER], "g", lazy.layout.maximize()),
    Key([SUPER], "i", lazy.layout.grow()),
    Key([SUPER, "shift"], "i", lazy.layout.shrink()),
 
    # Menus
    Key([SUPER], "s", lazy.spawn(scripts.MENU_POWER), desc="Search in browser"),
    Key([SUPER], "o", lazy.spawn(scripts.MENU_PROJECT), desc="Open projects menu"),
    Key([SUPER], "p", lazy.spawn(scripts.MENU_POWER), desc="Launch power menu"),
    Key([SUPER], "c", lazy.spawn(scripts.MENU_CALC), desc="Launch calculator"),
    Key([SUPER], "space", lazy.spawn(scripts.MENU_APP), desc="Launch app menu"),
    Key([SUPER, "shift"], "Equal", lazy.spawn(scripts.MENU_EMOJI), desc="Launch emoji list"),
    
    # Launch
    Key([], "Print", lazy.spawn(scripts.OPEN_SCREENSHOT), desc='Launch screenshot'),

    # Settings
    Key([SUPER, 'control'], 'p',lazy.spawn(scripts.RELOAD_PICOM), desc='Reload picom'),

    KeyChord([SUPER], "b", 
        [
            Key([], "k", lazy.hide_show_bar(position="top"), desc="Toggle top bar"),
            Key([], "j", lazy.hide_show_bar(position="bottom"), desc="Toggle bottom bar")
        ],
        name="Toggle Bar:    j -> Bottom Bar   k -> Top Bar"
    ),

    Key([SUPER, 'control'], 'w',
        lazy.spawn(scripts.RESTORE_WALLPAPER),
        lazy.spawn(utils.send_notification("Screens", "Wallpaper fixed", 4000)),
        desc='Update wallpaper (Used when screen layout change and the wallpaper brake)'),

    # Settings Menu
    KeyChord([SUPER], "Equal", [
        Key([], "k",  lazy.spawn(scripts.REMAP_CAPS), desc="Remap caps to act as super"),
        Key([], "w", lazy.spawn(scripts.OPEN_WIFI), desc="Open WIFI Menu"),

        # Audio submenu
        KeyChord([], "a", [
                Key([], "k", lazy.spawn(scripts.AUDIO_UP), desc="Increase audio volume"),
                Key([], "j", lazy.spawn(scripts.AUDIO_DOWN), desc="Decrease audio volume"),
                Key([], "m", lazy.spawn(scripts.AUDIO_MUTE_UNMUTE), desc="Toggle mute")
            ], 
            name='Audio Volume:    j -> Decrease   k -> Increase   m -> Mute',
            mode=True),

        # Brightness submenu
        KeyChord([], "b", [
                Key([], "k", lazy.spawn(scripts.BRIGHTNESS_UP), desc="Increase brightness"),
                Key([], "j", lazy.spawn(scripts.BRIGHTNESS_DOWN), desc="Descrease brightness")
            ], 
            name='Brightness:   j -> Decrease   k -> Increase',
            mode=True),

        # Settings / Screen layout
        KeyChord([], "s", [
            Key([], '0',
                lazy.spawn(scripts.MONITOR_ONLYNOTEBOOK),
                lazy.spawn(
                    utils.send_notification("Screens", "Using only notebook screen", 4000)),
                desc='Use only notebook screen'),

            Key([], '1',
                lazy.spawn(scripts.MONITOR_ONLYEXTERNAL),
                lazy.spawn(
                    utils.send_notification("Screens", "Using only external screen", 4000)),
                desc='Use only external screen'),

            Key([], '2',
                lazy.spawn(scripts.MONITOR_DUAL),
                lazy.spawn(utils.send_notification("Screens", "Using both screens", 4000)),
                desc='Use both screens, notebook and external'),
            ],
            name="Screens:   0 -> Only Notebook   1 -> Only External   2 -> Both",
            mode=False)
        ],
        name="Configuration:    a -> Audio   b -> Brightness   s -> Screens   w -> Wifi   k -> Remap Caps",
        mode=True
    ),

]

###############################################################################
# Groups - Workspaces
# Obs.: Group Keys MUST be in the same lenght as groups

groups: List[Group] = [
        Group("1", label="1", layout="max", matches=[]),
        Group("2", label="2", layout="monadtall", matches=[]),
        Group("3", label="3", layout="max", matches=[]), 
        Group("4", label="4", layout="max", matches=[]), 
        Group("7", label="7", layout="max", matches=[]), 
        Group("8", label="8", layout="max", matches=[]), 
        Group("9", label="9", layout="max", matches=[]), 
        Group("0", label="0", layout="max", matches=[Match(wm_class="Discord")]), 
]

for group in groups:
    keys.append(
        Key([SUPER], group.name,
            lazy.function(utils.go_to_group(group.name)),
            desc="Go to specified group"))
    keys.append(
        Key([SUPER, "shift"], group.name,
            lazy.window.togroup(group.name),
            lazy.function(utils.go_to_group(group.name)),
            desc="Move window to specified group"))

###############################################################################
# ScratchPads

groups.append(
    ScratchPad('scratchpad', [
        DropDown('notes', scripts.OPEN_NOTES, width=0.8, height=0.9, x=0.08, y=0.05, on_focus_lost_hide=False),
        DropDown('file_manager', scripts.OPEN_FILE_MANAGER, width=0.8, height=0.9, x=0.08, y=0.05, on_focus_lost_hide=False),
    ]))

keys.extend([
    Key([SUPER], "n", lazy.group["scratchpad"].dropdown_toggle('notes')),
    Key([SUPER], "e", lazy.group["scratchpad"].dropdown_toggle('file_manager'))
])


###############################################################################
# Layouts

# Default params for layouts
layout_theme = dict(
    border_width=2,
    border_focus=COLOR.window_focused_border,
    border_normal=COLOR.window_border,
    margin=10,
    padding=2)

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Zoomy(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Stack(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Floating(**layout_style),
]

###############################################################################
# Widgets

widget_defaults = dict(
    font=WIDGET_FONT,
    fontsize=11,
    padding=10)


icons_defaults = dict(
    font=WIDGET_FONT,
    fontsize=12,
    padding=0)
 

main_groupbox = widget.GroupBox(
    active=COLOR.groupbox_active,
    inactive=COLOR.groupbox_inactive,
    this_screen_border=COLOR.groupbox_this,
    other_screen_border=COLOR.groupbox_other,
    this_current_screen_border=COLOR.groupbox_this_current,
    other_current_screen_border=COLOR.groupbox_other_current,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=0,
    **widget_defaults)


secondary_groupbox = widget.GroupBox(
    active=COLOR.groupbox_active,
    inactive=COLOR.groupbox_inactive,
    this_screen_border=COLOR.groupbox_this,
    other_screen_border=COLOR.groupbox_other,
    this_current_screen_border=COLOR.groupbox_this_current,
    other_current_screen_border=COLOR.groupbox_other_current,
    highlight_method='block',
    disable_drag=True,
    hide_unused=True,
    borderwidth=3,
    visible_groups=[
        groups[4].name,
        groups[5].name,
        groups[6].name,
        groups[7].name,
    ],
    **widget_defaults)


main_top_widgets = [
    
    widget.Spacer(10),

    widget.WindowCount(
         background=COLOR.window_count.bg, 
         foreground=COLOR.window_count.fg, 
         show_zero=True),

    widget.CurrentLayoutIcon(
        background=COLOR.current_layout.bg,
        foreground=COLOR.current_layout.fg,
        scale=0.8,
        **widget_defaults),

    widget.Spacer(5),

    main_groupbox,

    widget.Spacer(20),
    
    widget.Mpris2(
        name="spotify",
        display_metadata=['xesam:title', 'xesam:artist'],
        scroll_chars=None,
        objname="org.mpris.MediaPlayer2.spotify",
        scroll_interval=0,
        background=COLOR.spotify.bg,
        foreground=COLOR.spotify.fg,
        fmt='{}   ',
        paused_text='  {track}',
        mouse_callbacks={
            "Button3": lazy.function(utils.go_to_group("8"))
        },
    ),

    widget.Spacer(5),

    widget.Clipboard(
        fmt="   Copied",
        max_width=2,
        background=COLOR.clipboard.bg,
        foreground=COLOR.clipboard.fg,
        **widget_defaults),

    widget.Spacer(),
 
    widget.Clock(
        format=f"  %H:%M:%S (%d/%m/%y)",
        background=COLOR.clock.bg,
        foreground=COLOR.clock.fg,
        mouse_callbacks={
            "Button1": lazy.spawn(scripts.OPEN_CALENDAR)
        }),

    widget.Chord(
        font="Iosevka NF ", 
        background=COLOR.chord.bg, 
        foreground=COLOR.chord.fg, 
        fmt=(" ") + "{}" + "   Esc -> Cancel"
    ),
   
    widget.Spacer(),

    widget.Wlan(
        format='   {percent:2.0%}',
        background=COLOR.wifi.bg,
        foreground=COLOR.wifi.fg,
        mouse_callbacks={
            "Button1": lazy.spawn(scripts.OPEN_WIFI)
        },
        **widget_defaults),

    widget.Spacer(5),

    widget.Volume(
        fmt="    {}",
        background=COLOR.audio.bg,
        foreground=COLOR.audio.fg, 
        mouse_callbacks={
            "Button3": lazy.spawn(scripts.OPEN_AUDIO_SETTINGS)
        },
        **widget_defaults),

    widget.Spacer(5),

    widget.Battery(
        background=COLOR.battery.bg,
        foreground=COLOR.battery.fg,
        low_background=COLOR.battery_low.bg,
        low_foreground=COLOR.battery_low.fg,
        low_percentage=0.40,
        notify_below=40,
        charge_char="  ",
        discharge_char='',
        show_short_text=True,
        format='    {percent:2.0%} {char}'),

    widget.Spacer(5),

    widget.Spacer(10),

]


secondary_top_widgets = [
    widget.Spacer(10),
    widget.CurrentLayoutIcon(
        background=COLOR.current_layout.bg,
        foreground=COLOR.current_layout.fg,
        scale=0.8,
        **widget_defaults),
    secondary_groupbox,
    widget.Spacer(),
]


bottom_widgets = [
    widget.Spacer(10),

    widget.WindowName(),

    widget.Spacer(),

    widget.CPU(
        background=COLOR.cpu_graph.bg,
        foreground=COLOR.cpu_graph.fg,
    ),
    widget.CPUGraph(
        type='line',
        background=COLOR.cpu_graph.bg,
        border_color=COLOR.cpu_graph.fg,
        border_width=0,
        line_width=2,
        margin_y=3,
        fill_color=COLOR.cpu_graph.fg,
        graph_color=COLOR.cpu_graph.fg
    ),

    widget.Spacer(10),
 
    widget.Memory(
        format='RAM {MemUsed: .3f}{mm} / {MemTotal: .3f}{mm}',
        measure_mem='G',
        background=COLOR.ram.bg,
        foreground=COLOR.ram.fg,
        **widget_defaults),
    widget.MemoryGraph(
        type='line',
        background=COLOR.ram.bg,
        border_color=COLOR.ram.fg,
        border_width=0,
        margin_y=3,
        line_width=1,
        fill_color=COLOR.ram.fg,
        graph_color=COLOR.ram.fg),

    widget.Spacer(),

    widget.Systray(),

    widget.Spacer(10),

    widget.CheckUpdates(
        display_format="  {updates} updates",
        colour_have_updates=COLOR.check_updates.fg,
        background=COLOR.check_updates.bg,
        no_update_string=""),

    widget.Spacer(10),
]


###############################################################################
# Screen and monitors

bar_style = dict(
    background=COLOR.bar.bg,
    border_color=COLOR.bar.bg,
    margin=[5, 10, 0, 10],
    border_width=0)

main_bar = bar.Bar(widgets=main_top_widgets, size=23, **bar_style)
secondary_bar = bar.Bar(widgets=secondary_top_widgets, size=23, **bar_style)
bottom_bar = bar.Bar(widgets=bottom_widgets, size=23, background=COLOR.bar.bg, border_width=0, margin=[0,10,5,10])

screens = []
for monitor in range(MONITORS):

    if monitor == 0:
        # Primary monitor
        screens.append(Screen(top=main_bar, bottom=bottom_bar))

    else:
        # Secondary monitors
        screens.append(Screen(top=secondary_bar))


###################################################################################################
# Hooks ###########################################################################################

@hook.subscribe.startup
def startup():
    """ Execute some steps in qtile refresh """
    main_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    secondary_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    bottom_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    reconfigure_groupbox()


@hook.subscribe.screens_reconfigured
def reconfigure_groupbox():
    """ Adapt visible groups depending on number of screens """
    groups_names = [g.name for g in qtile.groups]
    if len(qtile.screens) > 1:
        main_groupbox.visible_groups = groups_names[:4]
    else:
        main_groupbox.visible_groups = groups_names


@hook.subscribe.startup_once
def autostart():
    """ Executes a script on qtile startup """
    subprocess.Popen([scripts.AUTOSTART])


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
            # A way to call utils.go_to_group() because its impossible call directly
            client.qtile.cmd_simulate_keypress([SUPER], group.name)


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
        Match(wm_class="pavucontrol"),  # Wireless configuration
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
