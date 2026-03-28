#!/bin/bash

# 🚀 JARVIS DUMMY MODE TOGGLER
# =============================
# Enable/disable dummy mode for testing without API calls

ENV_FILE="/home/koma/Desktop/a/SAD-JARVIS/jarvis_uzb/backend/.env"

echo "🤖 JARVIS DUMMY MODE TOGGLER"
echo "============================"

# Check current dummy mode status
if grep -q "DUMMY_MODE=true" "$ENV_FILE"; then
    echo "📊 Current status: DUMMY MODE ENABLED (No API calls)"
    echo ""
    echo "🔄 Switching to REAL AI MODE..."
    sed -i 's/DUMMY_MODE=true/DUMMY_MODE=false/' "$ENV_FILE"
    echo "✅ REAL AI MODE activated!"
    echo ""
    echo "💡 Now Jarvis will use OpenAI API for responses"
else
    echo "📊 Current status: REAL AI MODE (Uses OpenAI API)"
    echo ""
    echo "🔄 Switching to DUMMY MODE..."
    sed -i 's/DUMMY_MODE=false/DUMMY_MODE=true/' "$ENV_FILE"
    echo "✅ DUMMY MODE activated!"
    echo ""
    echo "💡 Now Jarvis will use predefined responses (no API needed)"
fi

echo ""
echo "🎯 DUMMY MODE COMMANDS:"
echo "  • 'salom' → Greeting response"
echo "  • 'youtube' → Opens YouTube"
echo "  • 'google' → Opens Google"
echo "  • 'musiqa' → Opens YouTube music"
echo "  • Other → Default response"
echo ""
echo "🚀 Run Jarvis with: bash run_jarvis.sh"