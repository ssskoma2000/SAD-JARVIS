#!/usr/bin/env python3
"""
🚀 JARVIS SETUP SCRIPT
Setup Jarvis with virtual environment and dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
NC = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✅ {msg}{NC}")

def print_info(msg):
    print(f"{YELLOW}ℹ️  {msg}{NC}")

def print_error(msg):
    print(f"{RED}❌ {msg}{NC}")

def run_cmd(cmd, description=""):
    """Run command and return success status."""
    if description:
        print_info(description)
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    print("\n" + "="*50)
    print("🤖 JARVIS AUTOMATIC SETUP")
    print("="*50 + "\n")
    
    # Get backend directory
    backend_dir = Path(__file__).parent / "jarvis_uzb" / "backend"
    os.chdir(backend_dir)
    print_info(f"Working directory: {backend_dir}")
    
    # Step 1: Check Python
    print_info("Checking Python version...")
    success, output = run_cmd("python3 --version")
    if success:
        print_success(f"Python {output.strip()}")
    else:
        print_error("Python 3 not found!")
        sys.exit(1)
    
    # Step 2: Create venv
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        success, _ = run_cmd("python3 -m venv venv")
        if success:
            print_success("Virtual environment created")
        else:
            print_error("Failed to create venv")
            sys.exit(1)
    else:
        print_success("Virtual environment already exists")
    
    # Step 3: Upgrade pip
    print_info("Upgrading pip...")
    if sys.platform == "win32":
        pip_activate = "venv\\Scripts\\pip"
    else:
        pip_activate = "venv/bin/pip"
    
    success, _ = run_cmd(f"{pip_activate} install --upgrade pip setuptools wheel -q")
    if success:
        print_success("pip upgraded")
    
    # Step 4: Install requirements
    print_info("Installing dependencies (this may take a few minutes)...")
    success, output = run_cmd(f"{pip_activate} install -r requirements.txt")
    if success:
        print_success("Dependencies installed")
    else:
        print_error(f"Failed to install dependencies:\n{output}")
        sys.exit(1)
    
    # Step 5: Verify key packages
    print_info("Verifying installations...")
    packages = ["openai", "sounddevice", "soundfile", "numpy", "pynput", "fsapi"]
    
    verify_cmd = f"{pip_activate} list | grep -E '(openai|sounddevice|numpy|pynput|fastapi)'"
    success, output = run_cmd(verify_cmd)
    if output:
        print(f"{GREEN}{output}{NC}")
        print_success("Key packages verified")
    
    # Step 6: Create .env if not exists
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print_info("Creating .env file...")
        env_file.write_text("""# 🤖 JARVIS CONFIGURATION
OPENAI_API_KEY=sk-proj-YOUR_API_KEY_HERE
OPENAI_MODEL=gpt-4o-mini
WHISPER_LANGUAGE=uz
TTS_VOICE=nova
LOG_LEVEL=INFO
DEBUG=false
""")
        print_success(".env file created")
    else:
        print_success(".env file already exists")
    
    # Final summary
    print("\n" + "="*50)
    print_success("SETUP COMPLETE! 🎉")
    print("="*50 + "\n")
    
    print(f"{YELLOW}NEXT STEPS:{NC}\n")
    print("1️⃣  ADD YOUR OPENAI API KEY:")
    print(f"   Edit: {env_file}")
    print(f"   Replace: OPENAI_API_KEY=sk-proj-YOUR_API_KEY_HERE")
    print(f"   Get key: https://platform.openai.com/api/keys\n")
    
    print("2️⃣  ACTIVATE VIRTUAL ENVIRONMENT:")
    if sys.platform == "win32":
        print(f"   {backend_dir}\\venv\\Scripts\\activate\n")
    else:
        print(f"   source {backend_dir}/venv/bin/activate\n")
    
    print("3️⃣  RUN JARVIS:")
    print(f"   cd {backend_dir.parent / 'desktop'}")
    print(f"   python jarvis_tray.py\n")
    
    print("4️⃣  TEST:")
    print(f"   Press Ctrl+Space → Speak → Jarvis responds!\n")
    
    print(f"{GREEN}Status: Ready to run!{NC}\n")

if __name__ == "__main__":
    main()
