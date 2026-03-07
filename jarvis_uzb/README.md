# Jarvis AI Platform

A comprehensive AI assistant platform featuring voice control, real-time responses, and cross-platform compatibility. Built with modern web technologies and desktop applications.

## 🚀 Features

### Core Features
- **Voice Control**: Natural language processing in Uzbek and English
- **Real-time Communication**: WebSocket-based instant responses
- **AI Integration**: Powered by OpenAI GPT-4 and speech services
- **3D Jarvis Model**: Interactive animated AI assistant
- **Cross-platform**: Web, Windows, macOS, Linux, iOS, Android

### Desktop App Features
- **Voice Recognition**: Real-time speech-to-text
- **Audio Playback**: Text-to-speech responses
- **Command System**: 40,000+ supported commands
- **Database Integration**: Secure conversation history
- **Modern UI**: Sleek dark theme with animations

### Web Platform Features
- **Professional Website**: Marketing and download portal
- **3D Spline Models**: Interactive background animations
- **Responsive Design**: Mobile-first approach
- **Download Portal**: Direct app distribution

## 🏗️ Architecture

```
jarvis_uzb/
├── backend/           # Python FastAPI backend
│   ├── main.py       # WebSocket server & API
│   ├── ai_services.py # OpenAI integration
│   ├── command_handler.py # Command processing
│   ├── database_manager.py # Data persistence
│   └── security_utils.py # Security features
├── website/          # Next.js marketing site
│   ├── app/         # Next.js 13+ app router
│   └── components/  # React components
├── desktop/         # C# MAUI desktop app
│   └── CSharpProject/ # MAUI application
└── infra/           # Infrastructure as code
```

## 🛠️ Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI**: High-performance async web framework
- **WebSockets**: Real-time communication
- **OpenAI API**: GPT-4, TTS, Whisper
- **SQLite**: Local database
- **Uvicorn**: ASGI server

### Frontend (Web)
- **Next.js 14**: React framework
- **Tailwind CSS**: Utility-first styling
- **Three.js**: 3D graphics
- **Spline**: 3D model integration
- **Framer Motion**: Animations

### Desktop App
- **.NET 8**: Cross-platform framework
- **MAUI**: Multi-platform UI framework
- **NAudio**: Audio processing
- **WebView**: Embedded 3D models
- **WebSockets**: Backend communication

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- .NET 8 SDK
- OpenAI API Key

### Backend Setup
```bash
cd jarvis_uzb/backend
pip install -r requirements.txt
# Set OPENAI_API_KEY in .env
python main.py
```

### Website Setup
```bash
cd jarvis_uzb/website
npm install
npm run dev
```

### Desktop App Setup
```bash
cd jarvis_uzb/desktop/CSharpProject
dotnet restore
dotnet build
dotnet run
```

## 📱 Desktop App Installation

### Windows
1. Download `JarvisSetup.exe` from the website
2. Run installer as administrator
3. Launch Jarvis Desktop App
4. Ensure backend is running on port 8000

### System Requirements
- **Minimum**: Windows 10, 4GB RAM, 2GB storage
- **Recommended**: Windows 11, 8GB RAM, SSD storage

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///jarvis.db
WEBSOCKET_PORT=8000
```

### Desktop App Settings
- Audio input/output devices
- Language preferences (Uzbek/English)
- Animation settings
- Database location

## 🎯 Usage

### Voice Commands
- "Salom" - Greeting
- "Soat necha?" - Current time
- "Chrome och" - Open Chrome browser
- "Telegram och" - Open Telegram
- Custom AI commands via natural language

### Desktop App Controls
- **🎤 Speak**: Voice input button
- **👋 Wave**: Animation trigger
- **⚙️ Settings**: Configuration panel
- **Real-time Chat**: Message history

## 🔒 Security Features

### Frontend Security
- **Input Validation**: All user inputs validated and sanitized using DOMPurify
- **CORS Protection**: Strict origin policies for API calls
- **Asset Protection**: Secure serving of 3D models and textures
- **XSS Prevention**: HTML sanitization for all dynamic content

### Backend Security
- **Rate Limiting**: Request throttling to prevent DOS attacks (100 requests/minute)
- **Input Validation**: Pydantic models for all endpoints and WebSocket messages
- **Authentication**: JWT-based user authentication with secure token storage
- **API Key Protection**: Encrypted storage of OpenAI and other sensitive credentials
- **HTTPS/WebSocket**: Encrypted communications only

### Desktop Security
- **File Access Control**: Restricted system file access (no access to /etc, C:\Windows)
- **Signed Installers**: Secure update mechanisms with checksum validation
- **Anti-tampering**: Checksum validation for releases and isolated runtime environment

## 🧪 Testing & Debugging

### Automated Testing
- **Unit Tests**: Pytest for backend functions and API endpoints
- **Integration Tests**: WebSocket and database operations testing
- **UI Tests**: MAUI automated interface testing for desktop app
- **Load Testing**: Multi-user simulation to test server performance
- **Security Testing**: Input validation and injection attack prevention

### Debug Features
- **Comprehensive Logging**: Uvicorn and application-level logging with error tracking
- **Performance Monitoring**: FPS monitoring for 3D models and response times
- **Crash Reporting**: Automatic error reporting with user consent
- **Development Tools**: Debug builds with detailed diagnostics and console output

### CI/CD Pipeline
- **GitHub Actions**: Automated testing on every commit and pull request
- **Code Quality**: Linting, security scanning, and dependency checks
- **Version Control**: Semantic versioning with automated rollback capabilities
- **Sandbox Testing**: Isolated environment testing for AI-generated code

### Uzbek Language Support
- **Natural Language Processing**: Full Uzbek language support for voice and text commands
- **TTS Integration**: Text-to-speech in Uzbek using OpenAI voices
- **Cultural Adaptation**: Commands and responses tailored for Uzbek users
- **Code Generation**: Ability to generate code in requested languages with Uzbek explanations

## 📊 Database Schema

```sql
-- Messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT
);

-- Commands table
CREATE TABLE commands (
    id INTEGER PRIMARY KEY,
    command_text TEXT NOT NULL,
    response_text TEXT,
    audio_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Real-time communication

### REST API
- `GET /` - Health check
- `POST /command` - Text command processing
- `POST /audio` - Audio command processing

## 🎨 UI/UX Design

### Color Scheme
- **Primary**: #4a90e2 (Blue)
- **Secondary**: #7c3aed (Purple)
- **Background**: #0a192f (Dark Blue)
- **Accent**: #10b981 (Green)

### Typography
- **Primary Font**: Inter (Web), System Fonts (Desktop)
- **Sizes**: Responsive scaling
- **Weights**: Regular, Medium, Bold

## 🚀 Deployment

### Backend
```bash
# Production deployment
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Website
```bash
# Build for production
npm run build
npm start
```

### Desktop App
```bash
# Windows build
.\build_scripts\build_windows.ps1 -Configuration Release
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is proprietary software. All rights reserved.

## 👨‍💻 Author

**Koma** - *Creator & Lead Developer*
- Project: Jarvis AI Platform
- Tech Stack: Full-Stack AI Development
- Contact: iTech Innovations

## 🙏 Acknowledgments

- OpenAI for GPT-4 and speech services
- Microsoft for .NET MAUI framework
- Three.js community for 3D graphics
- FastAPI for excellent Python web framework

---

**Experience the future of AI assistance with Jarvis!** 🤖✨
