import re
from typing import Dict, Any, List

# Niyatlar va ularni aniqlash uchun kalit so'zlar/regexlar
INTENT_DEFINITIONS = {
    "open_app": {
        "keywords": ["och", "ishga tushur"],
        "entities": ["chrome", "telegram", "terminal", "fayl menejeri", "vs code"]
    },
    "open_website": {
        "keywords": ["saytini och", "ga kir"],
        "entities": ["kun.uz", "daryo.uz", "google.com", "youtube.com"]
    },
    "control_volume": {
        "keywords": ["ovozni", "musiqani"],
        "entities": ["oshir", "pasaytir", "ko'tar", "tushir", "%", "foizga"]
    },
    "control_window": {
        "keywords": ["oynani", "aktiv oynani"],
        "entities": ["yop", "pastga tushur", "kattalashtir", "yashir"]
    },
    "system_control": {
        "keywords": ["kompyuterni", "tizimni"],
        "entities": ["o'chir", "qayta yukla", "uxlat"]
    },
    "tell_story": {
        "keywords": ["ertak ayt", "hikoya aytib ber"],
        "entities": []
    },
    "tell_time": {
        "keywords": ["soat nechi", "vaqt nechi"],
        "entities": []
    }
}

class IntentParser:
    """
    Foydalanuvchi matnidan niyat (intent) va obyektlarni (entities) ajratib oladi.
    """
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Matnni tahlil qilib, niyat va obyektlarni topadi.
        
        Returns:
            Masalan: {"intent": "open_app", "entities": {"app_name": "chrome"}, "confidence": 0.9}
        """
        text = text.lower()
        
        # 1-bosqich: Kalit so'zlar orqali oddiy tahlil
        for intent, definition in INTENT_DEFINITIONS.items():
            for keyword in definition["keywords"]:
                if keyword in text:
                    # Niyat topildi, endi obyektlarni qidiramiz
                    found_entities = {}
                    for entity in definition["entities"]:
                        if entity in text:
                            # Obyekt nomini va turini aniqlash (bu qismni murakkablashtirish mumkin)
                            if intent == "open_app":
                                found_entities["app_name"] = entity
                            elif intent == "control_volume":
                                # Foizni ajratib olish
                                match = re.search(r'(\d+)', text)
                                if match:
                                    found_entities["level"] = int(match.group(1))
                                # Yo'nalishni aniqlash
                                if any(act in text for act in ["oshir", "ko'tar"]):
                                    found_entities["direction"] = "up"
                                elif any(act in text for act in ["pasaytir", "tushir"]):
                                    found_entities["direction"] = "down"

                    # Agar obyektlar ham topilsa, niyatni ishonchli deb hisoblash
                    if found_entities or not definition["entities"]:
                         return {
                            "intent": intent,
                            "entities": found_entities,
                            "original_text": text,
                            "confidence": 0.9 # Ishonch darajasi (oddiy usulda)
                        }

        # 2-bosqich: Agar oddiy tahlil natija bermasa
        # Kelajakda bu yerga AI orqali niyatni aniqlash logikasi qo'shiladi
        return {
            "intent": "unknown",
            "entities": {},
            "original_text": text,
            "confidence": 0.0
        }

# Test uchun
if __name__ == '__main__':
    parser = IntentParser()
    test_phrases = [
        "Chrome dasturini ochib yubor",
        "Ovozni 30 foizga pasaytir",
        "Ertak aytib ber",
        "Bugun havo qanday bo'ladi?",
        "Joriy oynani yop"
    ] 
    
    for phrase in test_phrases:
        result = parser.parse(phrase)
        print(f"Matn: '{phrase}'")
        print(f"  -> Natija: {result}\n")
