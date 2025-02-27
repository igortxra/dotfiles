"""
This script can be runned every time you open spotify; 
You can kill it when quit spotify;
I did not figure out how to do it yet;
PS.: This was the best i could do unitl now, I believe that alredy exists
better ways, but i wanted to give me a try first.
"""
import time
import re
import subprocess
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# Please, let this here in the beggining
DBusGMainLoop(set_as_default=True)


def get_volume():
    output = subprocess.run(['playerctl', 'volume'],
                            capture_output=True, text=True)
    return float(output.stdout.strip())


def handler_function(*args):
    global volume
    global prev_volume
    global was_last_track_ads
    
    """ Mute spotify when the ads starts and unmute when stops."""
    try:
        # All ads has this metadata
        is_ads = bool(re.search("advertisement", args[1]["Metadata"]["xesam:title"].lower()))
        if is_ads and was_last_track_ads is False:
            # Get actual volume before mute it
            volume = get_volume()

            # Use Playerctl to mute spotify
            subprocess.run(["playerctl", "-p", "spotify", "volume", "0"])

            was_last_track_ads = True
            print(f"Ads detected - Muting. Previous volume was {volume}")
            subprocess.run([f"notify-send", "Ads Detected!", "Muting spotify...", "-a", "Ads Detector"])

        if not is_ads and was_last_track_ads:
            print(f"Ads gone - Unmuting. Volume set to {prev_volume}")
            subprocess.run(
                [f"notify-send", "Ads gone!", "Unmuting spotify...", "-a", "Ads Detector"])
            
            # Use Playerctl to unmute spotify
            subprocess.run(
                [f"playerctl", "-p", "spotify", "volume", f"{prev_volume}"])

            was_last_track_ads = False

        else:
            print(f"Keeping volume...")


    except Exception as e:
        # I just wanted to silence the ignorable errors with this try except
        # print(str(e))
        pass


# Wait the spotify delay to open
time.sleep(5)

# Stores current volume; Scale is >= 0 <= 1.0
prev_volume = get_volume()
volume = get_volume()
was_last_track_ads = False

# When spotify is communicating with dbus, it uses this bus_name and this object path
# I discovered them running dbus-monitor while used play/pause/next in spotfiy GUI
bus_name = "org.freedesktop.DBus"
object_path = "/org/mpris/MediaPlayer2"

# Connect to SessionBus (Which spotify uses to communicate changes in its player)
session_bus = dbus.SessionBus()
session_bus.add_signal_receiver(
    handler_function,
    path=object_path,
)

# This loop is necessary to keep capturing dbus signals form spotfiy
loop = GLib.MainLoop()
loop.run()
