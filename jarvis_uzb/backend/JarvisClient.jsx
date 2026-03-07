'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

export default function JarvisClient() {
  const [status, setStatus] = useState('Tizim yuklanmoqda...');
  const [jarvisResponse, setJarvisResponse] = useState('');
  const [isListening, setIsListening] = useState(false);
  const ws = useRef(null);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const audioQueue = useRef([]);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  // 3D Effektlar uchun stillar
  const styles = {
    container: "fixed inset-0 bg-black flex flex-col items-center justify-center overflow-hidden font-mono",
    orbContainer: "relative w-64 h-64 flex items-center justify-center perspective-1000",
    orb: `w-48 h-48 rounded-full border-4 border-cyan-500 shadow-[0_0_50px_rgba(6,182,212,0.6)] 
          flex items-center justify-center transition-all duration-500 animate-pulse`,
    core: "w-32 h-32 bg-cyan-400 rounded-full blur-md opacity-80 animate-ping",
    ring: "absolute w-full h-full border-2 border-cyan-300 rounded-full animate-[spin_4s_linear_infinite]",
    ringReverse: "absolute w-[120%] h-[120%] border border-cyan-700 rounded-full animate-[spin_6s_linear_infinite_reverse]",
    text: "text-cyan-400 text-center mt-8 z-10 max-w-2xl px-4",
    button: `mt-12 px-8 py-3 bg-transparent border border-cyan-500 text-cyan-400 
             rounded hover:bg-cyan-500/20 transition-all duration-300 uppercase tracking-widest
             shadow-[0_0_15px_rgba(6,182,212,0.3)] hover:shadow-[0_0_25px_rgba(6,182,212,0.6)]`,
    downloadBtn: `absolute top-6 right-6 px-6 py-2 border border-green-500 text-green-400 
                  rounded hover:bg-green-500/20 transition-all text-sm uppercase tracking-wider cursor-pointer z-50`
  };

  // Olingan audioni navbat bilan ijro etish
  const playNextAudio = useCallback(() => {
    if (isAudioPlaying || audioQueue.current.length === 0) return;

    setIsAudioPlaying(true);
    const audioBase64 = audioQueue.current.shift();
    const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
    audio.play()
      .then(() => {
        audio.onended = () => {
          setIsAudioPlaying(false);
          playNextAudio();
        };
      })
      .catch(e => {
        console.error("Audio ijro etishda xatolik:", e);
        setIsAudioPlaying(false);
      });
  }, [isAudioPlaying]);

  // WebSocket ulanishini o'rnatish va boshqarish
  useEffect(() => {
    const connect = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws');

      ws.current.onopen = () => setStatus('JARVIS TIZIMI: ONLINE');
      ws.current.onclose = () => {
        setStatus('ALOQA UZILDI. QAYTA ULANMOQDA...');
        setTimeout(connect, 5000);
      };
      ws.current.onerror = (err) => {
        console.error('WebSocket xatoligi:', err);
        setStatus('TIZIM XATOLIGI');
        ws.current.close();
      };
      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'response') {
          setJarvisResponse(message.text);
          if (message.audio_base64) {
            audioQueue.current.push(message.audio_base64);
            if (!isAudioPlaying) playNextAudio();
          }
        } else if (message.type === 'stt_result') {
          setStatus(`QABUL QILINDI: "${message.text}"`);
        }
      };
    };

    connect();

    return () => {
      if (ws.current) ws.current.close();
    };
  }, [playNextAudio, isAudioPlaying]);

  // Ilovani yuklab olish
  const handleDownload = () => {
    window.location.href = "http://localhost:8000/download/app";
  };

  // Ovoz yozishni boshqarish
  const handleListen = async () => {
    if (isListening) {
      mediaRecorder.current?.stop();
      setIsListening(false);
      setStatus('TAHLIL QILINMOQDA...');
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder.current = new MediaRecorder(stream);
        audioChunks.current = [];

        mediaRecorder.current.ondataavailable = (event) => audioChunks.current.push(event.data);
        mediaRecorder.current.onstop = () => {
          const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
          const reader = new FileReader();
          reader.readAsDataURL(audioBlob);
          reader.onloadend = () => {
            const base64Audio = reader.result.split(',')[1];
            if (ws.current?.readyState === WebSocket.OPEN) {
              ws.current.send(JSON.stringify({ type: 'audio_command', audio_base64: base64Audio }));
            }
          };
          stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.current.start();
        setIsListening(true);
        setStatus('ESHITMOQDAMAN...');
      } catch (error) {
        console.error("Mikrofonga ruxsat berilmadi:", error);
        setStatus('MIKROFON XATOLIGI');
      }
    }
  };

  return (
    <div className={styles.container}>
      {/* Orqa fon panjarasi (Grid) */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none" 
           style={{
             backgroundImage: 'linear-gradient(rgba(6,182,212,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(6,182,212,0.3) 1px, transparent 1px)',
             backgroundSize: '40px 40px',
             transform: 'perspective(500px) rotateX(60deg) translateY(100px) scale(2)'
           }}>
      </div>

      {/* Download Button */}
      <button onClick={handleDownload} className={styles.downloadBtn}>
        Ilovani Yuklab Olish
      </button>

      {/* 3D Core Visualization */}
      <div className={styles.orbContainer}>
        <div className={styles.ring}></div>
        <div className={styles.ringReverse}></div>
        
        <div className={`${styles.orb} ${isListening ? 'bg-red-500/20 border-red-500 shadow-red-500/50' : ''}`}>
          <div className={`${styles.core} ${isListening ? 'bg-red-500 animate-pulse' : ''}`}></div>
        </div>
      </div>

      {/* Status va Javoblar */}
      <div className={styles.text}>
        <h2 className="text-xl font-bold tracking-[0.2em] mb-2">{status}</h2>
        <p className="text-lg text-white/90 drop-shadow-[0_0_5px_rgba(255,255,255,0.5)] min-h-[3rem]">
          {jarvisResponse}
        </p>
      </div>

      {/* Boshqaruv Tugmasi */}
      <button 
        onClick={handleListen}
        className={styles.button}
      >
        {isListening ? 'TO\'XTATISH' : 'OVOZLI BUYRUQ'}
      </button>

      {/* Footer */}
      <div className="absolute bottom-4 text-cyan-700 text-xs tracking-widest">
        JARVIS SYSTEM V2.0 • KOMA PRODUCTION
      </div>
    </div>
  );
}