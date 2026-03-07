from datetime import datetime
from typing import Optional, Dict, Any, Callable

# AI xizmatlarini import qilish
from .ai_services import get_ai_response, generate_speech_from_text
# Platforma bilan ishlash funksiyalarini import qilish
from . import platform_utils
# Kod generatsiya qilish modulini import qilish
from . import code_generator

# Shevalar va sinonimlarni hisobga olgan holda kalit so'zlar ro'yxati
OPEN_KEYWORDS = ["och", "otvor", "oching", "ochgil", "ishga tushir"]
CHROME_KEYWORDS = ["chrome", "xrom", "google chrome", "brauzer"]
FILES_KEYWORDS = ["fayl", "fayllarimni", "papka", "papkalarni", "explorer"]
SHOW_KEYWORDS = ["ko'rsat", "ko'rsating", "namoyish et"]
CODE_KEYWORDS = ["kod yoz", "kod generatsiya qil", "kodini yozib ber"]

def _check_keywords(text: str, keywords: list) -> bool:
    """Matnda kalit so'zlardan biri borligini tekshiradi."""
    return any(keyword in text for keyword in keywords)

def handle_local_command(text: str) -> Optional[Dict[str, Any]]:
    """
    Oddiy, mahalliy buyruqlarni aniqlaydi va tezkor javob qaytaradi.
    Javob sifatida bajariladigan funksiya va tasdiqlovchi matnni qaytaradi.
    """
    text_lower = text.lower()

    # --- Amaliy buyruqlar ---

    # "Chrome och"
    if _check_keywords(text_lower, OPEN_KEYWORDS) and _check_keywords(text_lower, CHROME_KEYWORDS):
        return {
            "action": platform_utils.open_chrome,
            "response": "Chrome brauzerini ochyapman.",
            "animation_triggers": [{"name": "confirm_action", "value": 1}]
        }

    # "Fayllarni ko'rsat"
    if _check_keywords(text_lower, SHOW_KEYWORDS) and _check_keywords(text_lower, FILES_KEYWORDS):
        return {
            "action": platform_utils.open_file_explorer,
            "response": "Fayl boshqaruvchini ochyapman.",
            "animation_triggers": [{"name": "confirm_action", "value": 1}]
        }

    # "Kod yoz"
    if _check_keywords(text_lower, CODE_KEYWORDS):
        # Bu yerda biz til va vazifani matndan ajratib olishimiz kerak.
        # Hozircha bu oddiy misol, kelajakda buni AI yordamida qilish mumkin.
        try:
            parts = text.split("uchun")
            language = parts[0].replace("kod yoz", "").strip() # "Python"
            task = parts[1].strip() # "salom dunyo chiqaradigan"
            return {
                "action": lambda: code_generator.generate_code(language, task),
                "is_async_action": True, # Action asinxron ekanligini belgilash
                "animation_triggers": [{"name": "coding_effect", "value": 1}]
            }
        except IndexError:
            return None # Agar format to'g'ri kelmasa, AI'ga yuboramiz

    # --- Suhbat buyruqlari ---

    # Vaqt bilan bog'liq buyruqlar
    if "soat" in text_lower and "necha" in text_lower:
        now = datetime.now()
        return {
            "action": None,
            "response": f"Hozir soat {now.strftime('%H:%M')}.",
            "animation_triggers": [{"name": "thinking", "value": 1}]
        }

    # Sana bilan bog'liq buyruqlar
    if "bugun" in text_lower and ("sana" in text_lower or "kun" in text_lower):
        now = datetime.now()
        days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        day_name = days[now.weekday()]
        return {
            "action": None,
            "response": f"Bugun {day_name}, {now.strftime('%d-%B, %Y-yil')}.",
            "animation_triggers": [{"name": "thinking", "value": 1}]
        }

    # Salomlashish
    if "salom" in text_lower or "assalomu alaykum" in text_lower:
        return {
            "action": None, # Bajariladigan amal yo'q
            "response": "Assalomu alaykum! Sizga qanday yordam bera olaman?",
            "animation_triggers": [{"name": "nod_head", "value": 1}]
        }

    # Boshqa oddiy buyruqlar shu yerga qo'shilishi mumkin
    # ...

    return None


async def process_command(text: str, username: str) -> Dict[str, Any]:
    """
    Foydalanuvchi buyrug'ini to'liq qayta ishlaydi.
    1. Mahalliy buyruqlarni tekshiradi.
    2. Agar topilmasa, AI'ga murojaat qiladi.
    3. Natijani ovozga o'giradi.
    """
    # 1-qadam: Mahalliy buyruqlarni tekshirish
    local_command_result = handle_local_command(text)
    response_data = {}

    if local_command_result:
        print(f"'{text}' uchun mahalliy buyruq topildi.")
        response_data["animation_triggers"] = local_command_result.get("animation_triggers", [])
        action = local_command_result.get("action")
        if local_command_result.get("is_async_action"):
            # Agar action asinxron bo'lsa, uni `await` bilan chaqiramiz
            response_data["text"] = await action()
        elif action:
            # Oddiy sinxron action
            action()
            response_data["text"] = local_command_result["response"]
        else:
            response_data["text"] = local_command_result["response"]
    else:
        # 2-qadam: Agar mahalliy buyruq topilmasa, AI'ga murojaat qilish
        print(f"'{text}' uchun mahalliy buyruq topilmadi. OpenAI'ga murojaat qilinmoqda...")
        response_data["text"] = await get_ai_response(text)
        # Umumiy AI javobi uchun standart animatsiya
        response_data["animation_triggers"] = [{"name": "speaking", "value": 1}]

    # 3-qadam: Matnli javobni ovozga o'girish
    response_data["audio_base64"] = await generate_speech_from_text(response_data["text"])

    return response_data