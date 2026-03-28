#!/bin/bash

# 🚀 JARVIS AUTOMATIC SETUP SCRIPT
# ==================================

set -e  # Exit on error

echo "🤖 JARVIS SETUP SCRIPT"
echo "======================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo -e "${YELLOW}1️⃣  Checking Python...${NC}"
python3 --version
echo -e "${GREEN}✅ Python OK${NC}\n"

# Step 2: Go to backend directory
cd "$(dirname "$0")/jarvis_uzb/backend"
echo -e "${YELLOW}2️⃣  Working directory: $(pwd)${NC}\n"

# Step 3: Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}3️⃣  Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}\n"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}\n"
fi

# Step 4: Activate virtual environment
echo -e "${YELLOW}4️⃣  Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}\n"

# Step 5: Upgrade pip
echo -e "${YELLOW}5️⃣  Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel -q
echo -e "${GREEN}✅ pip upgraded${NC}\n"

# Step 6: Install requirements
echo -e "${YELLOW}6️⃣  Installing dependencies (this may take 2-3 minutes)...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}\n"

# Step 7: Check .env file
echo -e "${YELLOW}7️⃣  Checking .env configuration...${NC}"
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo -e "${GREEN}✅ .env file configured with API key${NC}\n"
    else
        echo -e "${RED}⚠️  .env file exists but OPENAI_API_KEY not set!${NC}"
        echo -e "${YELLOW}   Edit .env and add your API key:${NC}"
        echo -e "${YELLOW}   OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE${NC}\n"
    fi
else
    echo -e "${RED}❌ .env file not found!${NC}\n"
fi

# Step 8: Verify installations
echo -e "${YELLOW}8️⃣  Verifying installations...${NC}"
python -c "import openai; print(f'✅ OpenAI: {openai.__version__}')"
python -c "import sounddevice; print('✅ sounddevice installed')"
python -c "import speech_recognition; print('✅ speech_recognition installed')"
python -c "import fastapi; print('✅ FastAPI installed')"
echo ""

# Step 9: Summary
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}🎉 SETUP COMPLETE!${NC}"
echo -e "${GREEN}================================${NC}\n"

echo "📝 NEXT STEPS:"
echo ""
echo "1️⃣  EDIT YOUR API KEY:"
echo -e "   ${YELLOW}nano .env${NC}"
echo "   Replace: OPENAI_API_KEY=sk-proj-YOUR_API_KEY_HERE"
echo "   Get key from: https://platform.openai.com/api/keys"
echo ""
echo "2️⃣  RUN JARVIS:"
echo -e "   ${YELLOW}cd ../desktop${NC}"
echo -e "   ${YELLOW}python jarvis_tray.py${NC}"
echo ""
echo "3️⃣  TEST HOTKEY:"
echo "   Press Ctrl+Space → Speak → Jarvis responds"
echo ""
echo "4️⃣  BUILD EXE:"
echo -e "   ${YELLOW}python build_exe.py${NC}"
echo ""

echo -e "${GREEN}Status: Ready to run!${NC}\n"
