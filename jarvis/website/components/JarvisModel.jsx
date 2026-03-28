'use client';

import { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function JarvisModel({ isSpeaking }) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const cameraRef = useRef(null);
  const jarvisRef = useRef(null);
  const animationIdRef = useRef(null);

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    rendererRef.current = renderer;
    mountRef.current.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Create Jarvis (simplified 3D model)
    const jarvisGroup = new THREE.Group();

    // Head
    const headGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({
      color: 0x4a90e2,
      emissive: 0x001122,
      shininess: 100
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    jarvisGroup.add(head);

    // Eyes
    const eyeGeometry = new THREE.SphereGeometry(0.05, 16, 16);
    const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });

    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.15, 0.1, 0.45);
    jarvisGroup.add(leftEye);

    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.15, 0.1, 0.45);
    jarvisGroup.add(rightEye);

    // Mouth
    const mouthGeometry = new THREE.BoxGeometry(0.2, 0.05, 0.05);
    const mouthMaterial = new THREE.MeshBasicMaterial({ color: 0x333333 });
    const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
    mouth.position.set(0, -0.15, 0.45);
    jarvisGroup.add(mouth);

    // Body
    const bodyGeometry = new THREE.CylinderGeometry(0.3, 0.4, 1, 32);
    const bodyMaterial = new THREE.MeshPhongMaterial({
      color: 0x2c3e50,
      emissive: 0x000011,
      shininess: 50
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = -0.8;
    jarvisGroup.add(body);

    scene.add(jarvisGroup);
    jarvisRef.current = jarvisGroup;

    // Animation loop
    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);

      if (isSpeaking) {
        // Speaking animation
        head.rotation.y += 0.01;
        mouth.scale.y = 1 + Math.sin(Date.now() * 0.01) * 0.3;
        jarvisGroup.rotation.y += 0.005;
      } else {
        // Idle animation
        head.rotation.y += 0.002;
        mouth.scale.y = 1;
        jarvisGroup.rotation.y += 0.001;
      }

      renderer.render(scene, camera);
    };
    animate();

    // Handle resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [isSpeaking]);

  return (
    <div
      ref={mountRef}
      className="w-full h-96 md:h-[500px] relative"
      style={{ background: 'transparent' }}
    />
  );
}
