'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

export const useJarvis = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const [jarvisText, setJarvisText] = useState("Kutmoqdaman...");
  const [animationTriggers, setAnimationTriggers] = useState([]);
  const ws = useRef(null);
  const audioQueue = useRef([]);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  const playNextAudio = useCallback(() => {
    if (isAudioPlaying || audioQueue.current.length === 0) {
      return;
    }

    setIsAudioPlaying(true);
    const audioBase64 = audioQueue.current.shift();
    const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
    
    audio.onended = () => {
      setIsAudioPlaying(false);
      // Keyingi audioni ijro etish
      playNextAudio();
    };

    audio.play().catch(e => {
      console.error("Audio ijro etishda xatolik:", e);
      setIsAudioPlaying(false);
    });
  }, [isAudioPlaying]);

  useEffect(() => {
    if (!ws.current) {
      ws.current = new WebSocket('ws://localhost:8000/ws');

      ws.current.onopen = () => {
        console.log('Backend bilan WebSocket ulanishi o\'rnatildi.');
        setIsConnected(true);
        setJarvisText("Ulanish o'rnatildi. Buyrug'ingizni kuting...");
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setLastMessage(message);
        console.log('Backenddan javob:', message);

        if (message.type === 'response') {
          setJarvisText(message.text);
          if (message.audio_base64) {
            audioQueue.current.push(message.audio_base64);
            playNextAudio();
          }
          if (message.animation_triggers) {
            setAnimationTriggers(message.animation_triggers);
          }
        } else if (message.type === 'greeting') {
            setJarvisText(message.text);
        }
      };

      ws.current.onclose = () => {
        console.log('WebSocket ulanishi uzildi.');
        setIsConnected(false);
        setJarvisText("Ulanish uzildi. Qayta ulanishga harakat qilinmoqda...");
      };

      return () => {
        ws.current.close();
      };
    }
  }, [playNextAudio]);

  const sendCommand = (text) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ type: 'command', text }));
    }
  };

  return { isConnected, jarvisText, animationTriggers, sendCommand };
};