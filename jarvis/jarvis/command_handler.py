import re
import json
import time
from pathlib import Path
from rapidfuzz import fuzz, process
from .ai_services import ai_fallback_response
from .action_dispatcher import dispatch
from .security import validate_and_sanitize, create_safe_ai_prompt, log_blocked_command
from .database import init_db

BASE_DIR = Path(__file__).resolve().parents[1]
COMMANDS_PATH = BASE_DIR / "commands.json"

class CommandHandler:
    def __init__(self, commands_path=COMMANDS_PATH):
        init_db()
        self.commands_path = commands_path
        self.commands = self._load_commands()

    def _load_commands(self):
        if not self.commands_path.exists():
            return {}
        with open(self.commands_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Stage 1: simple regex
    def stage_regex(self, text: str):
        t = text.lower().strip()
        # basic matches for time/date
        if re.search(r"\b(time|what time|soat)\b", t):
            return {"stage": "regex", "intent": "show_time", "action": "show_time", "args": {}}
        if re.search(r"\b(date|today|sana|bugun)\b", t):
            return {"stage": "regex", "intent": "show_date", "action": "show_time", "args": {}}
        return None

    # Stage 2: dictionary / exact / pattern / fuzzy
    def stage_dictionary(self, text: str, fuzzy_threshold: int = 80):
        # exact or pattern match
        keys = list(self.commands.keys())
        # exact equality
        if text in self.commands:
            meta = self.commands[text]
            args = self._extract_args_from_pattern(text, text)
            return {"stage": "dictionary", "intent": meta.get("intent"), "action": meta.get("action"), "args": args}

        # pattern matching: find pattern keys with placeholders like {query}
        for pattern, meta in self.commands.items():
            if "{" in pattern and "}" in pattern:
                # convert to regex
                regex = re.escape(pattern)
                regex = regex.replace(re.escape("{query}"), "(?P<query>.+)")
                m = re.match(regex + "$", text)
                if m:
                    args = {k: v.strip() for k, v in m.groupdict().items()}
                    return {"stage": "dictionary", "intent": meta.get("intent"), "action": meta.get("action"), "args": args}

        # fuzzy search
        best = process.extractOne(text, keys, scorer=fuzz.token_sort_ratio)
        if best and best[1] >= fuzzy_threshold:
            pattern = best[0]
            meta = self.commands[pattern]
            # attempt to extract trailing part as single argument if pattern contains {query}
            if "{query}" in pattern:
                # get everything after the fixed prefix
                prefix = pattern.split("{query}")[0].strip()
                if text.startswith(prefix):
                    arg = text[len(prefix):].strip()
                    args = {"query": arg}
                else:
                    args = {"query": ""}
            else:
                args = {}
            return {"stage": "dictionary", "intent": meta.get("intent"), "action": meta.get("action"), "args": args}

        return None

    def _extract_args_from_pattern(self, pattern, text):
        if "{query}" in pattern:
            prefix = pattern.split("{query}")[0].strip()
            arg = text[len(prefix):].strip()
            return {"query": arg}
        return {}

    def handle(self, text: str, user_id: str = "default"):
        t0 = time.time()
        
        # Security Layer: Input validation & rate limiting
        validation = validate_and_sanitize(text, user_id)
        if not validation["is_safe"]:
            log_blocked_command(text, validation["reason"], user_id)
            return {
                "stage": "security",
                "intent": "blocked",
                "action": "blocked",
                "error": validation["reason"],
                "blocked": True,
                "execution_time_ms": int((time.time() - t0) * 1000)
            }
        
        text = validation["sanitized"]
        
        # Stage 1: Regex
        res = self.stage_regex(text)
        if res:
            res["execution_time_ms"] = int((time.time() - t0) * 1000)
            # dispatch
            out = dispatch(res["action"], res.get("args", {}), text, res["stage"])
            res["dispatch_result"] = out
            return res

        # Stage 2: Dictionary
        res = self.stage_dictionary(text)
        if res:
            res["execution_time_ms"] = int((time.time() - t0) * 1000)
            out = dispatch(res["action"], res.get("args", {}), text, res["stage"])
            res["dispatch_result"] = out
            return res

        # Stage 3: AI fallback (with safety prompt shield)
        safe_prompt = create_safe_ai_prompt(text)
        ai_text = ai_fallback_response(safe_prompt)
        res = {"stage": "ai", "intent": "ai_fallback", "action": "ai_suggested", "args": {"response": ai_text}, "execution_time_ms": int((time.time() - t0) * 1000)}
        return res
