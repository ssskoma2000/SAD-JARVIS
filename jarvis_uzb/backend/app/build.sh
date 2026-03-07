#!/bin/bash

echo "Jarvis qurilmoqda..."

# Kerakli papkalarni tekshirish
mkdir -p build

# Kompilyatsiya (libcurl kutubxonasi bilan)
g++ src/*.cpp -o build/jarvis -lcurl -O2

if [ $? -eq 0 ]; then
    echo "Muvaffaqiyatli! Ishga tushirish uchun: ./build/jarvis uz"
else
    echo "Xatolik yuz berdi."
fi