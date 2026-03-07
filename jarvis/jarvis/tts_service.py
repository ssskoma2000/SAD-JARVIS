from gtts import gTTS
from pathlib import Path
import uuid

OUT_DIR = Path(__file__).resolve().parents[1] / "logs" / "tts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def synthesize_uzbek(text: str, filename: str | None = None) -> str:
    """Synthesize Uzbek text to an mp3 file and return path."""
    fn = filename or f"tts_{uuid.uuid4().hex}.mp3"
    out_path = OUT_DIR / fn
    tts = gTTS(text=text, lang="uz")
    tts.save(str(out_path))
    return str(out_path)
