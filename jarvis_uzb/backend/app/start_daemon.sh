#!/bin/bash

PIPE_PATH="$HOME/.jarvis_pipe"

# 1. Agar pipe mavjud bo'lmasa, yaratamiz
if [ ! -p "$PIPE_PATH" ]; then
    mkfifo "$PIPE_PATH"
    # Xavfsizlik: faqat egasi o'qiy/yoza oladi
    chmod 600 "$PIPE_PATH"
fi

echo "Jarvis orqa fonda ishga tushmoqda..."

# 2. Jarvisni ishga tushirish va pipe'dan o'qishga majburlash
# 'tail -f' pipe ochiq turishini ta'minlaydi
tail -f "$PIPE_PATH" | ./build/jarvis uz &

JARVIS_PID=$!
echo "Jarvis PID: $JARVIS_PID"
echo "To'xtatish uchun: kill $JARVIS_PID"

# 3. Dastlabki xabar
notify-send "Jarvis" "Tizim orqa fonda ishga tushdi" -i dialog-information