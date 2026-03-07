# Jarvis (Backend)

This folder contains the FastAPI backend for the Uzbek Jarvis assistant.

Quick start (development):

1. Create a virtual environment and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy your `.env` with `OPENAI_API_KEY` and any other secrets.

3. Run the server:

```bash
uvicorn jarvis.main:app --reload
```

Endpoints:
- `POST /command` - send a text command
- `GET /health` - health check
- WebSocket at `/ws` for real-time events

Notes:
- `commands.json` should contain the 1,207+ commands; a small sample is included.
- Action execution is whitelisted and sandboxed in `action_dispatcher.py`.
