import subprocess
from datetime import datetime
import re
from ai_services import AIService
import platform_utils
import os

class CommandHandler:
    """
    Foydalanuvchi buyruqlarini tahlil qiladi.
    """
    def __init__(self):
        self.ai_service = AIService()
        self._load_readme_commands()
        # 1-bosqich: Lokal buyruqlar (regex va funksiyalar)
        self.local_commands = [
            (re.compile(r"soat necha|vaqt nechi bo'ldi"), self.get_time),
            (re.compile(r"o'zingni tanishtir"), self.introduce_self),
            (re.compile(r"salom"), self.greet),
            # Lambda funksiyalar asinxron bo'lmagani uchun `await` talab qilmaydi
            (re.compile(r"chrome|brauzer"), lambda: self.open_path_or_app(target="Chrome")),
            (re.compile(r"telegram"), lambda: self.open_path_or_app(target="Telegram")),
        ]
        # 2-bosqich: AI uchun mavjud "asboblar" (tools)
        self.ai_tools = [
            {
                "type": "function",
                "function": {
                    "name": "open_path_or_app",
                    "description": "Kompyuterdagi dasturni, faylni yoki veb-saytni ochadi.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "description": "Ochilishi kerak bo'lgan narsaning nomi, masalan, 'Chrome', 'youtube.com', 'hisobot.docx fayli'."
                            }
                        },
                        "required": ["target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_code",
                    "description": "Berilgan talablar asosida turli dasturlash tillarida kod generatsiya qiladi.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {
                                "type": "string",
                                "description": "Kod yozilishi kerak bo'lgan dasturlash tili (masalan, 'Python', 'JavaScript', 'HTML')."
                            },
                            "task_description": {
                                "type": "string",
                                "description": "Kod nima qilishi kerakligi haqida batafsil tavsif."
                            }
                        },
                        "required": ["language", "task_description"],
                    },
                },
            },
        ]
        # AI "asbob" nomlarini funksiyalarga bog'lash
        self.tool_executors = {
            "open_path_or_app": self.open_path_or_app,
            "generate_code": self.generate_code_tool,
        }

    def _load_readme_commands(self):
        self.readme_commands = {}
        # Assuming the script runs from the 'backend' directory.
        # If not, this path needs to be adjusted.
        file_path = os.path.join(os.path.dirname(__file__), "buyruqlar", "readme.txt")
        
        intent = "unknown"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Heuristic to detect intent headers
                    if (re.match(r"^\d+[\.\u20e3\ufe0f]?\s", line) or 
                        line.startswith("🔹") or 
                        re.match(r"^[A-ZА-Я][a-zA-Zа-яА-Я\s'’`-]+:$", line) or
                        (not re.search(r"[:=]", line) and " " not in line.strip()) and line.isupper()):
                        
                        raw_intent = re.sub(r"^\d+[\.\u20e3\ufe0f]?\s*|^\s*🔹\s*|:$", "", line).strip()
                        if len(raw_intent) > 2: # Filter out short/irrelevant headers
                            intent = raw_intent
                        continue

                    # Format: "Versiya 1: Command"
                    match = re.match(r"Versiya\s+\d+:\s*(.+)", line, re.IGNORECASE)
                    if match:
                        command = match.group(1).strip().lower()
                        if command:
                            self.readme_commands[command] = intent
                        continue

                    # Format: "Command = Command = Command"
                    if "=" in line:
                        commands = [c.strip().lower() for c in line.split("=")]
                        for command in commands:
                            if command:
                                self.readme_commands[command] = intent
                        continue

                    # Simple line-by-line commands
                    command = line.lower()
                    
                    # Remove quotes and potential arguments for cleaner matching
                    command_clean = re.sub(r'["“].*["”]', '', command).strip()

                    if command_clean:
                        self.readme_commands[command_clean] = intent

        except FileNotFoundError:
            print(f"Warning: Command file not found at {file_path}")
        except Exception as e:
            print(f"Error loading readme commands: {e}")

        print(f"Loaded {len(self.readme_commands)} commands from readme.txt")

    async def handle(self, text: str) -> str:
        """
        Buyruqni ikki bosqichda tahlil qiladi va natijani qaytaradi.
        """
        lower_text = text.lower().strip()

        # 1-bosqich: Lokal buyruqlarni tekshirish
        for pattern, func in self.local_commands:
            if pattern.search(lower_text):
                print(f"Lokal buyruq topildi: {pattern.pattern}")
                import asyncio
                if asyncio.iscoroutinefunction(func):
                    return await func()
                return func()

        # 2-bosqich: Readme.txt dan yuklangan buyruqlarni tekshirish
        # To'liq moslikni tekshirish
        if lower_text in self.readme_commands:
            intent = self.readme_commands[lower_text]
            return await self._execute_readme_command(intent, lower_text)

        # Argumentli buyruqlarni tekshirish
        for command_base, intent in self.readme_commands.items():
            if command_base and lower_text.startswith(command_base + ' '):
                argument = lower_text[len(command_base):].strip()
                return await self._execute_readme_command(intent, lower_text, argument=argument)
        
        # 3-bosqich: AI yordamida niyatni aniqlash
        print("Lokal yoki readme buyrug'i topilmadi, AI'ga yuborilmoqda...")
        intent_data = await self.ai_service.get_intent_from_ai(text, self.ai_tools)
        
        if intent_data and intent_data.get("intent") != "unknown":
            intent = intent_data["intent"]
            entities = intent_data["entities"]
            print(f"AI niyatni aniqladi: {intent}, argumentlar: {entities}")
            
            if intent in self.tool_executors:
                executor = self.tool_executors[intent]
                import asyncio
                if asyncio.iscoroutinefunction(executor):
                    return await executor(**entities)
                return executor(**entities)
            else:
                return f"'{intent}' nomli buyruqni bajara olmayman."

        print("AI niyatni aniqlay olmadi, oddiy chat rejimiga o'tilmoqda...")
        return await self.ai_service.get_chat_response(text)

    async def _execute_readme_command(self, intent: str, command: str, argument: str = None) -> str:
        """
        readme.txt dan topilgan buyruqlar uchun amaliyotlarni bajaradi.
        """
        print(f"Readme buyrug'i bajarilmoqda. Niyat: '{intent}', Buyruq: '{command}', Argument: '{argument}'")
        
        intent_lower = intent.lower()

        # Har ehtimolga qarshi, ba'zi buyruqlar bu yerda ham takrorlanishi mumkin
        if any(kw in intent_lower for kw in ["soat", "vaqt"]):
            return await self.get_time()
        
        if any(kw in intent_lower for kw in ["kalkulyator", "hisoblash", "hisobla"]):
            return self.open_path_or_app(target="calculator")

        if any(kw in intent_lower for kw in ["internetdan qidir", "google-da izla", "ma'lumot top"]):
            query = argument if argument else command
            # Attempt to clean the query from the command itself
            if not argument:
                parts = command.split()
                if len(parts) > 1:
                    query = " ".join(parts[1:])
            
            return self.open_path_or_app(target=query)
            
        if any(kw in intent_lower for kw in ["saytga kir", "veb-sahifani och", "brauzerni ishga tushir"]):
              target_site = argument if argument else "google.com"
             return self.open_path_or_app(target=target_site)

        if "tizimni yopish" in intent_lower or "kompyuterni o'chir" in intent_lower:
            # Xavfsizlik uchun bu funksiyani to'g'ridan-to'g'ri ishga tushurmaymiz
            return "Kompyuterni o'chirish buyrug'i qabul qilindi, lekin xavfsizlik sababli bu funksiya o'chirilgan."
            # platform_utils.shutdown()
            # return "Kompyuter o'chirilmoqda..."

        if "qayta yuklash" in intent_lower or "restart qil" in intent_lower:
            # Xavfsizlik uchun bu funksiyani to'g'ridan-to'g'ri ishga tushurmaymiz
            return "Kompyuterni qayta yuklash buyrug'i qabul qilindi, lekin xavfsizlik sababli bu funksiya o'chirilgan."
            # platform_utils.restart()
            # return "Kompyuter qayta yuklanmoqda..."

        # Boshqa barcha buyruqlar uchun placeholder
        return f'"{intent}" niyati bo\'yicha buyruq qabul qilindi, lekin amaliyot hali qo\'shilmagan.'

    # --- Lokal buyruq funksiyalari ---
    async def get_time(self) -> str:
        now = datetime.now()
        return f"Hozir soat {now.strftime('%H:%M')}."

    async def introduce_self(self) -> str:
        return "Men Jarvis, sizning shaxsiy intellektual yordamchingizman. Koma tomonidan yaratilganman."

    async def greet(self) -> str:
        return "Assalomu alaykum! Qanday yordam bera olaman?"

    # --- AI "asbob" funksiyalari ---
    def open_path_or_app(self, target: str) -> str:
        """
        AI yoki readme tomonidan aniqlangan `target`ni ochadi.
        """
        target_lower = target.lower()
        path_to_open = ""
        
        # Oddiy qoidalar
        if target_lower == "calculator":
             try:
                # Windows uchun maxsus sxema
                platform_utils.open_path("calculator:")
                return "Kalkulyator ochilmoqda..."
             except Exception:
                # Linux/MacOS uchun harakat
                try:
                    # Umumiy nomlar
                    calculators = ["gnome-calculator", "kcalc", "calculator"]
                    for calc in calculators:
                        if subprocess.call(['which', calc], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
                            subprocess.Popen([calc])
                            return "Kalkulyator ochilmoqda..."
                    return "Kalkulyator topilmadi."
                except Exception as e:
                    return f"Kalkulyatorni ochishda xatolik: {e}"
        elif "chrome" in target_lower or "brauzer" in target_lower:
            path_to_open = "https://google.com"
        elif "telegram" in target_lower:
            path_to_open = "tg://resolve"
        elif "youtube" in target_lower:
            path_to_open = "https://youtube.com"
        elif "fayl" in target_lower:
            path_to_open = "." # Joriy papkani ochish
        # Agar yuqoridagilar mos kelmasa, URL yoki qidiruv so'rovi deb hisoblaymiz
        elif '.' in target_lower and ' ' not in target_lower:
             path_to_open = f"http://{target_lower}" if not target_lower.startswith("http") else target_lower
        else:
            path_to_open = f"https://google.com/search?q={target}"

        try:
            platform_utils.open_path(path_to_open)
            return f'Bajarildi, "{target}" ochilmoqda...'
        except Exception as e:
            return f'"{target}"ni ochishda xatolik yuz berdi: {e}'

    async def generate_code_tool(self, language: str, task_description: str) -> str:
        """
        AI yordamida kod generatsiya qiladi.
        """
        system_prompt = f"You are an expert programmer specializing in {language}. Provide only the raw code for the following request, without any explanations or markdown formatting."
        generated_code = await self.ai_service.get_chat_response(task_description, system_prompt=system_prompt)
        # Frontend markdownni to'g'ri ko'rsatishi uchun formatlaymiz
        return f"Mana {language} tilida so'ralgan kod:\n```{
language.lower()}
{generated_code}
```"