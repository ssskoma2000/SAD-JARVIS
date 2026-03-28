"""
⌨️ HOTKEY MANAGER - Windows Hotkey Binding
===========================================
Handles global hotkey listening for Jarvis desktop app.
Primary: Ctrl + Space to activate
Supports custom hotkey assignments.
"""

import threading
from typing import Optional, Callable, Dict
from enum import Enum
import time
from datetime import datetime

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("⚠️  pynput not installed. Install with: pip install pynput")


class ModifierKey(Enum):
    """Keyboard modifier keys."""
    CTRL = "ctrl"
    SHIFT = "shift"
    ALT = "alt"
    WIN = "cmd"  # Windows key


class HotKey:
    """Represents a single hotkey combination."""
    
    def __init__(self, modifiers: list, key: str):
        """
        Create hotkey.
        
        Args:
            modifiers: List of ModifierKey values
            key: Key name (e.g., 'space', 'f1', 'j')
        """
        self.modifiers = modifiers
        self.key = key
        self.display_name = self._format_display()
    
    def _format_display(self) -> str:
        """Format hotkey for display."""
        parts = [m.value.upper() for m in self.modifiers] + [self.key.upper()]
        return " + ".join(parts)
    
    def __str__(self) -> str:
        return self.display_name
    
    def __repr__(self) -> str:
        return f"HotKey({self.display_name})"


class HotKeyManager:
    """
    Global hotkey listener for Windows desktop application.
    Listens for hotkey in background thread.
    """
    
    def __init__(self):
        """Initialize hotkey manager."""
        
        if not PYNPUT_AVAILABLE:
            raise ImportError("pynput is required. Install with: pip install pynput")
        
        self._hotkeys: Dict[str, HotKey] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._listener: Optional[keyboard.Listener] = None
        self._is_listening = False
        self._pressed_keys = set()
        
        # Register default hotkey (Ctrl + Space)
        self.register_hotkey(
            "activate",
            [ModifierKey.CTRL],
            "space",
            lambda: print("🎙 Hotkey pressed: Ctrl+Space")
        )
        
        print("⌨️ HotKeyManager initialized")
    
    def register_hotkey(
        self,
        name: str,
        modifiers: list,
        key: str,
        callback: Callable
    ) -> bool:
        """
        Register a new hotkey.
        
        Args:
            name: Hotkey identifier (e.g., 'activate')
            modifiers: List of ModifierKey values
            key: Key name
            callback: Function to call when hotkey pressed
            
        Returns:
            True if registered successfully
        """
        
        try:
            hotkey = HotKey(modifiers, key)
            self._hotkeys[name] = hotkey
            self._callbacks[name] = callback
            
            print(f"✅ Hotkey registered: {name} = {hotkey}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to register hotkey: {e}")
            return False
    
    def unregister_hotkey(self, name: str) -> bool:
        """
        Unregister a hotkey.
        
        Args:
            name: Hotkey identifier
            
        Returns:
            True if unregistered
        """
        
        if name in self._hotkeys:
            del self._hotkeys[name]
            del self._callbacks[name]
            print(f"✅ Hotkey unregistered: {name}")
            return True
        
        return False
    
    def _on_press(self, key):
        """Internal: Called when any key is pressed."""
        
        try:
            # Get key name
            if hasattr(key, 'name'):
                key_name = key.name
            elif hasattr(key, 'char'):
                key_name = key.char
            else:
                key_name = str(key)
            
            # Track pressed keys
            self._pressed_keys.add(key_name)
            
            # Check all registered hotkeys
            for hotkey_name, hotkey in self._hotkeys.items():
                if self._check_hotkey_pressed(hotkey):
                    # Call callback in thread to avoid blocking listener
                    callback = self._callbacks[hotkey_name]
                    thread = threading.Thread(
                        target=callback,
                        name=f"hotkey-{hotkey_name}"
                    )
                    thread.daemon = True
                    thread.start()
                    
                    print(f"🔥 Hotkey triggered: {hotkey_name} ({hotkey})")
        
        except Exception as e:
            print(f"⚠️  Key press handler error: {e}")
    
    def _on_release(self, key):
        """Internal: Called when any key is released."""
        
        try:
            # Get key name
            if hasattr(key, 'name'):
                key_name = key.name
            elif hasattr(key, 'char'):
                key_name = key.char
            else:
                key_name = str(key)
            
            # Remove from pressed keys
            self._pressed_keys.discard(key_name)
        
        except Exception as e:
            print(f"⚠️  Key release handler error: {e}")
    
    def _check_hotkey_pressed(self, hotkey: HotKey) -> bool:
        """
        Check if a hotkey combination is currently pressed.
        
        Args:
            hotkey: HotKey to check
            
        Returns:
            True if hotkey pressed
        """
        
        # Check if all modifier keys are pressed
        for modifier in hotkey.modifiers:
            if modifier == ModifierKey.CTRL:
                if 'ctrl_l' not in self._pressed_keys and 'ctrl_r' not in self._pressed_keys:
                    return False
            elif modifier == ModifierKey.SHIFT:
                if 'shift_l' not in self._pressed_keys and 'shift_r' not in self._pressed_keys:
                    return False
            elif modifier == ModifierKey.ALT:
                if 'alt_l' not in self._pressed_keys and 'alt_r' not in self._pressed_keys:
                    return False
            elif modifier == ModifierKey.WIN:
                if 'cmd_l' not in self._pressed_keys and 'cmd_r' not in self._pressed_keys:
                    return False
        
        # Check if the main key is pressed
        if hotkey.key not in self._pressed_keys:
            return False
        
        return True
    
    def start(self) -> bool:
        """
        Start listening for hotkeys (background thread).
        
        Returns:
            True if listener started
        """
        
        if self._is_listening:
            print("⚠️  Listener already running")
            return True
        
        try:
            self._listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self._listener.start()
            self._is_listening = True
            
            print("🎧 Hotkey listener started")
            return True
        
        except Exception as e:
            print(f"❌ Failed to start listener: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop listening for hotkeys.
        
        Returns:
            True if listener stopped
        """
        
        if not self._is_listening:
            print("⚠️  Listener not running")
            return True
        
        try:
            if self._listener:
                self._listener.stop()
            self._is_listening = False
            
            print("🛑 Hotkey listener stopped")
            return True
        
        except Exception as e:
            print(f"❌ Failed to stop listener: {e}")
            return False
    
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._is_listening
    
    def get_hotkeys(self) -> Dict[str, str]:
        """
        Get all registered hotkeys.
        
        Returns:
            Dict of {name: display_string}
        """
        return {name: str(hk) for name, hk in self._hotkeys.items()}


# Convenience function for quick setup
def create_jarvis_hotkey_manager(
    on_activate: Callable
) -> Optional[HotKeyManager]:
    """
    Create and start a hotkey manager configured for Jarvis.
    
    Args:
        on_activate: Callback when Ctrl+Space pressed
        
    Returns:
        Configured HotKeyManager or None on error
    """
    
    try:
        manager = HotKeyManager()
        
        # Register Jarvis hotkey
        manager.register_hotkey(
            "jarvis_activate",
            [ModifierKey.CTRL],
            "space",
            on_activate
        )
        
        # Start listening
        if manager.start():
            print("✅ Jarvis hotkey manager ready (Ctrl+Space)")
            return manager
        else:
            return None
    
    except Exception as e:
        print(f"❌ Failed to create hotkey manager: {e}")
        return None


# Standalone test
if __name__ == "__main__":
    """Test hotkey manager."""
    
    def on_hotkey():
        """Called when Ctrl+Space pressed."""
        print("🔥 HOTKEY TRIGGERED! Ctrl+Space pressed!")
    
    # Create manager
    manager = HotKeyManager()
    
    # Register custom hotkeys
    manager.register_hotkey("activate", [ModifierKey.CTRL], "space", on_hotkey)
    manager.register_hotkey("exit", [ModifierKey.CTRL, ModifierKey.ALT], "q", 
                           lambda: print("Exit hotkey!"))
    
    # Show registered hotkeys
    print("\n📋 Registered hotkeys:")
    for name, hotkey_str in manager.get_hotkeys().items():
        print(f"  {name}: {hotkey_str}")
    
    # Start listening
    print("\n🎧 Starting listener...")
    if manager.start():
        print("Press Ctrl+Space to trigger hotkey")
        print("Press Ctrl+Alt+Q to exit")
        
        try:
            # Keep running
            while manager.is_listening():
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
            manager.stop()
    else:
        print("❌ Failed to start listener")
