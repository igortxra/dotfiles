from __future__ import annotations
from typing import Dict


class Colors:
    def __init__(self, fg: str, bg: str) -> None:
        self.fg = fg
        self.bg = bg


class Theme():
    wifi: Colors
    audio: Colors
    battery: Colors
    calendar: Colors
    ram: Colors
    window_count: Colors
    current_layout: Colors


class Dracula(Theme):
    BASIC_BLACK       = "#000000"
    BASIC_WHITE       = "#FFFFFF"
    GREY              = "#44475A50"
    BLACK             = "#282A36"
    WHITE             = "#F8F8F2"
    RED               = "#FF5555"
    ORANGE            = "#FFB86C"
    YELLOW            = "#F1FA8C"
    GREEN             = "#50fa7b"
    PURPLE            = "#BD93F9"
    CYAN              = "#8BE9FD"
    PINK              = "#FF79C6"
    BRIGHT_RED        = "#FF6E6E"
    BRIGHT_GREEN      = "#69FF94"
    BRIGHT_YELLOW     = "#FFFFA5"
    BRIGHT_BLUE       = "#D6ACFF"
    BRIGHT_MAGENTA    = "#FF92DF"
    BRIGHT_CYAN       = "#A4FFFF"
    BRIGHT_WHITE      = "#FFFFFF"
    MENU              = "#21222C"
    VISUAL            = "#3E4452"
    GUTTER_FG         = "#4B5263"
    NONTEXT           = "#3B4048"

    # Foreground and Background
    audio                   = Colors(BASIC_WHITE, bg=GREY)
    battery                 = Colors(BASIC_WHITE, bg=GREY)
    battery_low             = Colors(BRIGHT_RED, bg=GREY)
    calendar                = Colors(BASIC_WHITE, bg=GREY)
    clipboard               = Colors(BLACK, bg=BRIGHT_CYAN)
    clock                   = Colors(BASIC_WHITE, bg=GREY)   
    current_layout          = Colors(BASIC_WHITE, bg=GREY)
    check_updates           = Colors(BRIGHT_YELLOW, bg=GREY)   
    chord                   = Colors(BLACK, bg=WHITE)
    ram                     = Colors(PINK, bg=GREY)
    spotify                 = Colors(BRIGHT_GREEN, bg=GREY)
    wifi                    = Colors(BRIGHT_GREEN, bg=GREY)
    window_count            = Colors(BASIC_WHITE, bg=GREY)
    bar                     = Colors(BRIGHT_BLUE, GREY)
    cpu_graph               = Colors(CYAN, GREY)

    # Simple Color
    groupbox_active         = WHITE
    groupbox_inactive       = WHITE
    groupbox_this_current   = PURPLE
    groupbox_this           = GREY
    groupbox_other_current  = PURPLE
    groupbox_other          = GREY

    window_focused_border   = BRIGHT_BLUE
    window_border           = BLACK

class Catppuccin(Theme):
    BASIC_BLACK       = "#000000"
    BASIC_WHITE       = "#FFFFFF"
    GREY              = "#5b607850"
    BLACK             = "#181926"
    WHITE             = "#cad3f5"
    RED               = "#ed8796"
    ORANGE            = "#f5a97f"
    YELLOW            = "#eed49f"
    GREEN             = "#a6da95"
    PURPLE            = "#c6a0f6"
    CYAN              = "#91d7e3"
    PINK              = "#f5bde6"
    BLUE              = "#8aadf4"
    MAROON            = "#ee99a0"

    audio                   = Colors(BASIC_WHITE, bg=GREY)
    battery                 = Colors(BASIC_WHITE, bg=GREY)
    battery_low             = Colors(RED, bg=GREY)
    calendar                = Colors(BASIC_WHITE, bg=GREY)
    clipboard               = Colors(BLACK, bg=CYAN)
    clock                   = Colors(BASIC_WHITE, bg=GREY)   
    current_layout          = Colors(BASIC_WHITE, bg=GREY)
    check_updates           = Colors(YELLOW, bg=GREY)   
    chord                   = Colors(BLACK, bg=WHITE)
    ram                     = Colors(PINK, bg=GREY)
    spotify                 = Colors(GREEN, bg=GREY)
    wifi                    = Colors(GREEN, bg=GREY)
    window_count            = Colors(BASIC_WHITE, bg=GREY)
    bar                     = Colors(BLUE, GREY)
    cpu_graph               = Colors(CYAN, GREY)

    # Simple Color
    groupbox_active         = BASIC_WHITE
    groupbox_inactive       = BASIC_WHITE
    groupbox_this_current   = PURPLE
    groupbox_this           = GREY
    groupbox_other_current  = PURPLE
    groupbox_other          = GREY

    window_focused_border   = PURPLE
    window_border   = BLACK

THEMES : Dict[str, Theme] = {
    "dracula": Dracula(),
    "catppuccin": Catppuccin()
}

def get_theme(theme_name: str) -> Theme:
    return THEMES.get(theme_name, Dracula()) 
