from .ai_services import get_ai_response

async def generate_code(language: str, task_description: str) -> str:
    """
    Berilgan talablar asosida turli dasturlash tillarida kod generatsiya qiladi.

    Args:
        language: Kod yozilishi kerak bo'lgan dasturlash tili (masalan, 'Python', 'JavaScript').
        task_description: Kod nima qilishi kerakligi haqida batafsil tavsif.

    Returns:
        Generatsiya qilingan kodni o'z ichiga olgan formatlangan matn.
    """
    # AI uchun maxsus tizim xabari
    system_prompt = f"""
    You are an expert programmer specializing in {language}.
    Your task is to generate clean, efficient, and complete code based on the user's request.
    Provide only the raw code block, without any extra explanations, introductions, or markdown formatting.
    The code should be ready to be copied and run.
    """

    # Foydalanuvchi so'rovini AI'ga yuborish
    generated_code = await get_ai_response(f"Task: {task_description}", system_prompt=system_prompt)

    # Natijani frontend uchun chiroyli formatda qaytarish
    response = f"Mana, {language} tilida so'ralgan kod:\n\n```{language.lower()}\n{generated_code}\n```"
    
    return response