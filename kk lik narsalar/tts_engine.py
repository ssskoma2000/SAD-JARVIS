import os
import time
from pathlib import Path
from typing import Tuple, List, Optional, Dict

from viseme_mapper import map_text_to_visemes

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore

try:
    import pyttsx3
except Exception:
    pyttsx3 = None  # type: ignore

try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None  # type: ignore


class TTSEngine:
    def __init__(self, openai_api_key: str, out_dir: Path):
        self.out_dir = Path(out_dir)
        self.api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key) if (OpenAI and openai_api_key) else None
        self._sheva: Dict[str, Dict[str, Optional[float]]] = {
            "toshkent": {"rate": 180.0, "pitch": 50.0, "suffix": None},
            "samarqand": {"rate": 160.0, "pitch": 45.0, "suffix": " — azizim"},
            "buxoro": {"rate": 170.0, "pitch": 48.0, "suffix": " — jonim"},
            "andijon": {"rate": 190.0, "pitch": 52.0, "suffix": " — aka"},
            "fargona": {"rate": 185.0, "pitch": 51.0, "suffix": " — uka"},
            "namangan": {"rate": 185.0, "pitch": 51.0, "suffix": None},
            "qashqadaryo": {"rate": 165.0, "pitch": 47.0, "suffix": None},
            "xorazm": {"rate": 175.0, "pitch": 49.0, "suffix": None},
            "navoiy": {"rate": 170.0, "pitch": 49.0, "suffix": None},
            "surxondaryo": {"rate": 175.0, "pitch": 50.0, "suffix": None},
            "jizzax": {"rate": 170.0, "pitch": 48.0, "suffix": None},
            "qarakalpoq": {"rate": 160.0, "pitch": 45.0, "suffix": None},
        }

    def backend_name(self) -> str:
        return "OpenAI" if self.client else ("pyttsx3" if pyttsx3 else "none")

    def _tts_openai(self, text: str, voice: str, lang: str) -> Tuple[str, List[dict], str]:
        ts = int(time.time() * 1000)
        out_mp3 = str(self.out_dir / f"tts_{ts}.mp3")
        try:
            assert self.client is not None
            with self.client.audio.speech.with_streaming_response.create(
                model=os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
                voice=voice or "alloy",
                input=text,
                format="mp3",
            ) as response:
                response.stream_to_file(out_mp3)
            visemes = map_text_to_visemes(text)
            return out_mp3, visemes, "OpenAI"
        except Exception:
            # Fallback to local
            return self._tts_local(text)

    def _tts_local(self, text: str, rate: Optional[float] = None) -> Tuple[str, List[dict], str]:
        ts = int(time.time() * 1000)
        wav_path = self.out_dir / f"tts_{ts}.wav"
        if pyttsx3 is None:
            # No TTS available
            with open(self.out_dir / f"tts_{ts}.txt", "w", encoding="utf-8") as f:
                f.write(text)
            return str(wav_path), map_text_to_visemes(text), "none"
        try:
            engine = pyttsx3.init()
            # Try to set male voice if available
            for v in engine.getProperty('voices'):
                if 'male' in (v.name or '').lower() or 'male' in (v.id or '').lower():
                    engine.setProperty('voice', v.id)
                    break
            engine.setProperty('rate', int(rate or 170))
            engine.save_to_file(text, str(wav_path))
            engine.runAndWait()
            # Convert to mp3 if possible
            mp3_path = self.out_dir / (wav_path.stem + ".mp3")
            if AudioSegment is not None:
                try:
                    AudioSegment.from_wav(str(wav_path)).export(str(mp3_path), format="mp3")
                    if wav_path.exists():
                        try:
                            wav_path.unlink()
                        except Exception:
                            pass
                    return str(mp3_path), map_text_to_visemes(text), "pyttsx3"
                except Exception:
                    pass
            return str(wav_path), map_text_to_visemes(text), "pyttsx3"
        except Exception:
            return str(wav_path), map_text_to_visemes(text), "none"

    def synthesize(self, text: str, voice: str = "alloy", lang: str = "uz", dialect: Optional[str] = None) -> Tuple[str, List[dict], str]:
        d = (dialect or os.getenv("VOICE_PROFILE") or "").strip().lower()
        suffix = None
        rate = None
        if d in self._sheva:
            prof = self._sheva[d]
            rate = prof.get("rate")
            suffix = prof.get("suffix")
        final_text = text + (suffix or "")
        if self.client:
            return self._tts_openai(final_text, voice, lang)
        return self._tts_local(final_text, rate=rate)
