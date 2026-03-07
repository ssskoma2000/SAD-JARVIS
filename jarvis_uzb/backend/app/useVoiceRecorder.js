import { useState, useRef, useEffect, useCallback } from "react";

/**
 * Ovoz yozish va WebSocket orqali yuborish uchun maxsus React hook.
 * @param {string} url - WebSocket server manzili (masalan, 'ws://localhost:8000/ws').
 * @param {(data: object) => void} onMessageReceived - WebSocket'dan xabar kelganda ishga tushadigan funksiya.
 */
const useVoiceRecorder = (url, onMessageReceived) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isConnecting, setIsConnecting] = useState(true);
  const mediaRecorderRef = useRef(null);
  const webSocketRef = useRef(null);
  const audioChunksRef = useRef([]);

  // WebSocket ulanishini o'rnatish va boshqarish
  useEffect(() => {
    if (!url) return;

    const ws = new WebSocket(url);
    webSocketRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket muvaffaqiyatli ulandi.");
      setIsConnecting(false);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (onMessageReceived) {
          onMessageReceived(data);
        }
      } catch (error) {
        console.error("WebSocket'dan kelgan xabarni o'qishda xatolik:", error);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket xatoligi:", error);
      setIsConnecting(false);
    };

    ws.onclose = () => {
      console.log("WebSocket ulanishi uzildi.");
      setIsConnecting(true);
    };

    // Komponent o'chirilganda WebSocket ulanishini uzish
    return () => {
      ws.close();
    };
  }, [url, onMessageReceived]);

  const startRecording = useCallback(async () => {
    if (isRecording || isConnecting) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });
        if (
          webSocketRef.current &&
          webSocketRef.current.readyState === WebSocket.OPEN
        ) {
          // Blob'ni to'g'ridan-to'g'ri yuborish
          webSocketRef.current.send(audioBlob);
        }
        // Ovoz yozib bo'lingach, mikrofonni bo'shatish
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Mikrofonga ruxsat olishda xatolik:", error);
      alert("Iltimos, mikrofondan foydalanishga ruxsat bering.");
    }
  }, [isRecording, isConnecting]);

  const stopRecording = useCallback(() => {
    if (!isRecording || !mediaRecorderRef.current) return;

    mediaRecorderRef.current.stop();
    setIsRecording(false);
  }, [isRecording]);

  return {
    isRecording,
    isConnecting,
    startRecording,
    stopRecording,
  };
};

export default useVoiceRecorder;
