'use client';

import { useState } from 'react';
import SplineScene from '@/components/SplineScene';
import JarvisModel from '@/components/JarvisModel';

export default function Home() {
  const [isSpeaking, setIsSpeaking] = useState(false);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* 3D Background Scene */}
      <SplineScene />

      {/* Overlay Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-wider">
            JARVIS
          </h1>
          <p className="text-xl md:text-2xl text-blue-300 mb-8 max-w-2xl mx-auto">
            Your Intelligent AI Assistant
          </p>
          <p className="text-lg text-gray-300 mb-12 max-w-3xl mx-auto">
            Experience the future of AI assistance with voice control, real-time responses,
            and seamless integration with your digital life.
          </p>
        </div>

        {/* Interactive Jarvis Model */}
        <div className="mb-12">
          <JarvisModel isSpeaking={isSpeaking} />
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-6">
          <button
            onClick={() => setIsSpeaking(!isSpeaking)}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            {isSpeaking ? 'Stop Speaking' : 'Speak to Jarvis'}
          </button>
          <a
            href="/download"
            className="px-8 py-4 bg-transparent border-2 border-blue-400 text-blue-400 font-semibold rounded-lg hover:bg-blue-400 hover:text-white transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Download Desktop App
          </a>
        </div>

        {/* Features Preview */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="bg-black/30 backdrop-blur-sm p-6 rounded-lg border border-blue-500/20">
            <div className="text-blue-400 text-3xl mb-4">🎤</div>
            <h3 className="text-white text-xl font-semibold mb-2">Voice Control</h3>
            <p className="text-gray-300">Natural voice commands in Uzbek and English</p>
          </div>
          <div className="bg-black/30 backdrop-blur-sm p-6 rounded-lg border border-purple-500/20">
            <div className="text-purple-400 text-3xl mb-4">🤖</div>
            <h3 className="text-white text-xl font-semibold mb-2">AI Integration</h3>
            <p className="text-gray-300">Powered by OpenAI GPT-4 and Gemini AI</p>
          </div>
          <div className="bg-black/30 backdrop-blur-sm p-6 rounded-lg border border-green-500/20">
            <div className="text-green-400 text-3xl mb-4">⚡</div>
            <h3 className="text-white text-xl font-semibold mb-2">Real-time</h3>
            <p className="text-gray-300">Instant responses and seamless interactions</p>
          </div>
        </div>
      </div>
    </div>
  );
}
