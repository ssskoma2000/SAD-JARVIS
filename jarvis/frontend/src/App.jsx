import React, { Suspense, useState, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, useGLTF } from '@react-three/drei';
import { JarvisModel } from './JarvisModel';

// Base64 audio ma'lumotini ijro etuvchi yordamchi funksiya
const playAudio = (base64Audio) => {
  try {
    const byteCharacters = atob(base64Audio);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(blob);
    const audio = new Audio(audioUrl);
    audio.play();
  } catch (error) {
    console.error("Audio ijro etishda xatolik:", error);
  }
};


function App() {
  const [modelPath, setModelPath] = useState('');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [animationTriggers, setAnimationTriggers] = useState([]);
  const ws = useRef(null);

  // Drag-and-drop uchun
  const dragRef = useRef(null);
  const onMouseDown = (e) => {
    if (e.button !== 0) return;
    window.electronAPI.dragStart(e);
    dragRef.current.addEventListener('mousemove', onMouseMove);
    dragRef.current.addEventListener('mouseup', onMouseUp);
  };
  const onMouseMove = (e) => { window.electronAPI.dragging(e); };
  const onMouseUp = () => {
    window.electronAPI.dragEnd();
    dragRef.current.removeEventListener('mousemove', onMouseMove);
    dragRef.current.removeEventListener('mouseup', onMouseUp);
  };

  useEffect(() => {
    // Model yo'lini olish
    window.electronAPI.getModelPath().then(path => {
      const formattedPath = 'file://' + path;
      setModelPath(formattedPath);
      useGLTF.preload(formattedPath);
    });

    // WebSocket-ga ulanish
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Qabul qilingan ma\'lumot:', data);

        // Matnni chatga qo'shish
        setMessages(prev => [...prev, `JARVIS: ${data.text}`]);
        
        // Agar 'response' turi bo'lsa, ovozni ijro etish va animatsiyani ishga tushirish
        if (data.type === 'response' && data.audio_base64) {
          playAudio(data.audio_base64);
          setAnimationTriggers(data.animation_triggers || []);
        }

      } catch (error) {
        // Agar JSON bo'lmasa, oddiy matn sifatida qabul qilish
        console.log('Oddiy matn qabul qilindi:', event.data);
        setMessages(prev => [...prev, `JARVIS: ${event.data}`]);
      }
    };
    
    ws.current.onopen = () => { console.log('WebSocket ulandi!'); };
    ws.current.onclose = () => { console.log('WebSocket uzildi.'); setMessages(prev => [...prev, 'Aloqa uzildi.']); };
    ws.current.onerror = (err) => { console.error('WebSocket xatoligi:', err); };

    return () => { ws.current.close(); };
  }, []);

  const sendMessage = () => {
    if (input.trim() && ws.current?.readyState === WebSocket.OPEN) {
      setMessages(prev => [...prev, `SIZ: ${input}`]);
      ws.current.send(input);
      setInput('');
    }
  };

  return (
    <div ref={dragRef} className="hud-container" onMouseDown={onMouseDown}>
      <Canvas>
        <Suspense fallback={null}>
          {modelPath && <JarvisModel modelPath={modelPath} animationTriggers={animationTriggers} />}
          <ambientLight intensity={1.5} />
          <pointLight position={[10, 10, 10]} intensity={100} />
          <Environment preset="night" />
          <OrbitControls enabled={false} />
        </Suspense>
      </Canvas>
      <div className="chat-box" onMouseDown={(e) => e.stopPropagation()}>
         {messages.slice(-5).map((msg, index) => <div key={index}>{msg}</div>)}
         <input 
            type="text" value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Buyruq yozing..."
            style={{width: '95%', background: 'transparent', color: 'white', border: 'none', outline: 'none'}}
         />
      </div>
    </div>
  );
}

export default App;