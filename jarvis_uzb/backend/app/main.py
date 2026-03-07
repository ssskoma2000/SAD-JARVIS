from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import json
from typing import Annotated
from sqlalchemy.orm import Session

# AI xizmatlarini import qilish
from app.ai_services import transcribe_audio
# Xavfsizlik funksiyalarini import qilish
from app.security import create_access_token, get_current_user_from_token, verify_password
# Ma'lumotlar bazasi bilan ishlash uchun importlar
from . import crud, models, schemas, command_handler
from .database import SessionLocal, engine, get_db
# Logger'ni import qilish
from .logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jarvis AI Backend")

# Frontend (localhost:3000) dan keladigan so'rovlarga ruxsat berish (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Jarvis AI Backend ishlamoqda"}

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Yangi foydalanuvchini ro'yxatdan o'tkazadi."""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Bu nomdagi foydalanuvchi mavjud")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Foydalanuvchi nomi va parol orqali JWT token yaratadi.
    """
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi nomi yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"Foydalanuvchi '{form_data.username}' tizimga muvaffaqiyatli kirdi.")
    return {"access_token": access_token, "token_type": "bearer"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    """
    WebSocket orqali real-time aloqa uchun endpoint.
    Faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun ishlaydi.
    """
    username = await get_current_user_from_token(token, db)
    await websocket.accept()
    logger.info(f"WebSocket ulanishi o'rnatildi: {username}")
    try:
        while True:
            # Frontend'dan Blob sifatida yuborilgan ovozli ma'lumotlarni bayt ko'rinishida qabul qilish
            audio_bytes = await websocket.receive_bytes()
            
            # Ovozni matnga o'girish
            transcribed_text = await transcribe_audio(audio_bytes)
            logger.info(f"Foydalanuvchi '{username}' buyruq yubordi: '{transcribed_text}'")
            
            # Matnli buyruqni qayta ishlash
            response_data = await command_handler.process_command(transcribed_text, username)
            
            # Natijani JSON formatida klientga yuborish
            await websocket.send_json(response_data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket ulanishi uzildi: {username}")
    except Exception as e:
        logger.error(f"WebSocket'da kutilmagan xatolik ({username}): {e}", exc_info=True)
        # Xatolik yuz berganda klientga xabar yuborish
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.send_json({"text": "Serverda xatolik yuz berdi.", "audio_base64": ""})
    