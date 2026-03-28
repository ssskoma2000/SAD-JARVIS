import os
import subprocess
import sys
import shutil

def build_jarvis_backend():
    print("🚀 Jarvis Backend EXE yaratish boshlandi...")
    
    # 1. Pathlarni sozlash
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "backend", "main.py")
    data_file = os.path.join("backend", "buyruqlar", "readme.txt")
    
    # Windows va Linux uchun separatorni aniqlash
    sep = ";" if sys.platform == "win32" else ":"
    
    # 2. PyInstaller buyrug'i
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "JarvisBackend",
        # readme.txt ni EXE ichiga qo'shish
        f"--add-data={data_file}{sep}backend/buyruqlar",
        # Yashirin importlarni majburiy qo'shish
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--hidden-import=command_handler",
        "--hidden-import=ai_services",
        "--hidden-import=platform_utils",
        main_script
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ EXE muvaffaqiyatli yaratildi! 'dist/JarvisBackend.exe' ni tekshiring.")
    except Exception as e:
        print(f"\n❌ Build jarayonida xatolik: {e}")

if __name__ == "__main__":
    build_jarvis_backend()