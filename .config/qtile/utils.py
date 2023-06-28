import subprocess


def send_notification(title: str = "Message", msg: str = "", expire=2000):
    """ Return a notfication command """
    return f"notify-send '{title}' '{msg}' --expire-time={expire}"


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

