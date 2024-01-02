#!/bin/bash

capacity=$(cat /sys/class/power_supply/BAT1/capacity)

if [ -z "$capacity" ]
then
    capacity=10000
fi

quarter=$((capacity / 25))

case $quarter in
    [0-0.99])
        icon=" "  # Ícone de bateria fraca
        ;;
    [1-1.99])
        icon=" "  # Ícone de bateria média-baixa
        ;;
    [2-2.99])
        icon=" "  # Ícone de bateria média-alta
        ;;
    [3-3.99])
        icon=" "  # Ícone de bateria alta
        ;;
    4)
        icon=" "  # Ícone de bateria completa
        ;;
    *)
        icon=""  # Ícone de bateria desconhecida
        ;;
esac

echo "$icon" | tr -d "\n"
