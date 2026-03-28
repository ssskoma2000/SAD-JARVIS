"""
🎯 ACTION DISPATCHER - COMMAND EXECUTION ENGINE
================================================
Translates AI intent into real system actions.
Handles:
- Safe action execution (whitelisting)
- Blocked command detection
- Error handling and logging
- Response generation
"""

import subprocess
import os
import platform
import json
from typing import Dict, Any, Optional
from datetime import datetime
import webbrowser
import asyncio
from enum import Enum

try:
    import pyperclip
except ImportError:
    pyperclip = None


class ActionType(Enum):
    """Allowed action types."""
    OPEN_APP = "open_app"
    OPEN_URL = "open_url"
    SEARCH_GOOGLE = "search_google"
    PLAY_MUSIC = "play_music"
    SHOW_TIME = "show_time"
    CREATE_REMINDER = "create_reminder"
    READ_NOTE = "read_note"
    SEND_MESSAGE = "send_message"
    FILE_OPERATIONS = "file_operations"
    TAKE_SCREENSHOT = "take_screenshot"
    AI_RESPONSE = "ai_response"
    SYSTEM_INFO = "system_info"
    BLOCKED = "blocked"


class ActionDispatcher:
    """
    Executes AI-determined actions on the system.
    """
    
    # Blocked dangerous commands
    BLOCKED_COMMANDS = {
        'shutdown', 'restart', 'restart_now', 'power_off',
        'format', 'delete_system', 'rm_rf', 'delete_all',
        'hack', 'virus', 'penetration',
        'lock_screen', 'logout',
        'decrypt_file', 'break_encryption'
    }
    
    # Safe application mappings
    APP_MAPPINGS = {
        'chrome': 'chrome',
        'firefox': 'firefox',
        'edge': 'msedge',
        'safari': 'safari',
        'telegram': 'telegram',
        'discord': 'discord',
        'zoom': 'zoom',
        'skype': 'skype',
        'spotify': 'spotify',
        'youtube': 'youtube',
        'gmail': 'gmail',
        'outlook': 'outlook',
        'whatsapp': 'whatsapp',
        'notepad': 'notepad',
        'calculator': 'calc',
        'file explorer': 'explorer',
        'settings': 'ms-settings:',
        'task manager': 'taskmgr',
        'command prompt': 'cmd',
        'powershell': 'powershell',
        'terminal': 'wt',  # Windows Terminal
    }
    
    def __init__(self, log_database=None):
        """
        Initialize action dispatcher.
        
        Args:
            log_database: Optional database manager for logging
        """
        self.log_database = log_database
        self.os_type = platform.system()  # 'Windows', 'Darwin', 'Linux'
        print(f"🎯 ActionDispatcher initialized (OS: {self.os_type})")
    
    async def dispatch(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute action based on AI intent.

        Args:
            action_data: AI JSON response in format:
            {
                "intent": "foydalanuvchining asl niyati",
                "action": "tizim bajarishi kerak bo'lgan aniq funksiya",
                "parameters": {"query": "qidiruv so'zi, url yoki dastur nomi"},
                "response": "Foydalanuvchiga ovozli tarzda o'qib berilishi kerak bo'lgan javob"
            }

        Returns:
            {
                "success": true/false,
                "error": "...",
                "result": "...",
                "execution_time_ms": 0
            }
        """

        import time
        start_time = time.time()

        try:
            # AI dan kelgan JSON ma'lumotlarni ajratib olamiz
            intent = action_data.get("intent", "unknown")
            action = action_data.get("action", "none")
            params = action_data.get("parameters", {})
            query = params.get("query", "")

            print(f"🎯 Action qabul qilindi: {action} | Query: {query}")

            if action == "open_url":
                print(f"🌐 Veb-sahifa ochilmoqda...")
                webbrowser.open(query if query.startswith("http") else f"https://www.google.com/search?q={query}")
                return {"success": True, "result": "browser_opened"}

            elif action == "play_music":
                print(f"🎵 Youtube'dan qidirilmoqda: {query}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                return {"success": True, "result": "music_playing"}

            elif action == "open_app":
                print(f"💻 Dastur ishga tushirilmoqda: {query}")
                try:
                    # Windows uchun os.startfile(query), Linux uchun:
                    subprocess.Popen([query], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return {"success": True, "result": "app_opened"}
                except Exception as e:
                    print(f"❌ Dasturni ochishda xatolik: {e}")
                    return {"success": False, "error": str(e)}

            elif action == "none":
                # Shunchaki suhbat yoki bloklangan buyruq
                return {"success": True, "result": "chat_only"}

            elif action == "ai_response":
                # AI javobi - hech narsa qilmasdan, faqat javob qaytaradi
                return {"success": True, "result": "ai_response"}
            
        except Exception as e:
            print(f"❌ Action dispatch error: {e}")
            return {
                "success": False,
                "error": str(e),
                "result": None,
                "execution_time_ms": int((time.time() - start_time) * 1000)
            }
            await self._log_action(
                intent, 
                action, 
                result['success'],
                result.get('error') or 'OK'
            )
            
            return result
        
        except Exception as e:
            print(f"❌ Dispatch error: {e}")
            return {
                "success": False,
                "error": str(e),
                "result": None,
                "execution_time_ms": int((time.time() - start_time) * 1000)
            }
    
    async def _handle_open_url(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Open URL in default browser.
        
        Args:
            params: {url: "...", query: "..."}
            data: Full action data
        """
        
        try:
            url = params.get("url")
            query = params.get("query")
            
            if not url:
                if query:
                    # Search URL
                    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                else:
                    return {
                        "success": False,
                        "error": "No URL provided",
                        "result": None
                    }
            
            # Open browser
            webbrowser.open(url)
            
            print(f"✅ Opened URL: {url}")
            return {
                "success": True,
                "error": None,
                "result": f"Opened {url}",
                "url": url
            }
        
        except Exception as e:
            print(f"❌ open_url error: {e}")
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_search_google(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Search Google for a query.
        """
        
        try:
            query = params.get("query", "")
            
            if not query:
                return {
                    "success": False,
                    "error": "No query provided",
                    "result": None
                }
            
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            
            print(f"✅ Google search: {query}")
            return {
                "success": True,
                "error": None,
                "result": f"Searched for '{query}'"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_open_app(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Open an application.
        
        Args:
            params: {app: "chrome", command: "..."}
        """
        
        try:
            app = params.get("app", "").lower()
            command = params.get("command")
            
            if not app and not command:
                return {
                    "success": False,
                    "error": "No app or command specified",
                    "result": None
                }
            
            # Map app name to command
            if app:
                cmd = self.APP_MAPPINGS.get(app, app)
            else:
                cmd = command
            
            # Execute based on OS
            if self.os_type == "Windows":
                os.startfile(cmd)
            elif self.os_type == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', cmd])
            else:  # Linux
                subprocess.Popen([cmd])
            
            print(f"✅ Opened app: {app or cmd}")
            return {
                "success": True,
                "error": None,
                "result": f"Opened {app or cmd}"
            }
        
        except Exception as e:
            print(f"❌ open_app error: {e}")
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_play_music(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Open music service and play query.
        """
        
        try:
            query = params.get("query", "")
            service = params.get("service", "spotify")
            
            if service.lower() == "spotify":
                url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
            elif service.lower() == "youtube":
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            else:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            
            webbrowser.open(url)
            
            print(f"✅ Playing: {query}")
            return {
                "success": True,
                "error": None,
                "result": f"Playing {query}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_show_time(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Show current time.
        """
        
        try:
            from datetime import datetime
            
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%A, %d %B %Y")
            
            response = f"{time_str} - {date_str}"
            
            print(f"✅ Time: {response}")
            return {
                "success": True,
                "error": None,
                "result": response,
                "timestamp": now.isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_create_reminder(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Create a reminder (not yet implemented).
        """
        
        return {
            "success": False,
            "error": "Reminders not yet implemented",
            "result": None
        }
    
    async def _handle_ai_response(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Return AI response (no action needed).
        """
        
        try:
            response = data.get("response", "")
            
            return {
                "success": True,
                "error": None,
                "result": response
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_system_info(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Get system information.
        """
        
        try:
            import psutil
            
            info = {
                "os": platform.platform(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
            
            return {
                "success": True,
                "error": None,
                "result": json.dumps(info, ensure_ascii=False, indent=2)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _handle_take_screenshot(self, params: Dict, data: Dict) -> Dict[str, Any]:
        """
        Take a screenshot.
        """
        
        try:
            import subprocess
            
            if self.os_type == "Windows":
                # Windows: Use built-in print screen
                subprocess.run(["PrntScn"], check=False)
                result = "Screenshot taken (saved to clipboard)"
            else:
                result = "Screenshot feature not available on this OS"
            
            return {
                "success": True,
                "error": None,
                "result": result
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    async def _log_action(
        self,
        intent: str,
        action: str,
        success: bool,
        error: str
    ):
        """
        Log action execution.
        
        Args:
            intent: Intent name
            action: Action type
            success: Whether action succeeded
            error: Error message (empty if successful)
        """
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "action": action,
            "success": success,
            "error": error
        }
        
        print(f"📝 Logged: {json.dumps(log_entry, ensure_ascii=False)}")
        
        # Save to database if available
        if self.log_database:
            await self.log_database.log_action(log_entry)


# Standalone test
if __name__ == "__main__":
    
    async def test():
        """Test action dispatcher."""
        
        dispatcher = ActionDispatcher()
        
        # Test 1: Open URL
        print("\n🌐 Test 1: Open URL")
        result = await dispatcher.dispatch({
            "intent": "open_youtube",
            "action": "open_url",
            "parameters": {"query": "python tutorial"},
            "response": "Opening YouTube..."
        })
        print(f"Result: {result['success']}")
        
        # Test 2: Search Google
        print("\n🔍 Test 2: Search Google")
        result = await dispatcher.dispatch({
            "intent": "search_google",
            "action": "search_google",
            "parameters": {"query": "how to learn python"},
            "response": "Searching Google..."
        })
        print(f"Result: {result['success']}")
        
        # Test 3: Show time
        print("\n⏰ Test 3: Show Time")
        result = await dispatcher.dispatch({
            "intent": "show_time",
            "action": "show_time",
            "parameters": {},
            "response": "Current time"
        })
        print(f"Result: {result}")
        
        # Test 4: Blocked command
        print("\n🚫 Test 4: Blocked Command")
        result = await dispatcher.dispatch({
            "intent": "shutdown",
            "action": "blocked",
            "parameters": {},
            "response": "This command is blocked"
        })
        print(f"Success: {result['success']}")
    
    asyncio.run(test())
