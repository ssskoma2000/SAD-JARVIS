import os
import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# .env faylidan API kalitni yuklash
load_dotenv()

# OpenAI klientini sozlash
# Foydalanuvchi o'zining API kalitini .env fayliga OPENAI_API_KEY nomi bilan saqlashi kerak
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY topilmadi. Iltimos, .env fayliga qo'shing.")

client = OpenAI(api_key=api_key)

async def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Ovozli ma'lumotlarni OpenAI Whisper yordamida matnga o'giradi (STT).

    Args:
        audio_bytes: Ovoz faylining baytlari.

    Returns:
        Transkripsiya qilingan matn.
    """
    try:
        # Ovoz baytlarini vaqtinchalik faylga yozish, chunki Whisper API fayl ob'ektini talab qiladi.
        # Formatni (masalan, .wav yoki .mp3) frontend yuboradigan formatga moslash kerak.
        temp_audio_path = Path("temp_audio.wav")
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        with open(temp_audio_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="uz"  # O'zbek tilini belgilash
            )

        # Vaqtinchalik faylni o'chirish
        os.remove(temp_audio_path)

        return transcription.text
    except Exception as e:
        print(f"Xatolik: Whisper STT muvaffaqiyatsiz bo'ldi: {e}")
        return ""

async def get_ai_response(text: str) -> str:
    """
    Berilgan matn asosida OpenAI GPT-4 yordamida javob generatsiya qiladi.

    Args:
        text: Foydalanuvchidan kelgan matn.

    Returns:
        AI tomonidan generatsiya qilingan javob matni.
    """
    try:
        system_prompt = """
        Siz Jarvis, Koma (Nuraliev Javohir) tomonidan yaratilgan ilg'or sun'iy intellekt yordamchisisiz.
        Sizning vazifangiz foydalanuvchiga yordam berish, buyruqlarni bajarish va suhbatlashish.
        Javoblaringizni qisqa, aniq va professional ohangda, o'zbek tilida bering.
        """
        response = await client.chat.completions.create(
            model="gpt-4-turbo",  # Yoki "gpt-4"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Xatolik: GPT-4 javobini olishda muammo: {e}")
        return "Kechirasiz, hozir javob bera olmayman."

async def generate_speech_from_text(text: str) -> str:
    """
    Matnni OpenAI TTS yordamida ovozga aylantiradi va base64 formatida qaytaradi.

    Args:
        text: Ovozga aylantirilishi kerak bo'lgan matn.

    Returns:
        Ovoz faylining base64 kodlangan ko'rinishi.
    """
    try:
        response = await client.audio.speech.create(
            model="tts-1",       # Yoki "tts-1-hd" yuqori sifat uchun
            voice="alloy",     # Mavjud ovozlardan biri: alloy, echo, fable, onyx, nova, shimmer
            input=text,
            response_format="mp3" # Yoki "wav", "opus"
        )

        # Ovoz baytlarini to'g'ridan-to'g'ri base64 ga o'tkazish
        audio_bytes = response.read()
        base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
        return base64_audio
    except Exception as e:
        print(f"Xatolik: OpenAI TTS muvaffaqiyatsiz bo'ldi: {e}")
        return ""