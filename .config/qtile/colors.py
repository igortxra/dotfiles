from __future__ import annotations
from typing import Dict


BLACK = "#000000"
WHITE = "#FFFFFF"


class Colors:
    def __init__(self, fg: str, bg: str) -> None:
        self.fg = fg
        self.bg = bg


class IColorscheme():
    audio          : Colors
    battery        : Colors
    battery_low    : Colors
    calendar       : Colors
    clipboard      : Colors
    clock          : Colors
    current_layout : Colors
    check_updates  : Colors
    chord          : Colors
    ram            : Colors
    spotify        : Colors
    wifi           : Colors
    window_count   : Colors
    bar            : Colors
    cpu_graph      : Colors

    # Simple Color
    groupbox_active         : str
    groupbox_inactive       : str
    groupbox_this_current   : str
    groupbox_this           : str
    groupbox_other_current  : str
    groupbox_other          : str
    window_focused_border   : str
    window_border           : str

class Catppuccin(IColorscheme):

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
    audio                   = Colors(WHITE, bg=Mantle)
    battery                 = Colors(WHITE, bg=Mantle)
    battery_low             = Colors(Red, bg=Mantle)
    calendar                = Colors(WHITE, bg=Mantle)
    clipboard               = Colors(BLACK, bg=Green)
    clock                   = Colors(WHITE, bg=Mantle)   
    current_layout          = Colors(WHITE, bg=Mantle)
    check_updates           = Colors(Yellow, bg=Mantle)   
    chord                   = Colors(BLACK, bg=WHITE)
    ram                     = Colors(Pink, bg=Mantle)
    spotify                 = Colors(Green, bg=Mantle)
    wifi                    = Colors(Green, bg=Mantle)
    window_count            = Colors(WHITE, bg=Mantle)
    bar                     = Colors(Blue, bg=Mantle)
    cpu_graph               = Colors(Green, bg=Mantle)
    groupbox_active         = WHITE
    groupbox_inactive       = Overlay2
    groupbox_this_current   = Overlay1
    groupbox_this           = Mantle
    groupbox_other_current  = Overlay1
    groupbox_other          = Mantle
    window_focused_border   = Overlay1
    window_border           = BLACK

THEMES : Dict[str, IColorscheme] = {
    "catppuccin": Catppuccin(),
}

def get_theme(theme_name: str) -> IColorscheme:
    return THEMES.get(theme_name, Catppuccin())
