import os
import datetime
from collections import deque
from typing import Tuple, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore


class JarvisCore:
    def __init__(self, openai_api_key: str = "", memory_size: int = 5):
        self.memory = deque(maxlen=memory_size)
        self.api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key) if (OpenAI and openai_api_key) else None

    def remember(self, user_text: str, assistant_text: str):
        self.memory.append({"user": user_text, "assistant": assistant_text})

    def handle_command(self, text: str) -> Tuple[str, Optional[str]]:
        t = text.lower().strip()
        now = datetime.datetime.now().strftime("%H:%M")
        if any(k in t for k in ["qayta ayt", "yana ayt", "qaytar"]):
            # Repeat last assistant response if available
            if self.memory:
                last = self.memory[-1].get("assistant") or "Oxirgi javob yo'q."
                return last, "repeat_last"
            return "Oxirgi javob yo'q.", "repeat_last"
        if any(k in t for k in ["vaqt", "soat", "time"]):
            return f"Hozir soat {now}.", "tell_time"
        if any(k in t for k in ["sayt", "och", "open", "veb"]):
            return "Saytni ochish uchun havola yuboraman.", "open_site:https://huggingface.co/spaces"
        if any(k in t for k in ["musiqa", "ijro", "play music"]):
            return "Mahalliy musiqa ijro etilmoqda (demo).", "play_music:assets/audio/sample.mp3"
        if "men kimman" in t:
            return "Siz komandir, loyihaning asoschisisiz.", "affirm_identity"
        if any(k in t for k in ["holat", "status"]):
            return "Tizim barqaror ishlamoqda.", "system_status"
        # Default: ask LLM if available
        response = None
        if self.client:
            try:
                resp = self.client.chat.completions.create(
                    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": "Siz JARVIS. Siz faqat o'zbek tilida javob berasiz."},
                        *[{"role": "user", "content": m["user"]} for m in self.memory],
                        {"role": "user", "content": text},
                    ],
                    temperature=0.6,
                )
                response = resp.choices[0].message.content
            except Exception:
                response = None
        if not response:
            response = "Kechirasiz, internetga ulanishsiz qisqa javob bera olaman. So'rovingizni soddalashtiring."
        self.remember(text, response)
        return response, None
