import telebot
import subprocess
import os
import re # Regular expression

# Telegram bot tokenini .env faylidan olish
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Agar token topilmasa, xatolik chiqarish
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Telegram bot tokeni topilmadi. Iltimos, .env fayliga 'TELEGRAM_BOT_TOKEN=' qatorini qo'shing va tokeningizni kiriting.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# C++ bajariladigan faylning yo'li
CPP_EXECUTABLE_PATH = "./build/jarvis"

# --- Yordamchi funksiyalar ---
def run_cpp_command(command):
    """C++ dasturiga buyruq yuboradi va natijani qaytaradi."""
    try:
        result = subprocess.run([CPP_EXECUTABLE_PATH, command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Xatolik: {e.stderr.strip()}"
    except FileNotFoundError:
        return f"Xatolik: {CPP_EXECUTABLE_PATH} fayli topilmadi. Iltimos, C++ dasturini qurilganligini tekshiring."

# --- Telegram handlerlari ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """/start yoki /help buyruqlariga javob beradi."""
    bot.reply_to(message,
                 "Assalomu alaykum! Men Jarvisman, sizning Telegramdagi yordamchingiz.\n"
                 "Menga buyruqlar yuboring, masalan:\n"
                 "/vaqt - Hozirgi vaqtni aytadi\n"
                 "/ovoz balandligi 50 - Ovozni 50% ga o'rnatadi\n"
                 "/yoruglik 75 - Yorug'likni 75% ga o'rnatadi\n"
                 "Musiqa qo'y [nomi] - YouTube yoki lokal musiqani ochadi\n"
                 "Yoki oddiy matn yuboring, men ularni C++ Jarvisga yuboraman."
                 )

@bot.message_handler(commands=['vaqt'])
def get_time(message):
    """/vaqt buyrug'iga javob beradi."""
    result = run_cpp_command("vaqt")
    bot.reply_to(message, result)

@bot.message_handler(regexp=re.compile(r"ovoz balandligi (\d+)"))
def handle_volume(message):
    """Ovoz balandligini o'zgartirish buyrug'ini bajaradi."""
    try:
        level = message.text.split()[-1]
        result = run_cpp_command(f"ovozni {level} ga qo'y")
        bot.reply_to(message, result)
    except ValueError:
        bot.reply_to(message, "Noto'g'ri format. Iltimos, raqam kiriting (0-100).")

@bot.message_handler(regexp=re.compile(r"yoruglik (\d+)"))
def handle_brightness(message):
    """Ekran yorug'ligini o'zgartirish buyrug'ini bajaradi."""
    try:
        level = message.text.split()[-1]
        result = run_cpp_command(f"yorug'likni {level} ga qo'y")
        bot.reply_to(message, result)
    except ValueError:
        bot.reply_to(message, "Noto'g'ri format. Iltimos, raqam kiriting (0-100).")

@bot.message_handler(func=lambda msg: msg.text.lower().startswith("musiqa qo'y"))
def play_music(message):
    """Musiqa qo'yish buyrug'ini bajaradi."""
    result = run_cpp_command(message.text)
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Foydalanuvchi yuborgan barcha matnlarni C++ Jarvisga yuboradi."""
    result = run_cpp_command(message.text)
    bot.reply_to(message, result)

# --- Main ---
if __name__ == '__main__':
    print("Telegram bot ishga tushdi...")
    try:
        # Botni doimiy ishlashga sozlash
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot ishlatishda xatolik: {e}")



# --- Qo'shimcha ---
# Bu faylni Telegram bot bilan ishlash uchun alohida ishga tushiring.
# Misol uchun: python3 telegram_bot.py

# --- Xavfsizlik bo'yicha eslatma ---
# * Hech qachon bot tokenini ochiq kodda saqlamang. Uni .env faylida saqlang va `os.getenv` orqali oling.
# * Har bir buyruqni bajarishdan oldin foydalanuvchini tekshiring (agar kerak bo'lsa).
# * Tizim buyruqlarini ishlatishda ehtiyot bo'ling va faqat zarur bo'lgan buyruqlarni qo'llab-quvvatlang.
# * Yorug'likni o'zgartirish buyrug'i faqat Linuxda ishlaydi. Boshqa operatsion sistemalar uchun boshqa usul kerak bo'ladi.

# --- Telegram buyruqlari ---
# /start - Botni ishga tushirish
# /help - Yordam
# /vaqt - Hozirgi vaqtni so'rash
# /ovoz balandligi <0-100> - Ovoz balandligini o'zgartirish
# /yoruglik <0-100> - Ekran yorug'ligini o'zgartirish
# Boshqa matn - C++ Jarvisga yuboriladi