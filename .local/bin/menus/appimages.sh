#!/bin/bash

mapfile -t files < <(find "$HOME" -path "$HOME/.cache" -prune -o -type f -iname "*.appimage" -print 2>/dev/null)

if [[ ${#files[@]} -eq 0 ]]; then
    notify-send "Nenhum AppImage encontrado"
    exit 1
fi

declare -A app_map
choices=()

for path in "${files[@]}"; do
    filename=$(basename "$path")
    dirname=$(dirname "$path")

    clean_name="${filename%%-*}"
    clean_name="${clean_name%.AppImage}"
    clean_name="${clean_name%.appimage}"

    display_name="$clean_name ($dirname)"
    choices+=("$display_name")
    app_map["$display_name"]="$path"
done

selection=$(printf '%s\n' "${choices[@]}" | rofi -dmenu -p "AppImage")

[[ -z "$selection" ]] && exit 0

exec "${app_map["$selection"]}"

