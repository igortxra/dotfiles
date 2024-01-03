#!/bin/bash

# Verifica se o arquivo de capacidade da bateria existe
if [ -e "/sys/class/power_supply/BAT1/capacity" ]; then
    # Lê a capacidade da bateria do arquivo
    capacity=$(cat /sys/class/power_supply/BAT1/capacity)
else
    capacity=10000  # Define um valor padrão caso não seja possível ler a capacidade
fi

# Calcula o quarto da capacidade da bateria
quarter=$(echo "scale=0; $capacity / 25" | bc)

# Exibe o ícone com base no quarto da capacidade
case $quarter in
    0)
        icon=" "  # Ícone de bateria fraca
        ;;
    1)
        icon=" "  # Ícone de bateria média-baixa
        ;;
    2)
        icon=" "  # Ícone de bateria média-alta
        ;;
    3)
        icon=" "  # Ícone de bateria alta
        ;;
    4 | 5 | 6 | 7 | 8)
        icon=" "  # Ícone de bateria completa
        ;;
    *)
        icon="A"  # Ícone de bateria desconhecida
        ;;
esac

echo "$icon" | tr -d "\n"
