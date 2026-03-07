import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    SQLite ma'lumotlar bazasi bilan ishlash uchun menejer.
    Suhbatlar tarixini saqlaydi.
    """
    def __init__(self, db_name="jarvis_memory.db"):
        self.db_name = db_name
        self.conn = None
        try:
            # Bazaga ulanish (agar mavjud bo'lmasa, yaratiladi)
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.create_table()
        except sqlite3.Error as e:
            print(f"Ma'lumotlar bazasi bilan bog'lanishda xatolik: {e}")

    def create_table(self):
        """
        'conversations' jadvalini yaratadi (agar mavjud bo'lmasa).
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME NOT NULL
                );
            """)
            self.conn.commit()
            print(f"'{self.db_name}' bazasidagi 'conversations' jadvali tayyor.")
        except sqlite3.Error as e:
            print(f"Jadval yaratishda xatolik: {e}")

    def add_message(self, sender: str, message: str):
        """
        Bazaga yangi xabarni qo'shadi.
        
        Args:
            sender (str): Xabar yuboruvchi ('user' yoki 'jarvis').
            message (str): Xabar matni.
        """
        if not self.conn:
            print("Ma'lumotlar bazasiga ulanish mavjud emas.")
            return

        try:
            cursor = self.conn.cursor()
            timestamp = datetime.now()
            cursor.execute(
                "INSERT INTO conversations (sender, message, timestamp) VALUES (?, ?, ?)",
                (sender, message, timestamp)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Xabar qo'shishda xatolik: {e}")

    def get_last_n_messages(self, n: int = 10):
        """
        Oxirgi N ta xabarni qaytaradi.
        """
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT sender, message, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?",
                (n,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Xabarlarni olishda xatolik: {e}")
            return []

    def __del__(self):
        """
        Obyekt yo'q qilinganda baza ulanishini yopadi.
        """
        if self.conn:
            self.conn.close()

# Test uchun
if __name__ == "__main__":
    db_manager = DatabaseManager()
    print("\nTest uchun xabarlar qo'shilmoqda...")
    db_manager.add_message("user", "Salom Jarvis!")
    db_manager.add_message("jarvis", "Salom! Qanday yordam bera olaman?")
    
    print("\nOxirgi 5 ta xabar:")
    messages = db_manager.get_last_n_messages(5)
    for msg in reversed(messages): # Eskidan yangiga qarab chiqarish
        print(f"[{msg[2]}] {msg[0]}: {msg[1]}")
