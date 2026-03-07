import re
from typing import List, Dict

# Simple Uzbek phoneme to viseme mapping (approximate)
VOWEL = "VOWEL"
CONS = "CONS"

PHONEME_TO_VISEME = {
    'a': 'A', 'o': 'O', 'u': 'U', 'i': 'I', 'e': 'E', 'ö': 'O', 'ó': 'O', 'ü': 'U', 'â': 'A',
    'b': 'BMP', 'm': 'BMP', 'p': 'BMP',
    'f': 'FV', 'v': 'FV',
    't': 'TD', 'd': 'TD', 's': 'SZ', 'z': 'SZ', 'c': 'SZ',
    'k': 'KG', 'g': 'KG', 'q': 'KG', 'ğ': 'KG',
    'l': 'L', 'r': 'R', 'y': 'Y', 'n': 'N', 'h': 'H', 'j': 'SH', 'sh': 'SH', 'ch': 'CH', 'ng': 'NG'
}

DEFAULT_VISEME = 'REST'


def tokenize(text: str) -> List[str]:
    t = text.lower()
    t = re.sub(r"[^a-záéíóúöüğşıçq'’ ]", " ", t)
    # Handle digraphs first
    tokens: List[str] = []
    i = 0
    while i < len(t):
        if i + 1 < len(t) and t[i:i+2] in ("sh", "ch", "ng"):
            tokens.append(t[i:i+2])
            i += 2
        else:
            tokens.append(t[i])
            i += 1
    return [tok for tok in tokens if tok.strip()]


def map_text_to_visemes(text: str) -> List[Dict]:
    tokens = tokenize(text)
    visemes: List[Dict] = []
    time_ms = 0
    for tok in tokens:
        if tok == ' ':
            time_ms += 40
            continue
        v = PHONEME_TO_VISEME.get(tok, DEFAULT_VISEME)
        visemes.append({"viseme": v, "time": time_ms})
        time_ms += 90
    return visemes
