import os
import subprocess
import sys
import shutil
import time

# Skript joylashgan papkani aniqlash (Project Root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def install_dependencies():
    print("📦 Python kutubxonalari o'rnatilmoqda...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "pillow", "requests", "psutil"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "pillow", "requests", "psutil", "openai"])
        print("✅ Kutubxonalar o'rnatildi.")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

def setup_folders():
    print("📂 Papkalar tuzilmasi tekshirilmoqda...")
    backend_dir = os.path.join(PROJECT_ROOT, "backend")
    templates_dir = os.path.join(backend_dir, "templates")
    static_dir = os.path.join(backend_dir, "static")
    
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        
    # index.html ni templates ga ko'chirish
    index_html = os.path.join(backend_dir, "index.html")
    if os.path.exists(index_html):
        shutil.move(index_html, os.path.join(templates_dir, "index.html"))
        print("✅ index.html templates papkasiga ko'chirildi.")

def build_csharp():
    print("🔨 C# Desktop ilovasi qurilmoqda...")
    project_path = os.path.join(PROJECT_ROOT, "desktop", "CSharpProject")
    try:
        subprocess.check_call(["dotnet", "build"], cwd=project_path)
        print("✅ C# Build muvaffaqiyatli yakunlandi.")
    except Exception as e:
        print(f"❌ C# Build xatosi: {e}")
        print("⚠️ Davom etilmoqda (faqat web versiya ishlashi mumkin)...")

def run_system():
    print("🚀 Tizim ishga tushirilmoqda...")
    
    # Serverni ishga tushirish
    server_script = os.path.join(PROJECT_ROOT, "backend", "server.py")
    print(f"🔹 Server: {server_script}")
    server_process = subprocess.Popen([sys.executable, server_script], cwd=PROJECT_ROOT)
    
    print("⏳ Server yuklanishi kutilmoqda (5 soniya)...")
    time.sleep(5)
    
    # Desktop ilovani ishga tushirish
    desktop_project = os.path.join(PROJECT_ROOT, "desktop", "CSharpProject")
    print("🔹 Desktop ilova ishga tushmoqda...")
    
    # Linux/Mac/Windows uchun universal run
    subprocess.Popen(["dotnet", "run"], cwd=desktop_project)
        
    print("✅ HAMMASI ISHGA TUSHDI! (To'xtatish uchun Ctrl+C bosing)")
    
    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\nTizim to'xtatildi.")

if __name__ == "__main__":
    install_dependencies()
    setup_folders()
    build_csharp()
    run_system()