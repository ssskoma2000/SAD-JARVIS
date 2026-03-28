#!/usr/bin/env python3
"""
🧪 JARVIS VOICE TEST SCRIPT
===========================
Test the complete voice pipeline without hotkeys.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "jarvis_uzb" / "backend"
sys.path.insert(0, str(backend_path))

from ai_services import AIService
from voice_manager import VoiceManager
from action_dispatcher import ActionDispatcher

async def test_voice_pipeline():
    """Test the complete voice pipeline."""

    print("🧪 TESTING JARVIS VOICE PIPELINE")
    print("=" * 50)

    # Initialize components
    print("\n🔧 Initializing components...")

    ai_service = AIService()
    voice_manager = VoiceManager()
    action_dispatcher = ActionDispatcher()

    print("✅ Components initialized")

    # Test 1: AI Service
    print("\n🤖 Testing AI Service...")
    test_text = "Salom, bugun sana nima?"
    print(f"Input: {test_text}")

    intent = await ai_service.get_intent_from_ai(test_text)
    print(f"Intent: {intent}")

    # Test 2: Action Dispatcher
    print("\n🎯 Testing Action Dispatcher...")
    action_result = await action_dispatcher.dispatch(intent)
    print(f"Action result: {action_result}")

    # Test 3: Voice Manager (Text to Speech)
    print("\n🔊 Testing Text-to-Speech...")
    tts_audio = await ai_service.text_to_speech("Salom! Men Jarvisman. Ovoz tizimi ishlayapti!")
    if tts_audio:
        print("✅ TTS generated successfully")
        await voice_manager.play_audio(tts_audio)
        print("✅ Audio played")
    else:
        print("❌ TTS failed")

    print("\n🎉 VOICE PIPELINE TEST COMPLETE!")
    print("\n💡 Now test with real voice:")
    print("   Run: python jarvis_tray.py")
    print("   Type: listen")
    print("   Speak: 'salom' or 'youtube och'")

if __name__ == "__main__":
    asyncio.run(test_voice_pipeline())