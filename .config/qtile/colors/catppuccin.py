
from __future__ import annotations
from typing import Dict
from .colorscheme import Colors, IColorscheme


class Catppuccin(IColorscheme):
    
    BLACK = "#000000"
    WHITE = "#FFFFFF"

    # Colors
    Rosewater = "#f5e0dc"
    Flamingo = "#f2cdcd"
    Pink = "#f5c2e7"
    Mauve = "#cba6f7"
    Red = "#f38ba8"
    Maroon = "#eba0ac"
    Peach = "#fab387"
    Yellow = "#f9e2af"
    Green = "#a6e3a1"
    Teal = "#94e2d5"
    Sky = "#89dceb"
    Sapphire = "#74c7ec"
    Blue = "#89b4fa"
    Lavender = "#b4befe"
    Text = "#cdd6f4"
    Subtext1 = "#bac2de"
    Subtext0 = "#a6adc8"
    Overlay2 = "#9399b2"
    Overlay1 = "#7f849c"
    Overlay0 = "#6c7086"
    Surface2 = "#585b70"
    Surface1 = "#45475a"
    Surface0 = "#313244"
    Base = "#1e1e2e"
    Mantle = "#181825"
    Crust = "#11111b"

    # Colors Applied
    audio                   = Colors(Text, bg=Surface0)
    battery                 = Colors(Text, bg=Surface0)
    battery_icon            = Colors(Text, bg=Surface0)
    battery_low             = Colors(Text, bg=Red)
    calendar                = Colors(WHITE, bg=Mantle)
    clipboard               = Colors(Crust, bg=Green)
    clock                   = Colors(Text, bg=Surface0)   
    current_layout          = Colors(Crust, bg=Base)
    check_updates           = Colors(Surface0, bg=Yellow)   
    chord                   = Colors(Surface0, bg=WHITE)
    ram                     = Colors(Surface0, bg=Pink)
    spotify                 = Colors(Surface0, bg=Green)
    wifi                    = Colors(Surface0, bg=Green)
    window_count            = Colors(Overlay0, bg=Base)
    bar                     = Colors(WHITE, bg=Crust+"00")
    cpu                     = Colors(Crust, bg=Green)
    groupbox_active         = Text
    groupbox_inactive       = Surface2
    groupbox_this_current   = WHITE
    groupbox_this           = Surface0
    groupbox_other_current  = Overlay1
    groupbox_other          = Mantle
    groupbox_background     = Base
    window_focused_border   = Overlay2
    window_border           = Base
    separator               = Overlay0 
    github_active           = Green
    github_inactive         = Text
    github_background       = Surface0
    github_error            = Red

THEMES : Dict[str, IColorscheme] = {
    "catppuccin": Catppuccin(),
}

def get_theme(theme_name: str) -> IColorscheme:
    return THEMES.get(theme_name, Catppuccin())

