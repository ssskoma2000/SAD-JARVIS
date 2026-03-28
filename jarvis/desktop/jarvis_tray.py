"""
🖥️ JARVIS TRAY APPLICATION
===========================
Windows system tray app with hotkey activation.
Runs as background service listening for Ctrl+Space.

To run:
    python jarvis_tray.py

To build EXE:
    pyinstaller --onefile --windowed --icon=jarvis.ico jarvis_tray.py
"""

import sys
import os
import asyncio
import threading
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Flag to disable GUI on systems without tkinter
USE_GUI = True
try:
    import tkinter as tk
    from tkinter import messagebox
    from PIL import Image, ImageDraw
    import pystray
except ImportError:
    USE_GUI = False
    print("⚠️ tkinter/pillow not available, running in CLI mode")

from ai_services import AIService
from action_dispatcher import ActionDispatcher
from voice_manager import VoiceManager


class JarvisDesktopApp:
    """
    Main Jarvis desktop application.
    Manages tray icon, hotkey listening, and voice processing.
    """
    
    def __init__(self):
        """Initialize Jarvis desktop app."""
        
        self.ai_service = None
        self.action_dispatcher = None
        self.voice_manager = None
        self.hotkey_manager = None
        self.tray_icon = None
        
        self.is_running = False
        self.is_listening = False
        self.event_loop = None
        
        print("=" * 60)
        print("🤖 JARVIS DESKTOP ASSISTANT")
        print("=" * 60)
        print(f"⏰ Started: {datetime.now()}")
        print("\n🔧 Initializing components...")
    
    def initialize(self) -> bool:
        """
        Initialize all components.
        
        Returns:
            True if initialization successful
        """
        
        try:
            # Initialize AI service
            print("\n📡 Loading AI service...")
            self.ai_service = AIService()
            
            # Initialize action dispatcher
            print("🎯 Loading action dispatcher...")
            self.action_dispatcher = ActionDispatcher()
            
            # Initialize voice manager
            print("🎙️  Loading voice manager...")
            self.voice_manager = VoiceManager()
            
            # Test microphone
            print("\n🧪 Testing microphone...")
            if self.voice_manager.test_microphone():
                print("✅ Microphone OK")
            else:
                print("⚠️  Microphone test failed (may still work)")
            
            # Create event loop for async operations
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            
            print("\n✅ All components initialized successfully!")
            return True
        
        except Exception as e:
            print(f"\n❌ Initialization error: {e}")
            return False
    
    async def _on_hotkey_activated(self):
        """
        Called when Ctrl+Space is pressed.
        Starts voice listening and processing.
        """
        
        if self.is_listening:
            print("⚠️  Already listening...")
            return
        
        self.is_listening = True
        
        try:
            print("\n" + "=" * 60)
            print("🎤 LISTENING... (speak now)")
            print("=" * 60)
            
            # Record audio
            audio_bytes = await self.voice_manager.listen(timeout=10, min_duration=0.5)
            
            if not audio_bytes:
                print("❌ No audio recorded")
                return
            
            print(f"\n🎙️  Converting speech to text...")
            
            # Convert speech to text using Whisper
            text = await self.ai_service.speech_to_text(audio_bytes)
            
            if not text:
                print("❌ Could not understand speech")
                return
            
            print(f"📝 Recognized: \"{text}\"")
            
            # Get AI intent
            print(f"\n🧠 Analyzing intent...")
            action_data = await self.ai_service.get_intent_from_ai(text)
            
            print(f"💡 Intent: {action_data.get('intent')}")
            print(f"🎯 Action: {action_data.get('action')}")
            
            # Execute action
            print(f"\n⚙️  Executing action...")
            result = await self.action_dispatcher.dispatch(action_data)
            
            if result['success']:
                print(f"✅ Success: {result.get('result', 'OK')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            # Generate response text
            response_text = action_data.get('response', 'Bajarildi')
            
            # Convert to speech
            print(f"\n🔊 Generating voice response...")
            audio_response = await self.ai_service.text_to_speech(response_text)
            
            if audio_response:
                print(f"🎵 Playing response...")
                await self.voice_manager.play_audio(audio_response)
            
            print("\n✅ Complete!")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.is_listening = False
    

    def _setup_hotkey_manager(self) -> bool:
        """
        Setup hotkey manager.
        
        Returns:
            True if successful
        """
        
        try:
            print("\n⌨️  Setting up hotkey listener...")
            
            self.hotkey_manager = create_jarvis_hotkey_manager(
                on_activate=self._on_hotkey_wrapper
            )
            
            if self.hotkey_manager:
                print("✅ Hotkey manager ready (Ctrl+Space to activate)")
                return True
            else:
                print("❌ Failed to create hotkey manager")
                return False
        
        except Exception as e:
            print(f"❌ Hotkey setup error: {e}")
            return False
    
    def _create_tray_icon(self):
        """
        Create system tray icon.
        Only works on Windows with pystray.
        """
        
        if not USE_GUI:
            print("⚠️  GUI not available, skipping tray icon")
            return False
        
        try:
            import pystray
            from PIL import Image, ImageDraw
            
            # Create simple icon image
            image = Image.new('RGB', (64, 64), color=(73, 109, 137))
            draw = ImageDraw.Draw(image)
            
            # Draw "J" for Jarvis
            draw.text((22, 20), "J", fill=(255, 255, 255))
            
            # Create menu
            menu = pystray.Menu(
                pystray.MenuItem("🎤 Listen (Ctrl+Space)", self._on_tray_listen),
                pystray.MenuItem("⚙️ Settings", self._on_tray_settings),
                pystray.MenuItem("📋 About", self._on_tray_about),
                pystray.MenuItem.SEPARATOR,
                pystray.MenuItem("🛑 Exit", self._on_tray_exit)
            )
            
            # Create tray icon
            self.tray_icon = pystray.Icon("Jarvis", image, "Jarvis Assistant", menu)
            
            print("✅ Tray icon created")
            return True
        
        except Exception as e:
            print(f"⚠️  Tray icon error: {e}")
            return False
    
    def _on_tray_listen(self, icon=None, item=None):
        """Tray menu: Start listening."""
        self._on_hotkey_wrapper()
    
    def _on_tray_settings(self, icon=None, item=None):
        """Tray menu: Show settings."""
        print("⚙️  Settings not yet implemented")
    
    def _on_tray_about(self, icon=None, item=None):
        """Tray menu: Show about."""
        print("""
🤖 JARVIS DESKTOP ASSISTANT
Version: 1.0.0
Author: AI Assistant
License: MIT

Features:
- Voice input (Whisper STT)
- AI commands (OpenAI GPT)
- Voice output (OpenAI TTS)
- 1,200+ commands
- System hotkey (Ctrl+Space)
        """)
    
    def _on_tray_exit(self, icon=None, item=None):
        """Tray menu: Exit application."""
        self.stop()
    
    def _run_tray_icon(self):
        """Run tray icon (blocking)."""
        if self.tray_icon:
            self.tray_icon.run()
    
    def _start_terminal_listener(self):
        """
        Start terminal input listener for manual activation.
        Runs in background thread.
        """
        
        def listen_thread():
            print("💻 Terminal listener active (type 'listen' to activate)")
            
            while self.is_running:
                try:
                    # Non-blocking input check
                    import select
                    import sys
                    
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        command = input().strip().lower()
                        
                        if command == "listen":
                            print("\n🎤 Terminal activation: Starting voice input...")
                            self._on_hotkey_wrapper()
                        
                        elif command in ["exit", "quit", "stop"]:
                            print("🛑 Exit command received")
                            self.stop()
                            break
                        
                        elif command:
                            print(f"💬 Unknown command: {command}")
                            print("💡 Type 'listen' to activate Jarvis")
                
                except (EOFError, KeyboardInterrupt):
                    break
                except Exception as e:
                    print(f"⚠️  Terminal listener error: {e}")
                    break
        
        # Start in background thread (non-daemon)
        thread = threading.Thread(target=listen_thread)
        thread.start()
    
    def _start_continuous_listening(self):
        """
        Start continuous voice listening mode.
        Jarvis will listen continuously and respond to voice commands.
        """
        
        def listening_loop():
            print("🎧 Starting continuous voice listening...")
            
            while self.is_running:
                try:
                    print("\n🎤 Listening... (speak now)")
                    
                    # Listen for voice input
                    audio_data = asyncio.run(self.voice_manager.listen())
                    
                    if audio_data:
                        print("✅ Audio captured, processing...")
                        
                        # Convert speech to text
                        text = asyncio.run(self.ai_service.speech_to_text(audio_data))
                        
                        if text:
                            print(f"🗣️  You said: '{text}'")
                            
                            # Process with AI
                            print("🧠 Processing with AI...")
                            intent = asyncio.run(self.ai_service.get_intent_from_ai(text))
                            
                            if intent and intent.get('action') != 'error':
                                print(f"🎯 Intent: {intent.get('action', 'unknown')}")
                                
                                # Execute action
                                print("⚡ Executing action...")
                                action_result = asyncio.run(self.action_dispatcher.dispatch(intent))
                                
                                if action_result.get('success'):
                                    print(f"✅ Success: {action_result.get('result', 'OK')}")
                                else:
                                    print(f"❌ Error: {action_result.get('error', 'Unknown error')}")
                                
                                # Generate voice response
                                response_text = intent.get('response', 'Bajarildi')
                                print(f"\n🔊 Responding: {response_text}")
                                
                                # Convert to speech and play
                                audio_response = asyncio.run(self.ai_service.text_to_speech(response_text))
                                
                                if audio_response:
                                    asyncio.run(self.voice_manager.play_audio(audio_response))
                                    print("✅ Response played")
                                else:
                                    print("❌ TTS failed")
                            
                            else:
                                error_msg = intent.get('response', 'Tushunmadim') if intent else 'Tushunmadim'
                                print(f"❌ AI Error: {error_msg}")
                                
                                # Try to speak error
                                try:
                                    error_audio = asyncio.run(self.ai_service.text_to_speech(error_msg))
                                    if error_audio:
                                        asyncio.run(self.voice_manager.play_audio(error_audio))
                                except:
                                    pass
                        
                        else:
                            print("❌ Speech recognition failed")
                            # Try to speak error
                            try:
                                error_audio = asyncio.run(self.ai_service.text_to_speech("Tushunmadim, qayta ayting"))
                                if error_audio:
                                    asyncio.run(self.voice_manager.play_audio(error_audio))
                            except:
                                pass
                    
                    # Small pause between listens
                    import time
                    time.sleep(1)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"⚠️  Listening error: {e}")
                    import time
                    time.sleep(2)  # Wait before retrying
        
        # Start listening in background thread (non-daemon to avoid shutdown issues)
        thread = threading.Thread(target=listening_loop)
        thread.start()
    
    def start(self) -> bool:
        """
        Start Jarvis application.
        
        Returns:
            True if started successfully
        """
        
        # Initialize components
        if not self.initialize():
            return False
        
        # Create tray icon
        self._create_tray_icon()
        
        # Start terminal listener
        self._start_terminal_listener()
        
        self.is_running = True
        
        print("\n" + "=" * 60)
        print("✅ JARVIS IS READY!")
        print("=" * 60)
        print("\n🎤 VOICE MODE ACTIVE")
        print("  Jarvis is now listening continuously!")
        print("  Speak any command - Jarvis will respond")
        print("\n💡 TRY:")
        print("  • 'youtube och musiqa'")
        print("  • 'bugun sana nima?'")
        print("  • 'google qitir python'")
        print("  • 'vaqt nechada?'")
        print("\n🛑 Press Ctrl+C to exit")
        print("=" * 60 + "\n")
        
        # Start continuous voice listening immediately
        self._start_continuous_listening()
        
        return True
    
    def stop(self):
        """
        Stop Jarvis application.
        """
        
        print("\n\n🛑 Shutting down...")
        
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        if self.tray_icon:
            self.tray_icon.stop()
        
        self.is_running = False
        
        print("✅ Goodbye!")
        sys.exit(0)


def main():
    """
    Main entry point.
    """
    
    # Create and start app
    app = JarvisDesktopApp()
    
    try:
        if app.start():
            print("✅ Jarvis started successfully")
        else:
            print("❌ Failed to start Jarvis")
            sys.exit(1)
    
    except KeyboardInterrupt:
        app.stop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
