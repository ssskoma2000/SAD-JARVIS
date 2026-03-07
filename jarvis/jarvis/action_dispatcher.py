import webbrowser
import subprocess
import shlex
from typing import Dict, Any
from .database import log_command
import time

# Whitelisted actions
ALLOWED_ACTIONS = {
    "open_app",
    "open_url",
    "set_volume",
    "screenshot",
    "search_google",
    "play_music",
    "show_time",
}

def _safe_open_url(url: str) -> Dict[str, Any]:
    webbrowser.open(url)
    return {"ok": True, "url": url}

def _show_time() -> Dict[str, Any]:
    import datetime
    now = datetime.datetime.now().isoformat()
    return {"ok": True, "time": now}

def dispatch(action: str, args: Dict[str, Any], input_text: str, stage: str) -> Dict[str, Any]:
    start = time.time()
    blocked = False
    result = {"ok": False}

    if action not in ALLOWED_ACTIONS:
        # Log as blocked
        execution_time_ms = int((time.time() - start) * 1000)
        log_command(input_text, stage, action, False, execution_time_ms, blocked=1, meta="action_not_allowed")
        return {"ok": False, "error": "action_blocked", "blocked": True}

    try:
        if action == "open_url":
            url = args.get("url") or args.get("query")
            result = _safe_open_url(url)
        elif action == "show_time":
            result = _show_time()
        elif action == "search_google":
            q = args.get("query", "")
            url = f"https://www.google.com/search?q={q}"
            result = _safe_open_url(url)
        else:
            # default stub: return that the action was acknowledged
            result = {"ok": True, "action": action, "args": args}

        execution_time_ms = int((time.time() - start) * 1000)
        log_command(input_text, stage, action, True, execution_time_ms, blocked=0, meta=str(result))
        return result
    except Exception as e:
        execution_time_ms = int((time.time() - start) * 1000)
        log_command(input_text, stage, action, False, execution_time_ms, blocked=0, meta=str(e))
        return {"ok": False, "error": str(e)}
