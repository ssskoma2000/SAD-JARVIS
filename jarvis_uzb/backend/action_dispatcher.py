from typing import Dict, Any
from ai_services import AIService
from command_handler import CommandHandler
from database_manager import DatabaseManager

class ActionDispatcher:
    """
    Foydalanuvchi xabarini qabul qiladi, uni qayta ishlaydi va yakuniy natijani
    (matn, audio, animatsiya) qaytaradi.
    """
    def __init__(self):
        self.ai_service = AIService()
        self.command_handler = CommandHandler()
        self.db_manager = DatabaseManager()
        print("ActionDispatcher ishga tushdi.")

    async def dispatch(self, user_message: str) -> Dict[str, Any]:
        """
        Asosiy dispetcher funksiyasi.

        1. Buyruqni `CommandHandler` orqali tahlil qiladi.
        2. Natijaviy matnni oladi.
        3. Matnni `AIService` orqali ovozga o'giradi.
        4. Animatsiya triggerlarini aniqlaydi.
        5. Yakuniy javobni yig'adi.
        """
        print(f"Dispatching message: {user_message}")

        # 1. Buyruqni qayta ishlash
        # Bu yerda ham lokal, ham AI-ga asoslangan tahlil amalga oshiriladi
        result_text = await self.command_handler.handle(user_message)
        print(f"Handler result: {result_text}")

        # 2. Matnni ovozga o'girish (TTS)
        audio_bytes = await self.ai_service.text_to_speech(result_text)
        print(f"Generated audio bytes: {len(audio_bytes) if audio_bytes else 0}")

        # 3. Animatsiya triggerlarini aniqlash (hozircha sodda)
        # Kelajakda bu niyatga (intent) qarab o'zgarishi mumkin
        animation_triggers = []
        if "ochilmoqda" in result_text.lower() or "bajarildi" in result_text.lower():
            animation_triggers.append({"name": "nod_head", "value": 1.0})

        # 4. Yakuniy javobni yig'ish
        response = {
            "text": result_text,
            "audio": audio_bytes,
            "animation_triggers": animation_triggers
        }

        return response