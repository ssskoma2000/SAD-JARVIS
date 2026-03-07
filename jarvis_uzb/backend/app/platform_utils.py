import subprocess
import sys
import os
import datetime
from PIL import ImageGrab

def open_chrome():
    """Google Chrome brauzerini ochadi."""
    try:
        if sys.platform == "win32":
            # Windows uchun
            subprocess.Popen(['start', 'chrome', 'https://google.com'], shell=True)
        elif sys.platform == "darwin":
            # macOS uchun
            subprocess.Popen(['open', '-a', 'Google Chrome'])
        else:
            # Linux uchun
            subprocess.Popen(['google-chrome'])
        return True
    except Exception as e:
        print(f"Chrome'ni ochishda xatolik: {e}")
        return False

def open_file_explorer():
    """Foydalanuvchining uy papkasini fayl boshqaruvchisida ochadi."""
    home_dir = os.path.expanduser("~")
    try:
        if sys.platform == "win32":
            subprocess.Popen(['explorer', home_dir])
        elif sys.platform == "darwin":
            subprocess.Popen(['open', home_dir])
        else:
            subprocess.Popen(['xdg-open', home_dir])
        return True
    except Exception as e:
        print(f"Fayl boshqaruvchini ochishda xatolik: {e}")
        return False

def open_telegram():
    """Telegram dasturini ochadi."""
    try:
        if sys.platform == "win32":
            # Windows uchun standart yo'l yoki 'start telegram'
            subprocess.Popen(['start', 'telegram'], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(['open', '-a', 'Telegram'])
        else:
            subprocess.Popen(['telegram-desktop'])
        return True
    except Exception as e:
        print(f"Telegramni ochishda xatolik: {e}")
        return False

def get_system_time():
    """Tizim vaqtini qaytaradi."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def shutdown_pc():
    """Kompyuterni o'chiradi."""
    try:
        if sys.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "1"])
        else:
            subprocess.run(["shutdown", "-h", "now"])
        return True
    except Exception as e:
        print(f"O'chirishda xatolik: {e}")
        return False

def play_music():
    """Musiqa qo'yish (misol uchun Spotify yoki media player)."""
    try:
        if sys.platform == "win32":
            subprocess.Popen(['start', 'spotify'], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(['open', '-a', 'Spotify'])
        else:
            subprocess.Popen(['rhythmbox']) # Linux misol
        return True
    except Exception as e:
        print(f"Musiqa qo'yishda xatolik: {e}")
        return False

def get_weather_info(city="Tashkent"):
    """Ob-havo ma'lumotini olish (Mock/Simulyatsiya)."""
    # Real API ulash uchun bu yerni o'zgartirish kerak (OpenWeatherMap)
    # Hozircha statik javob qaytaramiz xatolik bo'lmasligi uchun
    return f"{city}da havo ochiq, +25 gradus."

def take_screenshot():
    """Ekran tasvirini oladi va static papkaga saqlaydi."""
    try:
        # Static papka yo'lini aniqlash (backend/static)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        static_dir = os.path.join(base_dir, 'static')
        
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(static_dir, filename)
        
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        return filename
    except Exception as e:
        print(f"Screenshot olishda xatolik: {e}")
        return None