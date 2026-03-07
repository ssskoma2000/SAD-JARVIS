import json
import time
from pathlib import Path
from typing import Optional, Tuple

from passlib.context import CryptContext
import jwt

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    def __init__(self, base_dir: Path, jwt_secret: str = "changeme", jwt_exp_seconds: int = 3600):
        self.base_dir = Path(base_dir)
        self.admin_file = self.base_dir / ".admin.json"
        self.jwt_secret = jwt_secret
        self.jwt_exp = jwt_exp_seconds
        self._mem_state = {"admin_enabled": False}
        self._load_state()

    def _load_state(self):
        if self.admin_file.exists():
            try:
                data = json.loads(self.admin_file.read_text(encoding="utf-8"))
                self._mem_state.update({
                    "admin_enabled": bool(data.get("hash")),
                })
            except Exception:
                self._mem_state["admin_enabled"] = False
        else:
            self._mem_state["admin_enabled"] = False

    def first_run(self) -> bool:
        return not self.admin_file.exists()

    def register_admin(self, password: str) -> bool:
        if not self.first_run():
            return False
        pw_hash = PWD_CONTEXT.hash(password)
        payload = {"hash": pw_hash, "created": int(time.time())}
        self.admin_file.write_text(json.dumps(payload), encoding="utf-8")
        self._mem_state["admin_enabled"] = True
        return True

    def verify_admin(self, password: str) -> bool:
        if not self.admin_file.exists():
            return False
        try:
            data = json.loads(self.admin_file.read_text(encoding="utf-8"))
            return PWD_CONTEXT.verify(password, data.get("hash", ""))
        except Exception:
            return False

    def mint_jwt(self) -> str:
        now = int(time.time())
        token = jwt.encode({"sub": "admin", "iat": now, "exp": now + self.jwt_exp}, self.jwt_secret, algorithm="HS256")
        return token

    def verify_jwt(self, token: str) -> bool:
        try:
            dec = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return dec.get("sub") == "admin"
        except Exception:
            return False

    def admin_enabled(self) -> bool:
        return self._mem_state.get("admin_enabled", False)
