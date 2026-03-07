# JARVIS 3D (Uzbek)

JARVIS — 3D avatarli, ovozli Uzbek tilidagi AI yordamchi. Hugging Face Spaces ichida ishlaydi.

## Xususiyatlar
- 3D avatar (GLB) yoki fallback sfera + tutun animatsiyasi
- STT: faster-whisper (offline) → fallback SpeechRecognition
- TTS: OpenAI gpt-4o-mini-tts → fallback pyttsx3
- Lip-sync: sodda viseme taymlayni
- FastAPI endpointlari + Gradio nazorat paneli

## Strukturasi
```
project/
├── app.py
├── jarvis_core.py
├── tts_engine.py
├── stt_engine.py
├── viseme_mapper.py
├── model_loader.js
├── index.html
├── assets/
│   ├── avatar.glb (ixtiyoriy, CC0)
│   ├── smoke.png
│   └── audio/
├── .env.example
├── requirements.txt
└── README.md
```

## O'rnatish (Spaces)
- Space turini: Python (Gradio). Repo rootda `app.py` bo'ladi.
- Talablar: `requirements.txt` da berilgan.

## Ishga tushirish
1. `.env` fayl yarating (yoki Space Secrets): `OPENAI_API_KEY` qo'shing (ixtiyoriy — bo'lmasa offline).
2. `assets/avatar.glb` (CC0) va `assets/smoke.png` joylashtiring. Agar `smoke.png` bo'lmasa ham dastur ishlaydi, lekin tutun yo'q.
3. Space ishga tushganda Gradio bosh sahifa ochiladi. 3D UI uchun `/static/index.html` ga o'ting.

## API
- GET `/status`
- POST `/speak` { text, voice, lang } → { audio_path, visemes, subtitle, backend }
- POST `/listen` (multipart audio)
- POST `/command` { text } → { result, action }

## Eslatma
- pyttsx3 MP3 ga o'tkazish uchun `pydub`+`ffmpeg` kerak. Agar ffmpeg bo'lmasa WAV qaytishi mumkin.
- faster-whisper `tiny` modeli ishlatiladi; CPUda sekin bo'lishi mumkin.
- Barcha loglar va xabarlar o'zbek tilida minimal uslubda.
