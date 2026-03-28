#!/bin/bash

# 🚀 JARVIS QUICK START SCRIPT
# ==============================
# This script activates everything and runs Jarvis

echo "🤖 JARVIS - VOICE ASSISTANT"
echo "============================"
echo ""
echo "🎤 Jarvis will start listening immediately!"
echo "Just speak your commands - no hotkeys needed!"
echo ""

# Go to backend directory
cd /home/koma/Desktop/a/SAD-JARVIS/jarvis_uzb/backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Run setup first: python3 setup.py"
    exit 1
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Check .env
echo "🔧 Checking configuration..."
if grep -q "sk-proj" .env; then
    echo "✅ OpenAI API key configured"
else
    echo "⚠️  WARNING: OpenAI API key not set!"
    echo "   Edit .env and add your API key to run Jarvis"
    echo "   Get it from: https://platform.openai.com/api/keys"
    echo ""
fi

# Go to desktop directory
cd ../desktop

# Run Jarvis
echo ""
echo "════════════════════════════════════════"
echo "🎯 STARTING JARVIS..."
echo "════════════════════════════════════════"
echo ""
echo "📌 USAGE:"
echo "   Jarvis starts listening automatically"
echo "   Speak your command in Uzbek/Russian/English"
echo "   Jarvis will respond with voice!"
echo ""
echo ""
echo "💡 TRY:"
echo "   'youtube och musiqa'"
echo "   'bugun sana?'"
echo "   'google qidir python'"
echo ""
echo "════════════════════════════════════════"
echo ""

python jarvis_tray.py
