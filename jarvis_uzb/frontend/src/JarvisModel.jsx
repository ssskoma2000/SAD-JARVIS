import React, { useRef, useEffect, useState } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function JarvisModel({ modelPath, animationTriggers = [], ...props }) {
  const group = useRef();
  const { scene, animations, nodes } = useGLTF(modelPath);
  const { actions } = useAnimations(animations, group);
  
  // Animatsiya holatlarini boshqarish
  const [activeAnimation, setActiveAnimation] = useState({ name: 'idle', duration: 0 });

  // 1. Asosiy "suzish" animatsiyasi
  useFrame((state) => {
    if (group.current && activeAnimation.name === 'idle') {
      group.current.position.y = -2 + Math.sin(state.clock.elapsedTime) * 0.1;
    }
  });

  // 2. Backend'dan kelgan triggerlarni kuzatish
  useEffect(() => {
    const trigger = animationTriggers[0]; // Hozircha birinchi triggerni olamiz
    if (trigger === 'confirm') {
      setActiveAnimation({ name: 'nod', duration: 1 }); // 1 soniya davom etadi
    } else if (trigger === 'thinking') {
       setActiveAnimation({ name: 'thinking', duration: 2 });
    }
    // ... boshqa triggerlar uchun shartlar
    
  }, [animationTriggers]);


  // 3. Aktiv animatsiyani bajarish
  useFrame((state) => {
    if (activeAnimation.duration > 0) {
      const elapsedTime = state.clock.getElapsedTime();
      const head = group.current?.getObjectByName("Head"); // Modelda "Head" nomli qism bo'lishi kerak

      if (head) {
        if (activeAnimation.name === 'nod') {
          // Boshni "ha" degandek qimirlatish
          head.rotation.x = Math.sin(elapsedTime * 10) * 0.2;
        } else if (activeAnimation.name === 'thinking') {
          // Boshni "o'ylanayotgandek" qimirlatish
          head.rotation.y = Math.sin(elapsedTime * 2) * 0.3;
        }
      }
      
      // Animatsiya vaqtini kamaytirish
      setActiveAnimation(prev => ({ ...prev, duration: prev.duration - state.clock.getDelta() }));
    } else {
      // Animatsiya tugagach "idle" holatiga qaytish
      if(activeAnimation.name !== 'idle') {
        const head = group.current?.getObjectByName("Head");
        if(head) {
            // Asl holatiga qaytarish
            head.rotation.x = 0;
            head.rotation.y = 0;
        }
        setActiveAnimation({ name: 'idle', duration: 0 });
      }
    }
  });

  // Lab harakatini (Lip Sync) simulatsiya qilish
  // Kelajakda bu qismni audio analiz bilan bog'lash mumkin
  useFrame((state) => {
    const jaw = group.current?.getObjectByName("Jaw"); // Modelda "Jaw" nomli qism bo'lishi kerak
    if(jaw) {
        // Hozircha oddiy, tasodifiy harakat
        jaw.rotation.x = Math.sin(state.clock.elapsedTime * 30) * 0.05;
    }
  });


  return (
    <group ref={group} {...props} dispose={null}>
      <primitive object={scene} scale={2.5} position={[-2, 0, 0]} />
    </group>
  );
}