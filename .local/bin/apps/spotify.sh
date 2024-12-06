#!/bin/bash

# Inicia o spotify-launcher
spotify-launcher &
SPOTIFY_PID=$!

# Inicia o script Python
python /home/igortxra/Desktop/Personal/ShutUpSpotify/main.py &
PYTHON_PID=$!

# Espera o Spotify ser fechado
wait $SPOTIFY_PID

# Quando o Spotify for fechado, mata o processo Python
echo "Spotify foi fechado. Terminando o script Python."
kill $PYTHON_PID

# Espera o processo Python ser encerrado
wait $PYTHON_PID

echo "Ambos os processos foram finalizados."
