'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Download() {
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = () => {
    setIsDownloading(true);
    setDownloadProgress(0);

    // Simulate download progress
    const interval = setInterval(() => {
      setDownloadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsDownloading(false);
          // Trigger actual download
          const link = document.createElement('a');
          link.href = '/downloads/JarvisSetup.exe'; // This would be the actual file path
          link.download = 'JarvisSetup.exe';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* Background Animation */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-3/4 right-1/4 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute bottom-1/4 left-1/2 w-64 h-64 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Download Jarvis
          </h1>
          <p className="text-xl text-blue-300 mb-8 max-w-3xl mx-auto">
            Get the full Jarvis AI experience on your desktop. Voice-controlled AI assistant with real-time responses.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Download Card */}
          <div className="bg-black/40 backdrop-blur-lg rounded-2xl p-8 border border-blue-500/20 shadow-2xl">
            <div className="text-center mb-8">
              <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-4xl">🤖</span>
              </div>
              <h2 className="text-3xl font-bold text-white mb-4">Jarvis Desktop App</h2>
              <p className="text-gray-300 mb-6">
                Version 1.0.0 | Windows 10+ | Size: ~2GB
              </p>
              <div className="flex justify-center space-x-4 mb-6">
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">Voice Control</span>
                <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">AI Integration</span>
                <span className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-sm">Real-time</span>
              </div>
            </div>

            {/* Download Button */}
            <div className="text-center mb-8">
              {!isDownloading ? (
                <button
                  onClick={handleDownload}
                  className="px-12 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  🚀 Download Now
                </button>
              ) : (
                <div className="space-y-4">
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${downloadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-white text-lg">Downloading... {downloadProgress}%</p>
                </div>
              )}
            </div>

            {/* System Requirements */}
            <div className="border-t border-gray-600 pt-8">
              <h3 className="text-xl font-semibold text-white mb-4">System Requirements</h3>
              <div className="grid md:grid-cols-2 gap-6 text-gray-300">
                <div>
                  <h4 className="font-semibold text-blue-400 mb-2">Minimum:</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Windows 10 (64-bit)</li>
                    <li>• 4GB RAM</li>
                    <li>• 2GB Storage</li>
                    <li>• Microphone (recommended)</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-purple-400 mb-2">Recommended:</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Windows 11</li>
                    <li>• 8GB RAM</li>
                    <li>• SSD Storage</li>
                    <li>• High-quality microphone</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="border-t border-gray-600 pt-8 mt-8">
              <h3 className="text-xl font-semibold text-white mb-4">What's Included</h3>
              <div className="grid md:grid-cols-2 gap-4 text-gray-300">
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>Voice recognition in Uzbek & English</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>OpenAI GPT-4 integration</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>Real-time WebSocket communication</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>40,000+ command support</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>3D Jarvis animations</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-400">✓</span>
                  <span>Secure database integration</span>
                </div>
              </div>
            </div>
          </div>

          {/* Back to Home */}
          <div className="text-center mt-12">
            <Link
              href="/"
              className="inline-block px-8 py-3 bg-transparent border-2 border-blue-400 text-blue-400 font-semibold rounded-lg hover:bg-blue-400 hover:text-white transition-all duration-300"
            >
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
