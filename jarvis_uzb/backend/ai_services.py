"""
🧠 OpenAI AI INTEGRATION - JARVIS BRAIN
=======================================
This module provides real OpenAI API integration with:
- GPT-4o-mini for command understanding
- Tool calling for action execution
- System prompt for Uzbek language
- Request caching and rate limiting
"""

import openai
from openai import OpenAI
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import json
import time
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

class AIService:
    """
    OpenAI-powered AI service for Jarvis.
    Handles command parsing, response generation, and action execution.
    """
    
    def __init__(self):
        """Initialize OpenAI client and configuration."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Dummy mode for testing without API
        self.dummy_mode = os.getenv("DUMMY_MODE", "false").lower() == "true"
        
        if not self.dummy_mode and not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env file")
        
        if not self.dummy_mode:
            self.client = OpenAI(api_key=self.api_key)
        
        self.model = "gpt-4o-mini"  # Lightweight but powerful
        
        # Dummy responses for testing without API
        self.dummy_responses = {
            "salom": {
                "intent": "greeting",
                "action": "ai_response", 
                "parameters": {},
                "response": "Assalom alaikum! Men Jarvisman, sizga qanday yordam bera olaman?",
                "confidence": 0.95
            },
            "youtube": {
                "intent": "open_youtube",
                "action": "open_url",
                "parameters": {"query": "https://youtube.com"},
                "response": "YouTube ochyapman!",
                "confidence": 0.98
            },
            "google": {
                "intent": "search_google", 
                "action": "open_url",
                "parameters": {"query": "https://google.com"},
                "response": "Google ochyapman!",
                "confidence": 0.97
            },
            "musiqa": {
                "intent": "play_music",
                "action": "play_music", 
                "parameters": {"query": "music"},
                "response": "Musiqa qo'yaman!",
                "confidence": 0.96
            },
            "default": {
                "intent": "unknown_command",
                "action": "ai_response",
                "parameters": {},
                "response": "Kechirasiz, bu buyruqni tushunmadim. Yordam kerakmi?",
                "confidence": 0.70
            }
        }
        
        # System prompt for Jarvis identity
        self.system_prompt = """Sen tizimni boshqaruvchi va foydalanuvchiga yordam beruvchi "Jarvis" nomli O'zbek tilidagi aqlli virtual yordamchisan. Sen oddiy chatbot emassan. Sening vazifang foydalanuvchining har qanday matnli yoki ovozli buyrug'ini tushunish, analiz qilish va tizim tushunadigan aniq JSON formatiga o'tkazib berishdir.

SENING QOIDALARING:

Foydalanuvchi shevada, xato yozuvda yoki rus/ingliz so'zlari aralash gapirsa ham uning asl niyatini tushunishing shart.

Har doim javobing qisqa, aniq va ortiqcha xushmuomalaliklarsiz, "Jarvis" uslubida (professional va sovuqqon) bo'lishi kerak.

HECH QACHON oddiy matn qaytarma. Sening javobing FAqat va FAqat quyidagi JSON strukturasida bo'lishi shart:

{
"intent": "foydalanuvchining asl niyati (masalan: open_app, play_music, search, system_control, chat)",
"action": "tizim bajarishi kerak bo'lgan aniq funksiya (masalan: open_url, run_exe, set_volume, none)",
"parameters": {
"query": "qidiruv so'zi, url yoki dastur nomi (agar kerak bo'lsa)"
},
"response": "Foydalanuvchiga ovozli tarzda o'qib berilishi kerak bo'lgan qisqa, o'zbekcha javobing"
}

TAQIQLANGAN BUYRUQLAR (Security):
Agar foydalanuvchi tizimni o'chirish (shutdown), format qilish, o'chirish (delete) yoki hack qilish kabi xavfli buyruqlarni bersa, "action" ni "none" ga o'zgartir va "response" ga "Kechirasiz bo'ss, bu xavfli buyruq bo'lgani uchun uni bajara olmayman" deb yoz."""
        
        # Request cache (simple in-memory, for production use Redis)
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
        
        print("✅ OpenAI AIService ishga tushdi (model: " + self.model + ")")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for request."""
        return f"ai_response_{text.lower()}"
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached result is still valid."""
        if key not in self._cache:
            return False
        timestamp, _ = self._cache[key]
        return (time.time() - timestamp) < self._cache_ttl
    
    async def get_intent_from_ai(
        self, 
        text: str, 
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        🧠 Main AI method: Parse user input and determine intent + action.
        
        Args:
            text: User input (Uzbek or any language)
            use_cache: Use cached response if available
            
        Returns:
            {
                "intent": "open_youtube",
                "action": "open_url",
                "parameters": {"query": "music"},
                "response": "...",
                "confidence": 0.95
            }
        """
        
        # Check cache
        cache_key = self._get_cache_key(text)
        if use_cache and self._is_cache_valid(cache_key):
            timestamp, cached_result = self._cache[cache_key]
            cached_result["source"] = "cache"
            return cached_result
        
        # Dummy mode for testing without API
        if self.dummy_mode:
            print("🤖 DUMMY MODE: Using predefined responses")
            
            # Simple keyword matching for dummy responses
            text_lower = text.lower()
            
            if "salom" in text_lower or "hello" in text_lower:
                response = self.dummy_responses["salom"].copy()
            elif "youtube" in text_lower:
                response = self.dummy_responses["youtube"].copy()
            elif "google" in text_lower:
                response = self.dummy_responses["google"].copy()
            elif "musiqa" in text_lower or "music" in text_lower:
                response = self.dummy_responses["musiqa"].copy()
            else:
                response = self.dummy_responses["default"].copy()
            
            response["source"] = "dummy"
            response["timestamp"] = datetime.now().isoformat()
            
            # Cache the response
            self._cache[cache_key] = (time.time(), response)
            
            return response
        
        try:
            # 🔥 Real OpenAI API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,  # Deterministic (not creative)
                max_tokens=500
            )
            
            # Parse response - AI must return JSON
            message = response.choices[0].message
            content = message.content.strip()
            
            try:
                # Parse JSON response from AI
                action_data = json.loads(content)
                
                # Validate required fields
                if not all(key in action_data for key in ["intent", "action", "parameters", "response"]):
                    raise ValueError("Missing required JSON fields")
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ AI JSON parse error: {e}")
                print(f"Raw response: {content}")
                
                # Fallback response
                action_data = {
                    "intent": "parse_error",
                    "action": "none",
                    "parameters": {},
                    "response": "Kechirasiz, sizning buyrug'ingizni tushunmadim. Qayta ayting.",
                    "confidence": 0.0
                }
            
            # Add metadata
            action_data["source"] = "openai"
            action_data["timestamp"] = datetime.now().isoformat()
            
            # Cache result
            self._cache[cache_key] = (time.time(), action_data)
            
            print(f"✅ AI Response: {action_data.get('intent')} (confidence: {action_data.get('confidence', 'N/A')})")
            
            return action_data
            
        except openai.APIError as e:
            print(f"❌ OpenAI API Error: {e}")
            return {
                "intent": "error",
                "action": "error",
                "response": "AI xizmati vaqtincha ishlamayapti, qayta urinib ko'ring",
                "error": str(e),
                "confidence": 0
            }
    
    async def get_chat_response(
        self, 
        text: str, 
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        💬 Get conversational AI response (not command execution).
        
        Args:
            text: User message
            system_prompt: Custom system prompt
            conversation_history: Previous messages for context
            
        Returns:
            Response text in Uzbek
        """
        
        try:
            messages = conversation_history or []
            
            # Add user message
            messages.append({"role": "user", "content": text})
            
            # System prompt
            system = system_prompt or self.system_prompt
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}] + messages,
                temperature=0.7,  # More creative for chat
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Chat Error: {e}")
            return "Kechirasiz, javob berish imkoni yo'q"
    
    async def text_to_speech(
        self, 
        text: str,
        voice: str = "nova",
        format: str = "mp3"
    ) -> Optional[bytes]:
        """
        🔊 Convert text to speech using OpenAI TTS.
        
        Args:
            text: Text to convert
            voice: Voice variant (nova, onyx, alloy, echo, fable, shimmer)
            format: Audio format (mp3, opus, aac, flac)
            
        Returns:
            Audio bytes (MP3)
        """
        
        # Dummy mode - skip TTS
        if self.dummy_mode:
            print(f"🔊 DUMMY MODE: Skipping TTS for '{text}'")
            return None
        
        try:
            if not text or len(text.strip()) == 0:
                return None
            
            response = self.client.audio.speech.create(
                model="tts-1",  # Fastest
                voice=voice,
                input=text
            )
            
            return response.content
            
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return None
    
    async def speech_to_text(
        self,
        audio_bytes: bytes,
        language: str = "uz"
    ) -> Optional[str]:
        """
        🎙 Convert speech to text using Whisper.
        
        Args:
            audio_bytes: WAV/MP3 audio data
            language: Language code (uz, en, ru)
            
        Returns:
            Recognized text
        """
        
        try:
            # Save audio to temporary file (Whisper API requires file)
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            # Call Whisper
            with open(tmp_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            # Cleanup
            os.unlink(tmp_path)
            
            return transcript.text
            
        except Exception as e:
            print(f"❌ STT Error: {e}")
            return None
    
    def clear_cache(self):
        """Clear request cache."""
        self._cache.clear()
        print("✅ Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_requests": len(self._cache),
            "cache_ttl_seconds": self._cache_ttl
        }


# Async wrapper for compatibility
async def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    return AIService()


if __name__ == "__main__":
    # Test
    import asyncio
    
    async def test():
        ai = AIService()
        
        # Test 1: Command parsing
        print("\n📝 Test 1: Command Parsing")
        result = await ai.get_intent_from_ai("youtube och relaxing music")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Test 2: Blocked command
        print("\n🚫 Test 2: Blocked Command")
        result = await ai.get_intent_from_ai("kompyuterni o'chir")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Test 3: Chat response
        print("\n💬 Test 3: Chat Response")
        response = await ai.get_chat_response("Salom, bugun qala qil?")
        print(f"Response: {response}")
        
        # Test 4: TTS
        print("\n🔊 Test 4: Text-to-Speech")
        audio = await ai.text_to_speech("Assalom alaikum, men Jarvis!")
        print(f"Audio generated: {len(audio) if audio else 0} bytes")
    
    asyncio.run(test())
