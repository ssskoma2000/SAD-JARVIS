from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from command_handler import CommandHandler

app = FastAPI()

# Xavfsizlik sozlamalari (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

command_handler = CommandHandler()

# Ilovani yuklab olish uchun endpoint
@app.get("/download/app")
async def download_app():
    # Bu yerda haqiqiy .exe yoki o'rnatuvchi fayl manzili bo'lishi kerak
    # Hozircha test uchun buyruqlar faylini beramiz
    file_path = "buyruqlar.zip" 
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/zip', filename="Jarvis_Setup.zip")
    return {"error": "O'rnatuvchi fayl topilmadi"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client ulandi")
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "audio_command":
                # Audio kelganda (STT logikasi shu yerda bo'lishi kerak)
                # Hozircha audioni matnga o'girish o'rniga simulyatsiya qilamiz
                print("Audio qabul qilindi")
                response_text = await command_handler.handle("salom") 
                await websocket.send_json({
                    "type": "response", 
                    "text": response_text
                })
                
            elif data.get("type") == "text_command":
                 text = data.get("text")
                 response_text = await command_handler.handle(text)
                 await websocket.send_json({
                     "type": "response", 
                     "text": response_text
                 })
    except WebSocketDisconnect:
        print("Client uzildi")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)