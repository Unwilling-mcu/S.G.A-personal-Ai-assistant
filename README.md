<div align="center">

```
███████╗ ██████╗      █████╗ 
██╔════╝██╔════╝     ██╔══██╗
███████╗██║  ███╗    ███████║
╚════██║██║   ██║    ██╔══██║
███████║╚██████╔╝    ██║  ██║
╚══════╝ ╚═════╝     ╚═╝  ╚═╝
```

# S.G.A — Personal AI Assistant

**Your own JARVIS. Voice-controlled. Always listening. Fully local.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![Electron](https://img.shields.io/badge/Electron-28-47848F?style=flat&logo=electron&logoColor=white)](https://electronjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks_API-FF6F00?style=flat&logo=google&logoColor=white)](https://mediapipe.dev)
[![SQLite](https://img.shields.io/badge/SQLite-Memory-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)]()

<br/>

> *"Good morning, Sir. All systems are operational. Weather in Asansol: Clear sky, 28°C. You have 3 pending tasks."*

<br/>

**S.G.A** (Smart General Assistant) is a fully voice-controlled personal AI desktop assistant built entirely from scratch — inspired by JARVIS from Iron Man and ADA v2. It runs as a real Electron desktop app, listens 24/7, and can control your PC, browse the web, write code, manage tasks, describe your screen, translate languages, perform gesture control, generate 3D CAD models, authenticate with your face, and much more — all through natural voice commands.

[**Features**](#-features) · [**Architecture**](#-architecture) · [**Installation**](#-installation) · [**Commands**](#-voice-commands) · [**Roadmap**](#-roadmap)

</div>

---

## 🎬 What It Looks Like

```
⚡ S . G . A
┌─────────────────┐  ┌──────────────────────┐  ┌────────────────────┐
│  SYSTEM STATUS  │  │   [Holographic Core]  │  │  AI INTELLIGENCE   │
│                 │  │    ◉ Thinking...      │  │  INTENT: action    │
│ Status: ●Active │  │  ~~~~ waveform ~~~~   │  │  ACTIONS:          │
│ Uptime: 00:12:4 │  │  → Processing...      │  │  [enable_gesture]  │
│ Mode: LISTENING │  │  → Executing...       │  │  PARSED: gesture   │
│ Exchanges: 47   │  │                       │  │    control         │
└─────────────────┘  └──────────────────────┘  └────────────────────┘

[💬 CHAT] [✅ TASKS] [🗂 MEMORY]          ✋ GESTURES  [floating orb ◉]
────────────────────────────────────────────────────────────
YOU  "enable gesture control"
AI   Gesture control activated. Show your hand to the camera, Sir.
────────────────────────────────────────────────────────────
YOU  "what is 25% of 2000"
AI   The answer is 500
────────────────────────────────────────────────────────────
```

---

## ✨ Features

### 🎙️ Voice & Intelligence
| Feature | Description |
|---|---|
| Always-on voice loop | Listens continuously, zero clicks needed |
| Wake word mode | Say *"Hey S.G.A"* or *"Jarvis"* to activate |
| Google Speech STT | Fast cloud-based recognition |
| Whisper STT (optional) | Local, highly accurate, works offline |
| JARVIS personality | Calm, witty, addresses you as *"Sir"* |
| SQLite memory | Persistent across restarts, 200 interactions |
| Context awareness | Uses recent conversation in replies |
| Morning briefing | Weather + news + tasks read aloud on startup |
| Settings control | Change features by voice or `settings.json` |

### 🤖 AI Chain (auto-fallback)
```
Gemini 2.0 Flash Lite  →  Ollama/Mistral (local)  →  Wikipedia + DuckDuckGo (free)
```
Everything except code generation and complex questions works **completely free** with no API key.

### 💻 PC Control
| Say | Does |
|---|---|
| *"Open Chrome / Notepad / VS Code / Calculator"* | Launches app |
| *"Open YouTube / Netflix / Gmail / WhatsApp"* | Opens website in Chrome |
| *"Volume up / down / mute"* | Controls Windows audio |
| *"Take a screenshot"* | Saves PNG to Desktop |
| *"What's on my screen?"* | Gemini Vision describes screen |
| *"Type hello world"* | Types at current cursor |
| *"Switch to Spotify"* | Brings running app to front |
| *"Lock screen"* | Locks PC instantly |
| *"Shutdown / restart my PC"* | System power with 10s warning |
| *"Kill Chrome"* | Terminates any process |

### 🖐️ Gesture Control *(MediaPipe Tasks API)*
Full contactless PC control via hand gestures detected through your webcam:

| Gesture | Action |
|---|---|
| ☝️ Point (index finger) | Moves mouse cursor in real-time |
| 🤏 Pinch (thumb + index) | Left click |
| ✊ Fist | Select / grab |
| ✋ Open palm | Pause S.G.A |
| 👍 Thumbs up | Volume up |
| 👎 Thumbs down | Volume down |
| 🖐️ Five fingers | Screenshot |
| ✌️ Peace sign | Scroll mode |

Air tracing mode: point your index finger to draw on screen.

**Activate:** Say *"enable gesture control"* or *"gesture mode"*

### 🔐 Face Biometric Authentication *(face_recognition + MediaPipe)*
- **High accuracy mode** — `face_recognition` + `dlib-bin`: recognises *you specifically*, rejects others
- **Presence mode** — MediaPipe: any face unlocks (no extra setup)
- **App-level access control** — protected apps require re-authentication every 5 min
- **Session persistence** — authenticated session lasts configurable duration

**Setup:** Say *"take reference photo"* → enable in `settings.json`

### 🧊 3D CAD Model Generation *(build123d)*
Voice → parametric 3D model → STL file ready for 3D printing:
```
"Create a cube 5cm by 5cm by 5cm"        → cad_models/cube_50x50x50_1.stl
"Make a cylinder radius 3cm height 8cm"  → cad_models/cylinder_r30_h80_2.stl
"Design a phone stand 60 degree angle"   → cad_models/phone_stand_60deg_3.stl
"Create a sphere radius 2cm"             → cad_models/sphere_r20_4.stl
"Make a bracket 10cm by 5cm"             → cad_models/bracket_100x50_5.stl
```
Complex models use Gemini to write `build123d` Python code and execute it safely.
Open `.stl` files in **Microsoft 3D Viewer** (built into Windows) to preview.

### 🧠 Knowledge & Information
| Say | Does |
|---|---|
| *"Tell me about [topic]"* | Wikipedia summary |
| *"Who is [person]"* | Wikipedia biography |
| *"Latest [topic] news"* | Google News RSS headlines — free |
| *"Weather in [city]"* | Real-time via Open-Meteo — free, no key |
| *"Search [query]"* | Google in Chrome |

### 🔢 Math, Conversions & Translation *(instant, no internet)*
```
"What is 25% of 2000"          →  The answer is 500
"What is 25 times 48"          →  The answer is 1200
"100 plus 200"                 →  The answer is 300
"10 divided by 2"              →  The answer is 5
"Convert 10 km to miles"       →  6.21 miles
"Convert 37 celsius to F"      →  98.6°F
"Convert 5 kg to pounds"       →  11.02 lbs
"Translate hello to Hindi"     →  नमस्ते
"Translate good morning to Japanese"  →  おはようございます
```
Supports 15+ languages. Unit conversions: km/miles, kg/lbs, °C/°F, m/feet, litres/gallons, cm/inches.

### 💻 Code Generation *(Gemini powered)*
Generates production-quality code with syntax highlighting and Copy button:
```
"Write a Python function to sort a list"
"Write a C++ bubble sort program"
"Write a Java calculator class"
"Create an HTML login page with CSS"
"Write a SQL query to find duplicates"
"Write a Bash script to backup files"
```

### ✅ Voice-Controlled Task Manager
```
"Add task buy groceries"        →  Task added
"My tasks"                      →  Pending: 1. buy groceries; 2. call mom
"Complete task 1"               →  Marked done
"Delete task groceries"         →  Deleted
"Clear completed tasks"         →  Cleared
```
Stored in SQLite — persists between sessions. Visible in the dedicated **Tasks tab**.

### 🌐 Real Web Browsing *(Playwright)*
S.G.A actually opens Chrome and browses — not just search:
```
"Search YouTube for Python tutorials"   → Returns top video titles
"Search Amazon for wireless headphones" → Returns products + prices
"Go to timesofindia.com"               → Opens and reads the page
```

### 🔧 System Information
```
"System info"     →  CPU 12%, RAM 6GB/16GB, Disk 120GB/512GB
"Battery level"   →  78%, on battery, ~142 minutes remaining
"What's running"  →  Chrome (PID 1234) 8.2% CPU; Discord 2.1%
"Kill Chrome"     →  Terminates process
```

### 📋 Clipboard & Files
```
"Read my clipboard"                    →  Reads what you copied
"Copy hello world to clipboard"        →  Writes to clipboard
"Read my notes.txt"                    →  Reads from Desktop/Documents
"Summarise my resume.pdf"              →  PDF text extraction + summary
```

### 😄 Fun & Personality
```
"Tell me a joke"       →  Live dad jokes from icanhazdadjoke.com
"What can you do"      →  Full capability list
"Introduce yourself"   →  JARVIS-style introduction
"How are you"          →  "Fully operational and at your disposal, Sir."
"Thank you"            →  "My pleasure."
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INTERACTION LAYER                               │
│              Microphone · Wake Word · Hand Gestures · Face              │
└──────────┬────────────────────┬────────────────────┬────────────────────┘
           │                   │                     │
    ┌──────▼──────┐   ┌────────▼────────┐   ┌───────▼──────────┐
    │   Voice STT  │   │ Gesture Engine  │   │  Face Auth       │
    │ Google/Whisper│  │ MediaPipe Tasks │   │ face_recognition │
    └──────┬──────┘   │  (Tasks API)    │   │  + MediaPipe     │
           │           └────────┬────────┘   └───────┬──────────┘
           └──────────────┬─────┘                    │
                          ▼                           │
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT ENGINE                                    │
│   1. CAD detector   2. Code detector   3. Fast pattern match (30+)     │
│   4. LLM call (Gemini → Ollama → Web)  5. Action dispatch              │
└──────────┬───────────────────────────────────────────────┬─────────────┘
           │                                               │
    ┌──────▼──────────────────────────────────────────────▼──────┐
    │                      AI PROVIDERS                           │
    │  Gemini 2.0 Flash Lite  →  Ollama/Mistral  →  Wiki/DDG    │
    └──────────────────────────────┬──────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────┐
│                        ACTION ENGINE (35+ actions)                      │
│  Apps · Websites · System · Screen · Code · CAD · Tasks · Weather      │
│  Clipboard · Files · Math · Translation · Reminders · Gestures         │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │      │      │      │
  Windows  Chrome  pyttsx3  SQLite  build123d  MediaPipe  FastAPI  React
   APIs   Playwright  TTS   Memory   3D CAD    Gestures  WebSocket  UI
```

### Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 18 + Framer Motion | Holographic animated UI |
| **Desktop** | Electron 28 | Native app, system tray, frameless |
| **Backend** | FastAPI + Python 3.10 | REST API + WebSocket server |
| **Voice In** | SpeechRecognition + Whisper | Audio + transcription |
| **AI Primary** | Google Gemini 2.0 Flash Lite | Intelligence + code + vision |
| **AI Local** | Ollama + Mistral | Offline fallback LLM |
| **AI Free** | Wikipedia + DuckDuckGo | No-key knowledge base |
| **Gestures** | MediaPipe Tasks API | Hand tracking (21 landmarks) |
| **Face Auth** | face_recognition + dlib-bin | Biometric security |
| **3D CAD** | build123d | Parametric model generation |
| **Browser** | Playwright + Chromium | Real web automation |
| **TTS** | pyttsx3 / ElevenLabs | Voice output |
| **Memory** | SQLite | Persistent conversation + tasks |
| **Settings** | JSON | Runtime config without code changes |

---

## 📁 Project Structure

```
SGA_Assistant/
│
├── 📂 backend/                       # Python AI backend
│   ├── server.py                     # FastAPI + WebSocket (lifespan pattern)
│   ├── agent_engine.py               # 🧠 Main AI pipeline + pattern matching
│   ├── action_engine.py              # ⚡ 35+ voice-triggered actions
│   ├── voice_loop.py                 # 🎤 Crash-resistant voice thread
│   ├── gesture_engine.py             # 🖐️ MediaPipe Tasks API hand tracking
│   ├── auth.py                       # 🔐 Face biometric authentication
│   ├── cad_agent.py                  # 🧊 3D CAD model generation (build123d)
│   ├── browser_agent.py              # 🌐 Playwright real web browsing
│   ├── briefing.py                   # 🌅 Morning weather+news+tasks briefing
│   ├── speaker.py                    # 🔊 pyttsx3 / ElevenLabs TTS
│   ├── memory.py                     # 💾 SQLite memory + task list
│   ├── personality.py                # 🎭 JARVIS personality + prompts
│   ├── settings.py                   # ⚙️ Runtime settings loader
│   ├── web_agent.py                  # 🔍 Wikipedia + DuckDuckGo lookup
│   ├── connection.py                 # 🔗 Thread-safe WebSocket broadcast
│   ├── local_ai.py                   # 🤖 Local Ollama interface
│   ├── offline_ai.py                 # 📡 Rule-based offline fallback
│   └── __init__.py
│
├── 📂 frontend/                      # React UI
│   └── src/
│       ├── App.js                    # Main app, tabs, WebSocket, state
│       ├── JarvisCore.js             # ◉ Animated holographic orb
│       ├── VoiceOrb.js               # 🔵 Floating corner Alexa-style orb
│       ├── GestureOverlay.js         # 🖐️ Gesture indicator + reference card
│       ├── Waveform.js               # 〰️ Canvas waveform visualizer
│       ├── TaskPanel.js              # ✅ Voice-controlled task list UI
│       ├── CodeBlock.js              # 💻 Syntax-highlighted code renderer
│       ├── DashboardPanel.js         # 📊 System status panel
│       ├── IntelligencePanel.js      # 🧠 AI intent/action display
│       ├── MemoryPanel.js            # 🗂️ Conversation history log
│       └── TitleBar.js               # 🪟 Custom frameless window controls
│
├── 📂 electron/                      # Desktop app wrapper
│   ├── main.js                       # Window, tray, IPC management
│   └── preload.js                    # Secure context bridge
│
├── 📂 cad_models/                    # Generated STL files (auto-created)
│
├── .env                              # 🔑 API keys — NEVER commit
├── settings.json                     # ⚙️ Auto-created on first run
├── sga_memory.db                     # 💾 SQLite database
├── requirements.txt                  # Python dependencies
└── package.json                      # Node dependencies + npm scripts
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anaconda / Miniconda (recommended)
- Windows 10/11
- Webcam (for gesture control + face auth)
- Microphone

### Step 1 — Clone
```bash
git clone https://github.com/Unwilling-mcu/S.G.A-personal-Ai-assistant.git
cd S.G.A-personal-Ai-assistant
```

### Step 2 — Python environment
```bash
conda create -n sga python=3.10 -y
conda activate sga
pip install -r requirements.txt
```

### Step 3 — Computer vision (gesture + face auth)
```bash
pip install opencv-python mediapipe
pip install dlib-bin
pip install face-recognition --no-deps
pip install face-recognition-models click pillow numpy
```

### Step 4 — Browser automation
```bash
pip install playwright
playwright install chromium
```

### Step 5 — Optional features
```bash
pip install build123d          # 3D CAD model generation
pip install openai-whisper     # Better speech recognition (offline)
pip install pygetwindow        # App window switching
pip install pymupdf            # PDF file reading
```

### Step 6 — Frontend
```bash
cd frontend && npm install && cd ..
npm install --save-dev electron electron-builder concurrently
```

### Step 7 — API Keys
Create `.env` in the project root:
```env
GEMINI_API_KEY=your_gemini_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here   # optional
```

Get a free Gemini key: https://aistudio.google.com/app/apikey

### Step 8 — Run
```bash
# Terminal 1: Backend
uvicorn backend.server:app --reload

# Terminal 2: React UI
cd frontend && npm start

# Terminal 3: Electron app (wait for React to compile)
npm run electron
```

---

## ⚙️ Configuration — `settings.json`

Auto-created on first run. Edit without touching code:

```json
{
  "face_auth_enabled":   false,
  "wake_word_mode":      false,
  "wake_word":           "hey sga",
  "tts_engine":          "pyttsx3",
  "elevenlabs_voice_id": "21m00Tcm4TlvDq8ikWAM",
  "stt_engine":          "google",
  "whisper_model":       "base",
  "gemini_model":        "gemini-2.0-flash-lite",
  "user_name":           "Sir",
  "morning_briefing":    true,
  "default_city":        "Asansol"
}
```

| Key | Options | Effect |
|---|---|---|
| `tts_engine` | `"pyttsx3"` / `"elevenlabs"` | Switch voice quality |
| `stt_engine` | `"google"` / `"whisper"` | Switch speech recognition |
| `wake_word_mode` | `true` / `false` | Require wake word |
| `face_auth_enabled` | `true` / `false` | Biometric login |
| `morning_briefing` | `true` / `false` | Startup briefing |
| `default_city` | any city name | Weather location |
| `user_name` | your name | How S.G.A addresses you |

---

## 🎤 Voice Commands — Complete Reference

### Apps & System
```
open chrome / notepad / vs code / calculator / camera / task manager
open youtube / netflix / amazon / github / gmail / whatsapp / maps
volume up / down / mute
system info · battery level · what's running · kill [app]
lock screen · shutdown · restart my pc · cancel shutdown
```

### 🖐️ Gesture Control
```
enable gesture control / gesture mode / start gesture
disable gesture / gesture off
enable tracing / air drawing / start tracing
clear trace / erase drawing
```

### 🔐 Biometric
```
take reference photo            → registers your face
(enable face_auth in settings.json → active on next startup)
```

### Screen & Files
```
take a screenshot · what's on my screen
type [any text] · switch to [app name]
read my [filename] · summarise my [filename.pdf]
read my clipboard · copy [text] to clipboard
```

### Knowledge
```
tell me about [topic]           → Wikipedia
who is [person]                 → Wikipedia bio
weather in [city]               → real-time, free
latest [topic] news             → Google News headlines
what is [concept]               → AI explanation
tell me a joke
```

### 🔢 Math & Conversions (instant)
```
what is 25% of 2000             → 500
25 times 48                     → 1200
100 plus 200 / minus / divided by
convert 10 km to miles
convert 37 celsius to fahrenheit
convert 5 kg to pounds
```

### 🌍 Translation (40+ languages, free)
```
translate [text] to hindi / french / japanese / arabic / bengali...
```

### 💻 Code Generation
```
write a python [description]
write a c++ program to [description]
write a java class for [description]
create an html page with [description]
write a sql query to [description]
```

### 🧊 3D CAD Models
```
create a cube [W]cm by [H]cm by [D]cm
make a cylinder radius [R]cm height [H]cm
create a sphere radius [R]cm
design a phone stand [angle] degree angle
make a bracket [W]cm by [H]cm
create a box with a lid [W]cm by [D]cm
```

### ✅ Tasks
```
add task [name]
my tasks
complete task [number or name]
delete task [name]
clear completed tasks
```

### 🌐 Web Browsing
```
search youtube for [query]
search amazon for [product]
go to [website]
```

### Reminders
```
remind me in 10 minutes to drink water
remind me in 2 hours to call mom
```

### Settings (by voice)
```
enable / disable wake word
switch to elevenlabs / default voice
clear memory
```

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Voice recognition (Google STT + Whisper support)
- [x] JARVIS personality with wake word activation
- [x] Gemini 2.0 Flash Lite + Ollama + Wikipedia fallback chain
- [x] 35+ voice-triggered actions
- [x] Screenshot + Gemini Vision screen description
- [x] Real web browsing with Playwright
- [x] Code generation with syntax highlighting + Copy button
- [x] SQLite memory + voice-controlled task list
- [x] Morning briefing (weather + news + tasks)
- [x] Real-time weather (free, Open-Meteo)
- [x] Google News headlines (free, no key)
- [x] Translation (40+ languages, free, no key)
- [x] Math calculator + unit conversions (instant, offline)
- [x] Volume, clipboard, process management
- [x] ElevenLabs natural voice TTS support
- [x] Electron desktop app (frameless, system tray, auto-reconnect)
- [x] `settings.json` runtime configuration
- [x] Holographic React UI with tabs (Chat / Tasks / Memory)
- [x] Floating Alexa-style voice orb
- [x] **MediaPipe Tasks API gesture control** (7 gestures + air tracing)
- [x] **Face biometric authentication** (face_recognition + dlib-bin)
- [x] **3D CAD model generation** (build123d → STL export)
- [x] **Biometric app access control** (per-app authentication)
- [x] Gesture overlay UI with real-time gesture indicator
- [x] Cached Gemini client (reduced latency)
- [x] Incomplete expression detection (asks for clarification)

### 🔨 In Progress
- [ ] Whisper STT full polish
- [ ] ElevenLabs streaming audio playback
- [ ] 3D model viewer in UI (Three.js)
- [ ] Gesture model auto-download on first run

### 🔭 Planned — Phase 2: Advanced Vision
- [ ] Live screen monitoring — alert on specific events
- [ ] OCR from any screen region
- [ ] Object detection in screenshots
- [ ] QR code scanning via webcam
- [ ] Multi-monitor support

### 🔭 Planned — Phase 3: 3D Printing Pipeline
- [ ] OrcaSlicer integration — auto-slice after model creation
- [ ] 3D printer discovery (mDNS scan)
- [ ] Print job submission (Moonraker / OctoPrint / PrusaLink)
- [ ] Print progress tracking with webcam stream
- [ ] Model iteration: *"make the walls thicker"*

### 🔭 Planned — Phase 4: Home Automation
- [ ] TP-Link Kasa smart lights + plugs
- [ ] Home Assistant integration
- [ ] Scene control: *"movie mode"* → dim lights + open Netflix
- [ ] Morning / evening / sleep routines

### 🔭 Planned — Phase 5: Calendar & Productivity
- [ ] Google Calendar: *"What's my schedule tomorrow?"*
- [ ] Gmail reading + draft by voice
- [ ] Meeting transcription + summary
- [ ] Focus mode — block distracting sites on timer

### 🔭 Planned — Phase 6: Advanced AI
- [ ] Gemini Live API — zero-latency streaming voice
- [ ] Multi-modal: see screen + hear voice simultaneously
- [ ] Long-term memory across sessions
- [ ] Code execution — run generated code, return output
- [ ] Agent chains — autonomous multi-step tasks

### 🔭 Planned — Phase 7: Mobile
- [ ] React Native mobile app — remote access to home PC
- [ ] macOS + Linux support
- [ ] Remote access via secure tunnel

---

## 🛡️ Security & Privacy

| Aspect | Implementation |
|---|---|
| API Keys | `.env` file, gitignored |
| Face data | Processed locally, never uploaded |
| Conversation | Local SQLite only |
| No telemetry | Zero analytics or tracking |
| No cloud storage | Everything on your machine |

> ⚠️ **Never commit your `.env` file.** It is in `.gitignore` by default.

---

## 📦 Requirements

```
# Core
fastapi uvicorn python-dotenv requests

# Voice
SpeechRecognition pyttsx3 PyAudio

# AI
google-genai

# Actions
pyautogui psutil pyperclip

# Computer Vision
opencv-python mediapipe dlib-bin face-recognition

# Browser
playwright

# Optional
openai-whisper    # better STT
pymupdf           # PDF reading
build123d         # 3D CAD
pygetwindow       # window switching
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m "feat: add amazing feature"`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Dev Tips
- Run `uvicorn backend.server:app --reload` — see live logs in terminal
- All features toggleable in `settings.json` — no code changes needed
- `sga_memory.db` — inspect with DB Browser for SQLite
- `cad_models/` — open `.stl` files with Microsoft 3D Viewer

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**Built by [Unwilling-mcu](https://github.com/Unwilling-mcu)**

*Inspired by [ADA v2](https://github.com/nazirlouis/ada_v2)*

⭐ **Star this repo if S.G.A impresses you!**

</div>
