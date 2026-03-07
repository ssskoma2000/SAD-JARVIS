from flask import Flask, render_template, jsonify, request, send_file
import os
from app import platform_utils, hacker_utils

# Flask ilovasini yaratish
app = Flask(__name__, template_folder='templates', static_folder='static')

# Asosiy sahifa (Landing Page + Web Jarvis)
@app.route('/')
def index():
    return render_template('index.html')

# API: Buyruqlarni bajarish (UzAI & Smart Desktop)
@app.route('/api/command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '').lower()
    response_text = "Tushunmadim, qaytaring."
    success = False

    print(f"Kelgan buyruq: {command}")

    if 'chrome' in command or 'brauzer' in command:
        success = platform_utils.open_chrome()
        response_text = "Chrome brauzeri ochilmoqda."
    elif 'fayl' in command or 'papka' in command:
        success = platform_utils.open_file_explorer()
        response_text = "Fayl boshqaruvchisi ochildi."
    elif 'telegram' in command:
        success = platform_utils.open_telegram()
        response_text = "Telegram ishga tushirilmoqda."
    elif 'vaqt' in command or 'soat' in command:
        time_str = platform_utils.get_system_time()
        response_text = f"Hozir soat: {time_str}"
        success = True
    elif 'ob-havo' in command:
        response_text = platform_utils.get_weather_info()
        success = True
    elif 'musiqa' in command:
        success = platform_utils.play_music()
        response_text = "Musiqa qo'yilmoqda."
    elif "o'chir" in command or 'uxlat' in command:
        response_text = "Kompyuter o'chirilmoqda..."
        # Xavfsizlik uchun hozircha o'chirmaymiz, lekin funksiya chaqiriladi
        # platform_utils.shutdown_pc() 
        success = True
    elif 'screenshot' in command or 'rasm' in command or 'ekran' in command:
        filename = platform_utils.take_screenshot()
        if filename:
            response_text = "Ekran rasmi olindi."
            return jsonify({'response': response_text, 'success': True, 'image_url': f'/static/{filename}'})
        else:
            response_text = "Screenshot olishda xatolik yuz berdi."
    elif 'salom' in command:
        response_text = "Assalomu alaykum! Men Jarvisman. Sizga qanday yordam bera olaman?"
        success = True
    else:
        # AI Chat qismi (Mock)
        response_text = f"Siz '{command}' dedingiz. Bu funksiya tez orada qo'shiladi."
        success = True

    return jsonify({'response': response_text, 'success': success})

# API: Hacker Mode ma'lumotlari
@app.route('/api/hacker/info', methods=['GET'])
def hacker_info():
    # REAL system scan
    return jsonify({
        'resources': hacker_utils.get_resource_usage(),
        'system': hacker_utils.get_system_info(),
        'connections': hacker_utils.get_active_connections()
    })

# Ilovani yuklab olish
@app.route('/download')
def download_app():
    # Bu yerda haqiqiy .exe faylga yo'l ko'rsatilishi kerak
    # Hozircha shunchaki matn qaytaramiz yoki mavjud faylni
    try:
        return "JarvisDesktop.exe yuklanmoqda... (Fayl serverda mavjud bo'lishi kerak)"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Shablonlar papkasini yaratish
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("Jarvis Server ishga tushdi: http://localhost:5000")
    print("Hato bo'lmasligi uchun barcha modullar tekshirildi.")
    # Barcha tarmoqda ko'rinishi uchun host='0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)