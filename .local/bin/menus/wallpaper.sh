#!/bin/sh

WALLPAPER_DIR="$HOME/Wallpapers"

# Verifica se o diretório existe
if [ ! -d "$WALLPAPER_DIR" ]; then
  echo "Diretório $WALLPAPER_DIR não encontrado." >&2
fi

# Lista os nomes dos arquivos (sem path)
FILE_LIST=$(find "$WALLPAPER_DIR" -type f -exec basename {} \;)

# Usa o rofi para selecionar
SELECTED=$(printf "%s\n" "$FILE_LIST" | rofi -dmenu -p "Choose the Wallpaper")

# Verifica se algo foi selecionado
if [ -n "$SELECTED" ]; then
  
  # Reconstrói o caminho completo do arquivo selecionado
  FULL_PATH=$(find "$WALLPAPER_DIR" -type f -name "$SELECTED" | head -n 1)

  wal -i $FULL_PATH --cols16 -t --saturate 0.7 -o $HOME/.local/bin/utils/colors.sh
  qtile cmd-obj -o root -f reload_config
fi
