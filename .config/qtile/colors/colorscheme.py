class Colors:
    def __init__(self, fg: str, bg: str) -> None:
        self.fg = fg
        self.bg = bg

class IColorscheme():

    BLACK = "#000000"
    WHITE = "#FFFFFF"

    audio          : Colors
    battery        : Colors
    battery_icon   : Colors
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

    # Simple Color
    groupbox_active         : str
    groupbox_inactive       : str
    groupbox_this_current   : str
    groupbox_this           : str
    groupbox_other_current  : str
    groupbox_other          : str
    groupbox_background     : str
    window_focused_border   : str
    window_border           : str
    separator               : str
    github_active           : str
    github_inactive         : str
    github_error            : str

