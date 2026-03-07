from typing import Optional

class STTEngine:
    def __init__(self):
        try:
            from faster_whisper import WhisperModel  # type: ignore
            self._whisper_available = True
            self._model = WhisperModel("tiny", device="cpu", compute_type="int8")
        except Exception:
            self._whisper_available = False
            self._model = None
        try:
            import speech_recognition as sr  # type: ignore
            self._sr = sr.Recognizer()
            self._sr_available = True
        except Exception:
            self._sr = None
            self._sr_available = False

    def transcribe(self, file_path: str) -> str:
        if self._whisper_available and self._model is not None:
            try:
                segments, _ = self._model.transcribe(file_path, language="uz")
                text = " ".join([s.text for s in segments]).strip()
                return text or ""
            except Exception:
                pass
        if self._sr_available and self._sr:
            try:
                import speech_recognition as sr  # type: ignore
                with sr.AudioFile(file_path) as source:
                    audio = self._sr.record(source)
                    return self._sr.recognize_sphinx(audio)
            except Exception:
                return ""
        return ""
