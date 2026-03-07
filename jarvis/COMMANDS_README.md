# 🎯 Jarvis Uzbek Commands Database (1,241 Commands)

## Overview

This directory contains the complete Jarvis command database with **1,241 Uzbek language commands** across 8 major categories. The command system uses a 3-stage parsing engine:

1. **Stage 1: Regex** (ultra-fast, ~50 commands)
2. **Stage 2: Dictionary** (exact, pattern, fuzzy matching; ~1,200 commands)
3. **Stage 3: AI Fallback** (OpenAI ChatGPT for unknown commands)

## 📊 Command Distribution

| Category | Count | Examples |
|----------|-------|----------|
| **Time & Date** | 75 | `what time is it`, `today's date`, `set alarm for 5pm`, `week number` |
| **System Control** | 95 | `shutdown`, `restart`, `lock screen`, `open settings`, `check updates` |
| **Media & Entertainment** | 165 | `play music`, `open YouTube`, `search YouTube for {query}`, `pause`, `next track` |
| **Internet & Browser** | 325 | `search Google`, `open Wikipedia`, `GitHub`, `ChatGPT`, `Stripe`, `Coursera` |
| **Files & Folders** | 145 | `create file`, `open folder`, `copy file`, `compress file`, `search for {query}` |
| **Communication** | 110 | `send email`, `open Gmail`, `Telegram`, `WhatsApp`, `Discord`, `Slack` |
| **Productivity & Reminders** | 195 | `create reminder`, `set timer`, `add task`, `show schedule`, `edit reminder` |
| **User Chat & Info** | 131 | `hello`, `how are you`, `tell me a joke`, `who is {query}`, `weather in {query}` |

**Total: 1,241 Uzbek + English + International commands**

## 📁 File Formats

### `commands.json`
Production-ready JSON with full metadata:

```json
{
  "open YouTube {query}": {
    "intent": "open_youtube",
    "action": "open_url",
    "category": "Media & Entertainment",
    "arguments": ["query"],
    "synonyms": ["youtube {query}", "youtube search {query}"],
    "template": "https://www.youtube.com/results?search_query={query}"
  },
  "what time is it": {
    "intent": "show_time",
    "action": "show_time",
    "category": "Time & Date",
    "arguments": [],
    "synonyms": ["tell the time", "current time", "soat nechada"]
  }
}
```

### `commands.csv`
Tabular format for analysis and import to external tools:

```
pattern,intent,action,category,arguments,synonyms,template
open YouTube {query},open_youtube,open_url,Media & Entertainment,query,youtube {query} | youtube search {query},https://www.youtube.com/results?search_query={query}
what time is it,show_time,show_time,Time & Date,,tell the time | current time | soat nechada,
```

## 🔑 Key Features

### ✅ Uzbek Language Support
- Primary commands in English and Uzbek
- **250+ Uzbek-specific commands** (`soat nechada`, `bugun sana`, `o'chir`, etc.)
- Uzbek city references (Tashkent, Samarkand, Bukhara)
- Cultural references (Silk Road, Timurid dynasty, Uzbek cuisine)

### 🎯 Multi-Synonym Support
Each command includes 3-8 synonyms for maximum flexibility:

```
"open YouTube {query}":
  - "youtube search {query}"
  - "youtube {query}"
  - "search YouTube for {query}"
```

### 🔗 Pattern Matching with `{query}`
Commands that accept dynamic arguments:

```
"search Google for {query}"    → extracts everything after "for"
"play {query}"                 → extracts song/artist name
"send email to {query}"        → extracts recipient
```

### 🌐 100+ Services Integrated
- **Streaming**: Netflix, Spotify, YouTube, Twitch, Disney+, HBO Max
- **Development**: GitHub, Stack Overflow, GitLab, npm, PyPI, Docker
- **Learning**: Coursera, Udemy, Khan Academy, FreeCodeCamp
- **Shopping**: Amazon, eBay, Aliexpress, Etsy
- **Communication**: Gmail, Telegram, WhatsApp, Slack, Discord, Zoom
- **AI Tools**: ChatGPT, Claude, Gemini, Midjourney, DALL-E
- **Finance**: PayPal, Stripe, Yahoo Finance
- **Travel**: Booking.com, Airbnb, Skyscanner
- **Health**: MyFitnessPal, WebMD, Mayo Clinic

### 🚫 Safety & Whitelisting
- **Blocked actions**: `shutdown`, `restart`, `format`, `rm -rf`, `force_close`
- **Safe actions only**: `open_url`, `open_app`, `show_time`, `search_google`
- All attempts logged to SQLite with timestamp and execution time

### 📊 Action Types

| Action | Examples |
|--------|----------|
| `open_url` | Opens browser to URL (often templated with `{query}`) |
| `open_app` | Launches desktop application |
| `show_time` | Returns current time/date |
| `search_google` | Opens Google search results |
| `play_music` | Interacts with music player |
| `create_reminder` | Schedules a reminder/task |
| `ai_response` | AI fallback (Stage 3) |
| `blocked` | Logs attempt as blocked (dangerous command) |

## 🔍 Usage Examples

### 1. Simple Time Command
```
User: "what time is it"
Match: Stage 1 Regex OR Stage 2 Dictionary
Action: show_time
Response: "12:45 PM" + TTS audio
```

### 2. Pattern with Query Parameter
```
User: "open YouTube relaxing music for sleeping"
Match: Stage 2 Dictionary (pattern match)
Template: https://www.youtube.com/results?search_query={query}
Extract: query = "relaxing music for sleeping"
Action: open_url
Result: Opens YouTube with search results
```

### 3. Fuzzy Typo Match (≥80% similarity)
```
User: "whats th tim" (typo)
Match: Stage 2 Fuzzy (RapidFuzz.token_sort_ratio)
Similarity: 85% ≥ 80%
Matched: "what time is it"
Action: show_time
```

### 4. AI Fallback
```
User: "tell me a funny story about a robot"
Stages 1 & 2: No match
Stage 3: AI Fallback (ChatGPT)
System Prompt: "You are Jarvis, Uzbek AI assistant. Respond concisely in Uzbek."
Response: AI-generated story in Uzbek + TTS
```

## 🔧 Integration with Backend

### Python (FastAPI)
```python
from jarvis.command_handler import CommandHandler

handler = CommandHandler()  # Auto-loads commands.json

# Process a command
result = handler.handle("open YouTube cat videos")
# Returns:
# {
#   "stage": "dictionary",
#   "intent": "open_youtube",
#   "action": "open_url",
#   "args": {"query": "cat videos"},
#   "execution_time_ms": 12,
#   "dispatch_result": {"ok": True, "url": "..."}
# }
```

### JavaScript (Frontend - WebSocket)
```javascript
const ws = new WebSocket("ws://localhost:8000/ws");

ws.send(JSON.stringify({
  type: "command",
  text: "search Google for best coffee in Tashkent"
}));

ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  console.log(result.payload); // Command result
};
```

## 📈 Performance Metrics

- **Stage 1 (Regex)**: < 1ms
- **Stage 2 (Dictionary + Fuzzy)**: 5-50ms (depending on fuzzy threshold)
- **Stage 3 (AI Fallback)**: 500-3000ms (API call to OpenAI)
- **Full Pipeline**: ~1-3 seconds average (fastest: regex, slowest: AI)

**Memory footprint**: ~2-5 MB (JSON loaded in memory at startup)

## 🛠 Generation & Maintenance

### Generate Commands
```bash
python3 generate_commands.py
# Output: commands.json (1,241 entries), commands.csv (1,241 rows)
```

### Adding Custom Commands

Edit `generate_commands.py` and add to any category list:

```python
custom_commands.extend([
    {
        "pattern": "my custom command {query}",
        "synonyms": ["alt version {query}", "another way {query}"],
        "intent": "my_custom_intent",
        "action": "open_url",
        "template": "https://example.com/search?q={query}"
    }
])
```

Then regenerate:
```bash
python3 generate_commands.py
```

### Bulk Import from CSV

If you have your own command spreadsheet:

```python
import csv
import json

commands = {}
with open("my_commands.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        commands[row["pattern"]] = {
            "intent": row["intent"],
            "action": row["action"],
            "category": row["category"],
            "arguments": row["arguments"].split(","),
            "synonyms": row["synonyms"].split("|")
        }

with open("commands_merged.json", "w") as f:
    json.dump(commands, f, ensure_ascii=False, indent=2)
```

## 📚 Command Categories Deep Dive

### Time & Date (75 commands)
Covers time-related operations including:
- Current time/date in various formats
- Timezone queries
- Alarms, timers, countdowns
- Holiday calendars
- Leap year, week number calculations
- Sunrise/sunset times

### System Control (95 commands)
Desktop & OS operations:
- Shutdown, restart (blocked)
- Lock screen, logout (blocked)
- Task manager, settings, control panel
- File cleanup, disk defragmentation (blocked)
- Network, firewall, security settings
- Hardware monitoring (CPU, RAM, GPU)
- Mouse, keyboard, display, audio settings

### Media & Entertainment (165 commands)
Streaming and media:
- Music playback control (play, pause, next, volume)
- 15+ streaming services (Netflix, Hulu, Disney+, Prime)
- 12+ music platforms (Spotify, Apple Music, SoundCloud, Pandora)
- YouTube search and playback
- TikTok, Instagram, Twitch
- Audio and podcast apps
- Video recommendations

### Internet & Browser (325 commands)
Web-based services:
- Major search engines (Google, Bing, DuckDuckGo, Yandex)
- Social media (LinkedIn, Reddit, Twitter/X, Facebook)
- Developer tools (GitHub, GitLab, Stack Overflow, npm, PyPI)
- Educational platforms (Coursera, Udemy, Khan Academy)
- Shopping (Amazon, eBay, Aliexpress, Etsy)
- Travel & booking (Airbnb, Booking.com, Skyscanner)
- AI assistants (ChatGPT, Claude, Gemini, Perplexity)
- Finance & crypto (PayPal, CoinGecko, Etherscan)
- Research (Wikipedia, Google Scholar, ArXiv)

### Files & Folders (145 commands)
File management:
- Create, delete, copy, move, rename files/folders
- Open recent files, search for files
- File compression and extraction
- File properties and sorting
- Hide/show hidden files
- Batch operations

### Communication (110 commands)
Messaging & collaboration:
- Email (Gmail, Outlook)
- Messaging apps (Telegram, WhatsApp, Messenger)
- Communication platforms (Slack, Discord, Teams)
- Video conferencing (Zoom, Skype, Google Meet)
- Chat services (Signal, Jami, Matrix, Rocket.Chat)
- Call management (blocked for security)

### Productivity & Reminders (195 commands)
Task & project management:
- Create, edit, delete, reschedule reminders
- Task scheduling with frequency (daily, weekly, monthly, yearly)
- Task priorities (high, normal, low)
- To-do lists, notes, calendar events
- Time tracking and project management (Trello, Asana, Monday.com)
- Office apps (Google Docs, Sheets, Slides, Microsoft Office)
- Design tools (Figma, Adobe XD, Canva)

### User Chat & Info (131 commands)
Conversational AI & knowledge:
- Greetings in Uzbek and English
- Small talk ("how are you", "tell me a joke")
- Knowledge queries ("who is {query}", "what is {query}")
- Weather queries
- Definition and explanation requests
- Language switching commands
- Tips, help, about information

## 🔐 Security Considerations

1. **Blocked Commands**: Operations that could harm the system are blocked and logged
2. **Whitelisting**: Only safe actions (open URL, open app, search) are executed
3. **API Keys**: Stored in `.env`, never hardcoded
4. **Rate Limiting**: Implement on backend to prevent abuse
5. **Audit Logging**: Every command logged with timestamp, stage, outcome
6. **AI Prompt Shield**: System prompt prevents dangerous suggestions

## 🚀 Next Steps

1. **Import to Production Backend**: Load `commands.json` in FastAPI app
2. **Frontend Integration**: Connect to WebSocket for real-time command processing
3. **STT Integration**: Add Whisper/VOSK for voice input
4. **TTS Enhancement**: Replace gTTS with Coqui for offline support
5. **Analytics**: Track most-used commands, success rates, performance
6. **Continuous Learning**: Update commands based on user feedback

## 📞 Support & Feedback

For adding new commands or reporting issues:

1. Edit `generate_commands.py` with your command
2. Run `python3 generate_commands.py`
3. Test in backend: `curl -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"text":"your command"}'`
4. Submit pull request or issue report

---

**Generated**: 1,241 Uzbek Jarvis Commands  
**Categories**: 8 major categories  
**Synonyms**: 3-8 per command  
**Languages**: Uzbek + English + International  
**Export Formats**: JSON + CSV  
**Integration**: FastAPI Backend + Next.js Frontend + WebSocket
