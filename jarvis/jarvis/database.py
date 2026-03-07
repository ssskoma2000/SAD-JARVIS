import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "jarvis.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(str(DB_PATH), detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS command_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT,
        stage TEXT,
        intent TEXT,
        success INTEGER,
        blocked INTEGER DEFAULT 0,
        timestamp REAL,
        execution_time_ms INTEGER,
        meta TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS preferences (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    conn.commit()
    conn.close()

def log_command(input_text, stage, intent, success, execution_time_ms, blocked=0, meta=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO command_logs (input, stage, intent, success, blocked, timestamp, execution_time_ms, meta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (input_text, stage, intent, int(bool(success)), int(bool(blocked)), time.time(), execution_time_ms, meta))
    conn.commit()
    conn.close()
