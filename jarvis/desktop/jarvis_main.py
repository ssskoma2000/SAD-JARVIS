import sys
import os
import asyncio
import threading
import numpy as np
import pyttsx3
import speech_recognition as sr
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QTextEdit, QSlider, QLabel)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.builder import JarvisBuilder
from backend.app.ai_services import get_ai_response

class JarvisSignals(QObject):
    log = pyqtSignal(str)
    speak = pyqtSignal(str)
    volume_changed = pyqtSignal(float)

class Jarvis3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pulse = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)
        self.is_active = False

    def initializeGL(self):
        glClearColor(0.02, 0.02, 0.05, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)
        
        self.pulse += 0.05
        scale = 1.0 + (0.3 * math.sin(self.pulse) if self.is_active else 0.05 * math.sin(self.pulse))
        
        # Jarvisning 3D yadrosi (Futuristik sfera)
        glColor4f(0.0, 0.8, 1.0, 0.6)
        for i in range(12):
            glRotatef(30, 0, 1, 1)
            self.draw_circle(scale)

    def draw_circle(self, radius):
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2 * math.pi * i / 100
            glVertex2f(radius * math.cos(theta), radius * math.sin(theta))
        glEnd()

class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS AI - Professional Edition")
        self.resize(1100, 800)
        self.setStyleSheet("background-color: #050510; color: #00d4ff; font-family: 'Consolas';")
        
        self.signals = JarvisSignals()
        self.builder = JarvisBuilder()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.current_volume = 0.8

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 3D Avatar
        self.avatar = Jarvis3D()
        layout.addWidget(self.avatar, stretch=5)

        # Chat & Logs
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #0a0a20; border: 1px solid #0055ff; color: #00d4ff; font-size: 14px;")
        layout.addWidget(self.log_box, stretch=3)

        # Controls
        controls = QHBoxLayout()
        self.start_btn = QPushButton("INITIALIZE JARVIS")
        self.start_btn.setFixedSize(200, 50)
        self.start_btn.setStyleSheet("background-color: #004488; font-weight: bold; border-radius: 10px;")
        self.start_btn.clicked.connect(self.toggle_system)
        
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(80)
        
        controls.addWidget(self.start_btn)
        controls.addWidget(QLabel("VOLUME:"))
        controls.addWidget(self.vol_slider)
        layout.addLayout(controls)

    def setup_connections(self):
        self.signals.log.connect(self.add_log)
        self.signals.speak.connect(self.speak_text)
        self.vol_slider.valueChanged.connect(self.update_volume)

    def add_log(self, text):
        self.log_box.append(f"[{self.get_time()}] {text}")

    def get_time(self):
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")

    def update_volume(self, value):
        self.current_volume = value / 100.0
        self.engine.setProperty('volume', self.current_volume)

    def speak_text(self, text):
        self.avatar.is_active = True
        self.add_log(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        self.avatar.is_active = False

    def toggle_system(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_btn.setText("SHUTDOWN")
            self.start_btn.setStyleSheet("background-color: #aa0000; border-radius: 10px;")
            self.signals.speak.emit("Tizim ishga tushirildi. Shu yerda man, bo'ss.")
            threading.Thread(target=self.voice_listener_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.start_btn.setText("INITIALIZE JARVIS")
            self.start_btn.setStyleSheet("background-color: #004488; border-radius: 10px;")

    def voice_listener_loop(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = r.listen(source, timeout=3, phrase_time_limit=5)
                    # Adaptive Volume Logic
                    rms = self.calculate_rms(audio)
                    if rms > 0.1: # Agar baland ovozda gapirilsa
                         self.signals.volume_changed.emit(min(1.0, self.current_volume + 0.1))
                    
                    text = r.recognize_google(audio, language="uz-UZ").lower().strip()
                    self.signals.log.emit(f"Siz: {text}")
                    
                    # "Jarvis" triggeri
                    if text == "jarvis":
                        self.signals.speak.emit("Shu yerda man.")
                        continue
                    elif "jarvis" in text:
                        self.handle_command(text)
                except Exception:
                    continue

    def calculate_rms(self, audio):
        data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
        return np.sqrt(np.mean(data**2)) / 32768.0

    def handle_command(self, text):
        if any(kw in text for kw in ["yarat", "build", "yozib ber"]):
            lang = "python"
            if "c++" in text: lang = "cpp"
            elif "c#" in text: lang = "c#"
            elif "javascript" in text or "js" in text: lang = "js"
            
            self.signals.speak.emit(f"{lang} tilida kod tayyorlanmoqda va EXE qilinmoqda...")
            threading.Thread(target=self.run_async_build, args=(lang, text), daemon=True).start()
        else:
            response = asyncio.run(get_ai_response(text))
            self.signals.speak.emit(response)

    def run_async_build(self, lang, text):
        prompt = f"""Faqat toza va ishlaydigan {lang} kodi qaytarilsin. 
        Markdown formatisiz, tushuntirishlarsiz. 
        Vazifa: {text}"""
        
        code = asyncio.run(get_ai_response(prompt))
        # Markdown belgilarini tozalash (agar AI baribir qo'shsa)
        code = code.replace("```" + lang, "").replace("```", "").strip()
        
        result = asyncio.run(self.builder.build(lang, code, "JarvisBuild"))
        self.signals.log.emit(result)
        self.signals.speak.emit("Dastur tayyor. Dist papkasidan olishingiz mumkin.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = JarvisApp()
    jarvis.show()
    sys.exit(app.exec())