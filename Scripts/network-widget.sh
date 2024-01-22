#!/bin/sh
# Author: igortxta

connection_name=$(nmcli -t -f NAME connection show --active | grep -v lo | head --lines=1)
connection_type=$(nmcli -t -f TYPE connection show --active | grep -v lo | head --lines=1)

if [[ "$connection_type" == "802-3-ethernet" ]]; then
    connection_icon="󱎔 "
    connection_name="Wired"
elif [[ "$connection_type" == "802-11-wireless" ]]; then
    connection_icon=" "
else
    connection_icon="󰲛"
fi

echo "$connection_icon $connection_name" | tr -d '\n'
