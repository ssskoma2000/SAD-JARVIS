#!/bin/bash

PIPE_PATH="$HOME/.jarvis_pipe"

# Foydalanuvchiga eshitayotganini bildirish
notify-send "Jarvis" "Eshitmoqdaman..." -i microphone-sensitivity-high

# Python skriptini ishga tushirish va natijani pipe'ga yozish
# Diqqat: src/voice.py manzili to'g'ri ekanligiga ishonch hosil qiling
TEXT=$(python3 src/voice.py)

if [ ! -z "$TEXT" ]; then
    echo "$TEXT" > "$PIPE_PATH"
fi