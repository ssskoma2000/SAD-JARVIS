import asyncio

class AIService:
    """
    Sun'iy intellekt xizmatlari bilan ishlash uchun klass.
    """
    async def get_intent_from_ai(self, text: str, tools: list):
        # Haqiqiy OpenAI integratsiyasi shu yerda bo'ladi.
        # Hozircha test uchun oddiy javob qaytaramiz.
        return {"intent": "unknown", "entities": {}}

    async def get_chat_response(self, text: str, system_prompt: str = None):
        # Chat rejimi uchun javob
        await asyncio.sleep(1) # O'ylash jarayonini imitatsiya qilish
        return f"Siz '{text}' dedingiz, lekin men hozircha faqat buyruqlarni bajarishga o'rgatilganman."