import os
import time
from pathlib import Path
from typing import Optional
import json
import base64
import hashlib

import gradio as gr
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from jarvis_core import JarvisCore
from tts_engine import TTSEngine
from stt_engine import STTEngine
from auth import AuthManager

# Ensure directories
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
NOTES_DIR = ASSETS_DIR / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)
QR_DIR = ASSETS_DIR / "qr"
QR_DIR.mkdir(parents=True, exist_ok=True)
SCREENS_DIR = ASSETS_DIR / "screens"
SCREENS_DIR.mkdir(parents=True, exist_ok=True)

# Load env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize engines
jarvis = JarvisCore(openai_api_key=OPENAI_API_KEY)
tts = TTSEngine(openai_api_key=OPENAI_API_KEY, out_dir=AUDIO_DIR)
stt = STTEngine()
auth = AuthManager(BASE_DIR, jwt_secret=os.getenv("JWT_SECRET", "change_this_secret"))

# Optional deps
try:
    import qrcode
except Exception:
    qrcode = None
try:
    import speedtest
except Exception:
    speedtest = None
try:
    import pyautogui
except Exception:
    pyautogui = None
try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None

app = FastAPI(title="JARVIS 3D Assistant", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets and frontend
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static")


class SpeakRequest(BaseModel):
    text: str
    voice: Optional[str] = "alloy"
    lang: Optional[str] = "uz"
    dialect: Optional[str] = None


class SpeakResponse(BaseModel):
    audio_path: str
    visemes: list
    subtitle: str
    backend: str


class CommandRequest(BaseModel):
    text: str


class CommandResponse(BaseModel):
    result: str
    action: Optional[str] = None


@app.get("/status")
def status():
    return {
        "status": "ok",
        "tts_backend": tts.backend_name(),
        "model": "connected" if OPENAI_API_KEY else "fallback",
        "language": "uz",
        "admin_setup_required": auth.first_run(),
    }


@app.post("/speak", response_model=SpeakResponse)
def speak(req: SpeakRequest):
    text = req.text.strip()
    if not text:
        text = "Matn bo'sh. Iltimos, so'rov yuboring."
    audio_path, visemes, backend = tts.synthesize(text=text, voice=req.voice, lang=req.lang, dialect=req.dialect)
    subtitle = text
    # Return relative path for the frontend
    rel_path = f"/assets/audio/{Path(audio_path).name}"
    return SpeakResponse(audio_path=rel_path, visemes=visemes, subtitle=subtitle, backend=backend)


@app.post("/listen")
async def listen(file: UploadFile = File(...)):
    # Save temp file
    tmp = AUDIO_DIR / f"mic_{int(time.time()*1000)}_{file.filename}"
    with tmp.open("wb") as f:
        f.write(await file.read())
    text = stt.transcribe(str(tmp))
    return {"text": text}


@app.post("/command", response_model=CommandResponse)
def command(req: CommandRequest):
    result, action = jarvis.handle_command(req.text or "")
    return CommandResponse(result=result, action=action)


# ----------------- Admin Auth -----------------
class RegisterRequest(BaseModel):
    password: str


class LoginRequest(BaseModel):
    password: str


@app.post("/auth/register")
def auth_register(req: RegisterRequest):
    if not auth.first_run():
        return {"ok": False, "msg": "Allaqachon sozlangan"}
    ok = auth.register_admin(req.password)
    return {"ok": ok}


@app.post("/auth/login")
def auth_login(req: LoginRequest):
    if not auth.admin_enabled():
        return {"ok": False, "msg": "Avval ro'yxatdan o'ting"}
    if not auth.verify_admin(req.password):
        return {"ok": False, "msg": "Parol noto'g'ri"}
    token = auth.mint_jwt()
    return {"ok": True, "token": token}


def _is_admin(authorization: Optional[str]) -> bool:
    if not authorization:
        return False
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return auth.verify_jwt(parts[1])
    return False


# ----------------- Admin-only actions -----------------
class AdminCmd(BaseModel):
    action: str
    payload: Optional[dict] = None


@app.post("/admin/command")
def admin_command(cmd: AdminCmd, authorization: Optional[str] = None):
    if not _is_admin(authorization):
        return {"ok": False, "msg": "Ruxsat yo'q"}
    act = (cmd.action or "").lower()
    payload = cmd.payload or {}
    # Only safe, in-app actions
    if act == "open_url":
        url = payload.get("url", "")
        if not url.startswith("http"):
            return {"ok": False, "msg": "Noto'g'ri URL"}
        # Frontend should actually open it; here we just acknowledge
        return {"ok": True, "msg": f"URL tayyor: {url}"}
    if act == "play_music":
        fname = payload.get("file", "sample.mp3")
        path = AUDIO_DIR / fname
        if not path.exists():
            return {"ok": False, "msg": "Fayl topilmadi"}
        return {"ok": True, "audio": f"/assets/audio/{fname}"}
    if act == "write_note":
        text = payload.get("text", "")
        ts = int(time.time()*1000)
        p = NOTES_DIR / f"note_{ts}.txt"
        p.write_text(text, encoding="utf-8")
        return {"ok": True, "path": f"/assets/notes/{p.name}"}
    if act == "toggle_flag":
        key = payload.get("key", "flag")
        val = bool(payload.get("value", False))
        # Store ephemeral flag in a file
        flags_file = BASE_DIR / ".flags.json"
        import json
        data = {}
        if flags_file.exists():
            try:
                data = json.loads(flags_file.read_text(encoding="utf-8"))
            except Exception:
                data = {}
        data[key] = val
        flags_file.write_text(json.dumps(data), encoding="utf-8")
        return {"ok": True, "msg": f"{key}={val}"}
    if act == "generate_qr":
        if qrcode is None:
            return {"ok": False, "msg": "QR kutubxonasi o'rnatilmagan"}
        text = payload.get("text", "")
        ts = int(time.time()*1000)
        out = QR_DIR / f"qr_{ts}.png"
        img = qrcode.make(text)
        img.save(out)
        return {"ok": True, "path": f"/assets/qr/{out.name}"}
    if act == "speedtest":
        if speedtest is None:
            return {"ok": False, "msg": "speedtest kutubxonasi yo'q"}
        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            dl = s.download() / 1e6
            ul = s.upload() / 1e6
            return {"ok": True, "download_mbps": round(dl,2), "upload_mbps": round(ul,2)}
        except Exception as e:
            return {"ok": False, "msg": str(e)}
    if act == "screenshot":
        if pyautogui is None:
            return {"ok": False, "msg": "pyautogui yo'q"}
        try:
            ts = int(time.time()*1000)
            out = SCREENS_DIR / f"screen_{ts}.png"
            img = pyautogui.screenshot()
            img.save(out)
            return {"ok": True, "path": f"/assets/screens/{out.name}"}
        except Exception as e:
            return {"ok": False, "msg": str(e)}
    if act == "encrypt_text":
        if Fernet is None:
            return {"ok": False, "msg": "cryptography yo'q"}
        txt = (payload.get("text") or "").encode("utf-8")
        if not txt:
            return {"ok": False, "msg": "Matn yo'q"}
        secret = os.getenv("JWT_SECRET", "change_this_secret").encode("utf-8")
        key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
        f = Fernet(key)
        token = f.encrypt(txt).decode("utf-8")
        return {"ok": True, "token": token}
    if act == "decrypt_text":
        if Fernet is None:
            return {"ok": False, "msg": "cryptography yo'q"}
        token = payload.get("token") or ""
        if not token:
            return {"ok": False, "msg": "Token yo'q"}
        try:
            secret = os.getenv("JWT_SECRET", "change_this_secret").encode("utf-8")
            key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
            f = Fernet(key)
            txt = f.decrypt(token.encode("utf-8")).decode("utf-8")
            return {"ok": True, "text": txt}
        except Exception as e:
            return {"ok": False, "msg": str(e)}
    if act == "email_draft":
        subject = payload.get("subject", "")
        points = payload.get("points", []) or []
        body = "Assalomu alaykum,\n\n" + ("Mavzu: " + subject + "\n\n" if subject else "")
        if points:
            body += "Quyidagilarni taqdim etaman:\n" + "\n".join([f"- {p}" for p in points]) + "\n\n"
        body += "Hurmat bilan,\nJARVIS yordamchingiz"
        return {"ok": True, "draft": body}
    if act == "reminder_add":
        text = payload.get("text", "").strip()
        when = payload.get("when", "").strip()
        if not text:
            return {"ok": False, "msg": "Matn kerak"}
        store = BASE_DIR / "reminders.json"
        data = []
        if store.exists():
            try:
                data = json.loads(store.read_text(encoding="utf-8"))
            except Exception:
                data = []
        item = {"id": int(time.time()*1000), "text": text, "when": when}
        data.append(item)
        store.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True, "item": item}
    if act == "reminder_list":
        store = BASE_DIR / "reminders.json"
        if not store.exists():
            return {"ok": True, "items": []}
        try:
            data = json.loads(store.read_text(encoding="utf-8"))
        except Exception:
            data = []
        return {"ok": True, "items": data}
    return {"ok": False, "msg": "Noma'lum amal"}


# ---------- Gradio UI (simple control panel) ----------

def gradio_ui():
    with gr.Blocks(title="JARVIS 3D") as demo:
        gr.Markdown("## JARVIS 3D — Uzbek tilida\nHolat paneli va tezkor test.")
        with gr.Row():
            status_box = gr.JSON(label="Holat")
            refresh = gr.Button("Holatni yangila")
        with gr.Row():
            txt = gr.Textbox(label="So'rov matni", placeholder="Salom, komandir! Bugun nima topshiriq?")
            speak_btn = gr.Button("So'rov yuborish")
        with gr.Row():
            audio_out = gr.Audio(label="Javob audio", interactive=False)
            subtitle = gr.Textbox(label="Subtitr", interactive=False)
        with gr.Row():
            backend_used = gr.Textbox(label="TTS backend", interactive=False)
        
        def do_status():
            from fastapi.testclient import TestClient
            client = TestClient(app)
            r = client.get("/status")
            return r.json()
        
        def do_speak(text):
            if not text:
                text = "Salom, komandir! Bugun nima topshiriq?"
            from fastapi.testclient import TestClient
            client = TestClient(app)
            r = client.post("/speak", json={"text": text, "voice": "alloy", "lang": "uz"})
            data = r.json()
            # Build absolute path for gradio audio component
            file_path = str(AUDIO_DIR / Path(data["audio_path"]).name)
            return file_path, data.get("subtitle", ""), data.get("backend", "?")
        
        refresh.click(fn=do_status, outputs=status_box)
        speak_btn.click(fn=do_speak, inputs=txt, outputs=[audio_out, subtitle, backend_used])
        
        gr.Markdown("### Frontend 3D sahifa\nUshbu URL orqali 3D interfeysni oching: <a href='/static/index.html' target='_blank'>/static/index.html</a>")
    return demo


# Expose Gradio on root for Spaces convenience
try:
    # Newer Gradio exposes mount_gradio_app helper
    from fastapi import FastAPI as _FastAPI
    demo = gradio_ui()
    app = gr.mount_gradio_app(app, demo, path="/")
except Exception:
    # Fallback: do nothing, FastAPI will still serve endpoints
    pass
