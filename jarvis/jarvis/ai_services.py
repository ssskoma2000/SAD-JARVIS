import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = "You are Jarvis, an Uzbek AI assistant. Reply concisely in Uzbek. Only suggest safe actions; do not provide destructive system commands."

def ai_fallback_response(prompt: str, max_tokens: int = 256) -> str:
    """Call OpenAI ChatCompletion to get an Uzbek response. Returns text."""
    if not OPENAI_API_KEY:
        return "Jarvis: AI xizmatiga ulanmagan. Iltimos, server konfiguratsiyasini tekshiring."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=max_tokens, temperature=0.2)
    # Fallback safety
    try:
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Jarvis: AI javobini olishda xatolik yuz berdi."
