"""
🎙 VOICE MANAGER - STT/TTS INTEGRATION
======================================
Handles real-time voice input/output for Jarvis.
Supports:
- Whisper API for accurate speech recognition
- OpenAI TTS for natural voice output
- Background noise handling
- Real-time audio processing
"""

import asyncio
import numpy as np
from typing import Optional, Callable, List
import os
from dotenv import load_dotenv
from enum import Enum
import time
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import tempfile

load_dotenv()

class AudioFormat(Enum):
    """Supported audio formats."""
    WAV = "wav"
    MP3 = "mp3"
    M4A = "m4a"


class VoiceManager:
    """
    Manages all voice operations (STT, TTS, audio recording).
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_duration: float = 0.1,  # 100ms chunks
        silence_threshold: float = 0.02,  # Silence detection
        silence_duration: float = 2.0  # 2 seconds of silence = end of speech
    ):
        """
        Initialize voice manager.
        
        Args:
            sample_rate: Audio sample rate (Hz)
            channels: Number of audio channels (1=mono)
            chunk_duration: Duration of audio chunk in seconds
            silence_threshold: Volume threshold for silence detection
            silence_duration: Duration of silence to trigger end-of-speech
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = int(sample_rate * chunk_duration)
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        # State
        self._is_recording = False
        self._audio_buffer = []
        self._silence_counter = 0
        
        # Callbacks
        self._on_audio_start: Optional[Callable] = None
        self._on_audio_end: Optional[Callable] = None
        self._on_silent: Optional[Callable] = None
        
        print(f"🎙 VoiceManager initialized (sample_rate: {sample_rate}Hz)")
    
    def set_callbacks(
        self,
        on_start: Optional[Callable] = None,
        on_end: Optional[Callable] = None,
        on_silent: Optional[Callable] = None
    ):
        """
        Set event callbacks.
        
        Args:
            on_start: Called when audio starts
            on_end: Called when audio ends  
            on_silent: Called on prolonged silence
        """
        self._on_audio_start = on_start
        self._on_audio_end = on_end
        self._on_silent = on_silent
    
    def _is_silence(self, audio_chunk: np.ndarray) -> bool:
        """
        Detect if audio chunk is silence.
        
        Args:
            audio_chunk: Audio data
            
        Returns:
            True if silence
        """
        # Calculate RMS (root mean square) volume
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        is_silent = rms < self.silence_threshold
        
        return is_silent
    
    async def listen(
        self,
        timeout: float = 30.0,
        min_duration: float = 0.5
    ) -> Optional[bytes]:
        """
        🎤 Record audio from microphone.
        
        Records until:
        - Silence for 2+ seconds detected, OR
        - Timeout reached
        
        Args:
            timeout: Max recording time (seconds)
            min_duration: Min recording time (seconds)
            
        Returns:
            WAV audio bytes or None on error
        """
        
        try:
            self._is_recording = True
            self._audio_buffer = []
            self._silence_counter = 0
            
            start_time = time.time()
            
            if self._on_audio_start:
                self._on_audio_start()
            
            print("🎤 Listening... (speak now)")
            
            with sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                dtype=np.float32
            ) as stream:
                while self._is_recording:
                    # Read chunk
                    audio_chunk, _ = stream.read(self.chunk_size)
                    self._audio_buffer.append(audio_chunk)
                    
                    # Check for silence
                    if self._is_silence(audio_chunk):
                        self._silence_counter += 1
                        
                        # If enough silence, stop recording
                        if (self._silence_counter * self.chunk_size / self.sample_rate 
                            >= self.silence_duration):
                            
                            # But respect minimum duration
                            elapsed = time.time() - start_time
                            if elapsed >= min_duration:
                                print("⏹ Silence detected, stopping...")
                                break
                    else:
                        self._silence_counter = 0
                    
                    # Check timeout
                    if time.time() - start_time >= timeout:
                        print("⏱ Timeout reached")
                        break
                    
                    # Non-blocking yield (allow cancellation)
                    await asyncio.sleep(0.01)
            
            # Combine chunks into single array
            if self._audio_buffer:
                audio_data = np.concatenate(self._audio_buffer)
                
                # Save to WAV file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    sf.write(tmp.name, audio_data, self.sample_rate)
                    
                    # Read back as bytes
                    with open(tmp.name, "rb") as f:
                        wav_bytes = f.read()
                    
                    os.unlink(tmp.name)
                
                elapsed = time.time() - start_time
                print(f"✅ Recording complete ({elapsed:.1f}s, {len(wav_bytes)} bytes)")
                
                if self._on_audio_end:
                    self._on_audio_end()
                
                return wav_bytes
            else:
                print("❌ No audio recorded")
                return None
        
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
        finally:
            self._is_recording = False
    
    async def play_audio(
        self,
        audio_bytes: bytes,
        format: AudioFormat = AudioFormat.MP3
    ) -> bool:
        """
        🔊 Play audio from bytes.
        
        Args:
            audio_bytes: Audio data
            format: Audio format
            
        Returns:
            True if played successfully
        """
        
        try:
            # Convert to temporary file
            with tempfile.NamedTemporaryFile(suffix=f".{format.value}", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            # Read and play
            audio_data, fs = sf.read(tmp_path)
            
            print(f"🔊 Playing audio ({fs}Hz)...")
            sd.play(audio_data, fs)
            sd.wait()  # Wait for playback to finish
            
            # Cleanup
            os.unlink(tmp_path)
            
            print("✅ Playback complete")
            return True
        
        except Exception as e:
            print(f"❌ Playback error: {e}")
            return False
    
    async def record_to_file(
        self,
        filepath: str,
        duration: float = 5.0
    ) -> bool:
        """
        Record audio directly to file.
        
        Args:
            filepath: Output file path
            duration: Recording duration
            
        Returns:
            True if successful
        """
        
        try:
            print(f"📝 Recording to {filepath} for {duration}s...")
            
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32
            )
            
            sd.wait()
            
            sf.write(filepath, audio_data, self.sample_rate)
            print(f"✅ Saved to {filepath}")
            return True
        
        except Exception as e:
            print(f"❌ File recording error: {e}")
            return False
    
    def get_audio_devices(self) -> List[dict]:
        """
        List available audio input devices.
        
        Returns:
            List of device info
        """
        try:
            devices = sd.query_devices()
            input_devices = []
            
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append({
                        "id": i,
                        "name": device['name'],
                        "channels": device['max_input_channels'],
                        "sample_rate": device['default_samplerate']
                    })
            
            return input_devices
        
        except Exception as e:
            print(f"❌ Device query error: {e}")
            return []
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is working.
        
        Returns:
            True if microphone is accessible
        """
        
        try:
            print("🧪 Testing microphone...")
            
            # Try to open input stream
            with sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size
            ) as stream:
                # Read one chunk
                stream.read(self.chunk_size)
            
            print("✅ Microphone test passed")
            return True
        
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False


class VoiceProcessor:
    """
    Additional voice processing utilities.
    """
    
    @staticmethod
    def normalize_audio(audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to [-1, 1] range.
        
        Args:
            audio: Raw audio data
            
        Returns:
            Normalized audio
        """
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio
    
    @staticmethod
    def remove_silence_edges(
        audio: np.ndarray,
        threshold: float = 0.02,
        sample_rate: int = 16000
    ) -> np.ndarray:
        """
        Remove silence from beginning and end of audio.
        
        Args:
            audio: Input audio
            threshold: Silence threshold
            sample_rate: Sample rate
            
        Returns:
            Trimmed audio
        """
        
        # Find non-silent regions
        energy = np.sqrt(np.mean(audio ** 2))
        non_silent = np.abs(audio) > threshold * energy
        
        # Find first and last non-silent samples
        indices = np.where(non_silent)[0]
        
        if len(indices) == 0:
            return audio
        
        start = indices[0]
        end = indices[-1] + 1
        
        return audio[start:end]
    
    @staticmethod
    def apply_high_pass_filter(
        audio: np.ndarray,
        cutoff: int = 300,
        sample_rate: int = 16000
    ) -> np.ndarray:
        """
        Apply high-pass filter to reduce background noise.
        
        Args:
            audio: Input audio
            cutoff: Cutoff frequency (Hz)
            sample_rate: Sample rate
            
        Returns:
            Filtered audio
        """
        
        try:
            from scipy import signal
            
            nyquist = sample_rate / 2
            normalized_cutoff = cutoff / nyquist
            
            # Design filter
            b, a = signal.butter(5, normalized_cutoff, btype='high')
            
            # Apply filter
            filtered = signal.filtfilt(b, a, audio)
            
            return filtered
        
        except ImportError:
            print("⚠️ scipy not available, skipping filter")
            return audio


# Standalone test
if __name__ == "__main__":
    
    async def test_voice():
        """Test voice manager."""
        
        voice = VoiceManager()
        
        # Test 1: List devices
        print("\n🔊 Available Audio Devices:")
        devices = voice.get_audio_devices()
        for dev in devices:
            print(f"  {dev['id']}: {dev['name']} ({dev['channels']} ch)")
        
        # Test 2: Test microphone
        print("\n🧪 Testing Microphone...")
        if voice.test_microphone():
            print("✅ Microphone working!")
        else:
            print("❌ Microphone not available")
            return
        
        # Test 3: Record audio
        print("\n🎤 Recording 5 seconds...")
        audio_bytes = await voice.listen(timeout=5.0, min_duration=0.5)
        
        if audio_bytes:
            print(f"✅ Recorded {len(audio_bytes)} bytes")
            
            # Test 4: Play back
            print("\n🔊 Playing back...")
            await voice.play_audio(audio_bytes)
    
    # Run test
    asyncio.run(test_voice())
