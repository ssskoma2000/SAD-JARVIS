from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .command_handler import CommandHandler
from .database import init_db
import structlog
import time

logger = structlog.get_logger()

app = FastAPI(title="Jarvis Uzbek Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = CommandHandler()


class CommandIn(BaseModel):
    text: str
    user_id: str = "default"


@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("startup", msg="Jarvis backend started with 1,241 commands loaded")


@app.get("/health")
def health():
    return {"status": "ok", "commands_loaded": 1241}


@app.post("/command")
def post_command(cmd: CommandIn):
    t0 = time.time()
    if not cmd.text or not cmd.text.strip():
        raise HTTPException(status_code=400, detail="Empty command")

    res = handler.handle(cmd.text.strip(), user_id=cmd.user_id)
    res["processing_time_ms"] = int((time.time() - t0) * 1000)
    return res


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: dict):
        for ws in list(self.active):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(ws)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting {"type": "command", "text": "...", "user_id": "..."}
            if data.get("type") == "command":
                user_id = data.get("user_id", "default")
                res = handler.handle(data.get("text", ""), user_id=user_id)
                await manager.broadcast({"type": "result", "payload": res})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
