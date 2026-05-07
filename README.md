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
[![Groq](https://img.shields.io/badge/Groq-LPU_AI-F55036?style=flat&logo=groq&logoColor=white)](https://console.groq.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks_API-FF6F00?style=flat&logo=google&logoColor=white)](https://mediapipe.dev)
[![SQLite](https://img.shields.io/badge/SQLite-Memory-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)]()
[![GitHub](https://img.shields.io/badge/GitHub-Unwilling--mcu-181717?style=flat&logo=github)](https://github.com/Unwilling-mcu/S.G.A-personal-Ai-assistant)

<br/>

> *"Good morning, Sir. All systems are operational. Weather in Asansol: Clear sky, 28°C. You have 3 pending tasks."*

<br/>

**S.G.A** (Smart General Assistant) is a fully voice-controlled personal AI desktop assistant built entirely from scratch — inspired by JARVIS from Iron Man and ADA v2. It runs as a real Electron desktop app, listens 24/7, and can control your PC, browse the web, write code, manage tasks, describe your screen, translate languages, perform gesture control, generate 3D CAD models, authenticate with your face, and much more — all through natural voice commands.

[**Features**](#-features) · [**Architecture**](#-architecture) · [**Installation**](#-installation) · [**Commands**](#-voice-commands) · [**Roadmap**](#-roadmap) · [**License**](#-license)

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
YOU  "create a cylinder radius 3cm height 8cm"
AI   3D model created: cylinder_r30_h80_1.stl (42 KB). Saved to cad_models folder.
────────────────────────────────────────────────────────────
```

---

## ✨ Features

### 🎙️ Voice & Intelligence
| Feature | Description |
|---|---|
| Always-on voice loop | Listens continuously — zero clicks needed |
| Wake word mode | Say *"Hey S.G.A"* or *"Jarvis"* to activate |
| Google Speech STT | Fast cloud-based recognition |
| Whisper STT (optional) | Local, highly accurate, works fully offline |
| JARVIS personality | Calm, witty, addresses you as *"Sir"* |
| SQLite memory | Persistent across restarts, 200 interactions |
| Context awareness | Uses recent conversation in every reply |
| Morning briefing | Weather + news + tasks read aloud on startup |
| Voice-controlled settings | Change features without touching code |

### 🤖 AI Provider Chain (auto-fallback)
```
Groq LLM (fastest, 14,400 free/day)
  → Gemini 2.0 Flash Lite (Google)
    → Ollama / Mistral (local, offline)
      → Wikipedia + DuckDuckGo (always free)
```
Most commands work **100% free with no API key** via fast pattern matching.

### 🖐️ Gesture Control *(MediaPipe Tasks API v0.10+)*
Full contactless PC control via webcam hand tracking — 21 landmark detection:

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

**Air tracing** — point your index finger to draw on screen in real-time.
**Activate by voice:** *"enable gesture control"* or *"gesture mode"*

### 🔐 Face Biometric Authentication
- **High accuracy** — `face_recognition` + `dlib-bin`: recognises *you specifically*
- **Presence mode** — MediaPipe fallback: any face unlocks
- **App-level access control** — protected apps require re-auth every 5 minutes
- **Voice setup:** Say *"take reference photo"* to register your face

### 🧊 3D CAD Model Generation *(build123d)*
Voice → parametric 3D model → STL file ready for 3D printing:

```
"Create a cube 5cm by 5cm by 5cm"          → cube_50x50x50_1.stl
"Make a cylinder radius 3cm height 8cm"    → cylinder_r30_h80_2.stl
"Design a phone stand 60 degree angle"     → phone_stand_60deg_3.stl
"Create a sphere radius 2cm"               → sphere_r20_4.stl
"Make a bracket 10cm by 5cm"              → bracket_100x50_5.stl
"Create a box with a lid 8cm by 6cm"      → box_with_lid_6.stl
```
Complex models use Groq/Gemini to write `build123d` Python code and execute it safely.
Open STL files in **Microsoft 3D Viewer** (built into Windows) to preview.

### 💻 PC Control
```
open chrome / notepad / vs code / calculator / camera / task manager
open youtube / netflix / amazon / github / gmail / whatsapp / maps / spotify
volume up / down / mute
take a screenshot · what's on my screen (Gemini Vision)
type [text] · switch to [app] · lock screen
shutdown / restart / cancel shutdown · kill [process]
```

### 🧠 Knowledge & Information
```
tell me about [topic]      → Wikipedia summary
who is [person]            → Wikipedia biography
weather in [city]          → real-time, free (Open-Meteo)
latest [topic] news        → Google News RSS, free
search [query]             → Google in Chrome
```

### 🔢 Math, Conversions & Translation *(instant, offline)*
```
"what is 25% of 2000"              → The answer is 500
"25 times 48"                      → The answer is 1200
"convert 10 km to miles"           → 6.21 miles
"convert 37 celsius to fahrenheit" → 98.6°F
"translate hello to Hindi"         → नमस्ते
"translate good morning to Japanese" → おはようございます
```
Supports 40+ languages. Conversions: km/miles, kg/lbs, °C/°F, m/feet, cm/inches.

### 💻 Code Generation *(Groq/Gemini powered)*
Syntax-highlighted code with Copy button:
```
"write a Python function to sort a list"
"write a C++ bubble sort program"
"write a Java calculator class"
"create an HTML login page"
"write a SQL query to find duplicates"
"write a Bash script to backup files"
```

### ✅ Voice Task Manager
```
"add task buy groceries"     → Task added
"my tasks"                   → lists all pending + done
"complete task 1"            → marked done
"delete task groceries"
"clear completed tasks"
```
Stored in SQLite — persists between sessions. Visible in **Tasks tab**.

### 🌐 Real Web Browsing *(Playwright)*
```
"search YouTube for Python tutorials"   → returns top video titles
"search Amazon for wireless headphones" → products + prices
"go to timesofindia.com"               → opens and reads page
```

### 🔧 System Information
```
"system info"     → CPU%, RAM used, disk space
"battery level"   → %, charging status, time remaining
"what's running"  → top CPU-consuming processes
```

### 📋 Clipboard & Files
```
"read my clipboard" · "copy [text] to clipboard"
"read my notes.txt" · "summarise my resume.pdf"
```

### ⏰ Reminders
```
"remind me in 10 minutes to drink water"
"remind me in 2 hours to call mom"
```

### 😄 Fun & Personality
```
"tell me a joke"       → live dad jokes from internet
"what can you do"      → full capability list
"introduce yourself"   → JARVIS-style intro
"how are you"          → "Fully operational, Sir."
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INTERACTION LAYER                               │
│         Microphone  ·  Wake Word  ·  Hand Gestures  ·  Face Auth       │
└──────────┬──────────────────┬──────────────────────┬────────────────────┘
           │                  │                       │
    ┌──────▼──────┐  ┌────────▼────────┐   ┌────────▼──────────┐
    │   STT Engine │  │ Gesture Engine  │   │   Face Auth       │
    │Google/Whisper│  │MediaPipe Tasks  │   │ face_recognition  │
    └──────┬──────┘  │  (21 landmarks) │   │ + MediaPipe       │
           │          └────────┬────────┘   └────────┬──────────┘
           └──────────────┬────┘                     │
                          ▼                           │
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT ENGINE                                    │
│  1. CAD detector  2. Code detector  3. Fast patterns (35+ actions)     │
│  4. LLM call: Groq → Gemini → Ollama → Wikipedia/DDG                  │
└──────────┬──────────────────────────────────────────┬───────────────────┘
           │                                           │
    ┌──────▼──────────────────────────────────────────▼──────┐
    │                    AI PROVIDERS                          │
    │  Groq LLM (14,400/day free, fastest)                    │
    │    → Gemini 2.0 Flash Lite                              │
    │      → Ollama / Mistral (offline)                       │
    │        → Wikipedia + DuckDuckGo (always free)           │
    └──────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────┐
│                     ACTION ENGINE (35+ actions)                         │
│  Apps · System · Screen · Code · 3D CAD · Tasks · Weather · Files     │
│  Math · Translation · Clipboard · Reminders · Gestures · Biometric    │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │      │      │      │
  Windows  Chrome  SQLite  pyttsx3  build123d  MediaPipe  FastAPI   React
   APIs   Playwright Memory  /ElevenLabs 3D CAD  Gestures  WebSocket   UI
```

### Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 18 + Framer Motion | Holographic animated UI |
| **Desktop** | Electron 28 | Native app, system tray, frameless window |
| **Backend** | FastAPI + Python 3.10 | REST API + WebSocket server |
| **Voice In** | SpeechRecognition + Whisper | Audio capture + transcription |
| **AI Primary** | Groq LLM (Llama 3.3 70B) | Fastest inference, 14,400 free/day |
| **AI Secondary** | Google Gemini 2.0 Flash Lite | Backup LLM + Vision |
| **AI Local** | Ollama + Mistral | Fully offline fallback |
| **AI Free** | Wikipedia + DuckDuckGo | Zero-cost knowledge base |
| **Gestures** | MediaPipe Tasks API | 21-landmark hand tracking |
| **Face Auth** | face_recognition + dlib-bin | Biometric security |
| **3D CAD** | build123d | Parametric model generation → STL |
| **Browser** | Playwright + Chromium | Real web automation |
| **TTS** | pyttsx3 / ElevenLabs | Voice output |
| **Memory** | SQLite | Persistent conversations + tasks |
| **Settings** | JSON | Runtime config, no code changes |

---

## 📁 Project Structure

```
SGA_Assistant/
│
├── 📂 backend/                       # Python AI backend
│   ├── server.py                     # FastAPI + WebSocket server
│   ├── agent_engine.py               # 🧠 Main AI pipeline + 35+ patterns
│   ├── action_engine.py              # ⚡ All voice-triggered actions
│   ├── voice_loop.py                 # 🎤 Crash-resistant voice thread
│   ├── gesture_engine.py             # 🖐️ MediaPipe Tasks API (auto-detects version)
│   ├── auth.py                       # 🔐 Face biometric + app access control
│   ├── cad_agent.py                  # 🧊 3D CAD generation (build123d → STL)
│   ├── browser_agent.py              # 🌐 Playwright real web browsing
│   ├── briefing.py                   # 🌅 Morning weather + news + tasks
│   ├── speaker.py                    # 🔊 pyttsx3 / ElevenLabs TTS
│   ├── memory.py                     # 💾 SQLite memory + task manager
│   ├── personality.py                # 🎭 JARVIS personality + system prompts
│   ├── settings.py                   # ⚙️ Runtime settings from settings.json
│   ├── web_agent.py                  # 🔍 Wikipedia + DuckDuckGo lookup
│   ├── connection.py                 # 🔗 Thread-safe WebSocket broadcast
│   ├── local_ai.py                   # 🤖 Ollama local LLM interface
│   └── offline_ai.py                 # 📡 Rule-based offline fallback
│
├── 📂 frontend/                      # React UI
│   └── src/
│       ├── App.js                    # Main app, tabs, WebSocket, state
│       ├── JarvisCore.js             # ◉ Animated holographic orb
│       ├── VoiceOrb.js               # 🔵 Floating Alexa-style corner orb
│       ├── GestureOverlay.js         # 🖐️ Gesture indicator + reference card
│       ├── Waveform.js               # 〰️ Canvas audio waveform
│       ├── TaskPanel.js              # ✅ Voice task list UI
│       ├── CodeBlock.js              # 💻 Syntax-highlighted code renderer
│       ├── DashboardPanel.js         # 📊 System status panel
│       ├── IntelligencePanel.js      # 🧠 Intent/action display
│       ├── MemoryPanel.js            # 🗂️ Conversation history log
│       └── TitleBar.js               # 🪟 Custom frameless window controls
│
├── 📂 electron/                      # Desktop wrapper
│   ├── main.js                       # Window, tray, IPC
│   └── preload.js                    # Secure context bridge
│
├── 📂 cad_models/                    # Generated STL files (auto-created)
│
├── .gitignore                        # Excludes .env, node_modules, large files
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
├── package.json                      # Node dependencies + npm scripts
└── settings.json                     # Runtime config (auto-created)
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anaconda / Miniconda
- Windows 10/11
- Webcam + Microphone

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

### Step 3 — Computer vision
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
pip install openai-whisper     # Better offline speech recognition
pip install pygetwindow        # Precise app window switching
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
GROQ_API_KEY=your_groq_key_here          # FREE — get at console.groq.com
GEMINI_API_KEY=your_gemini_key_here      # optional backup
ELEVENLABS_API_KEY=your_key_here         # optional natural voice
```

**Get free Groq key (recommended):** https://console.groq.com — 14,400 requests/day free

**Get free Gemini key (backup):** https://aistudio.google.com/app/apikey

### Step 8 — Run
```bash
# Terminal 1: Backend
uvicorn backend.server:app --reload

# Terminal 2: React UI
cd frontend && npm start

# Terminal 3: Electron (wait for React to compile first)
npm run electron
```

---

## ⚙️ Configuration — `settings.json`

Auto-created on first run. Edit anytime without touching code:

```json
{
  "face_auth_enabled":   false,
  "wake_word_mode":      false,
  "wake_word":           "hey sga",
  "tts_engine":          "pyttsx3",
  "elevenlabs_voice_id": "21m00Tcm4TlvDq8ikWAM",
  "stt_engine":          "google",
  "whisper_model":       "base",
  "groq_model":          "llama-3.3-70b-versatile",
  "gemini_model":        "gemini-2.0-flash-lite",
  "user_name":           "Sir",
  "morning_briefing":    true,
  "default_city":        "Asansol"
}
```

| Key | Options | Effect |
|---|---|---|
| `groq_model` | `llama-3.3-70b-versatile` / `gemma2-9b-it` / `mixtral-8x7b-32768` | Switch Groq model |
| `tts_engine` | `pyttsx3` / `elevenlabs` | Switch voice quality |
| `stt_engine` | `google` / `whisper` | Switch speech recognition |
| `wake_word_mode` | `true` / `false` | Require wake word activation |
| `face_auth_enabled` | `true` / `false` | Biometric login on startup |
| `morning_briefing` | `true` / `false` | Startup weather+news+tasks |
| `default_city` | any city name | Weather location |
| `user_name` | your name | How S.G.A addresses you |

---

## 🎤 Voice Commands — Complete Reference

### 🖥️ Apps & System
```
open chrome / notepad / vs code / calculator / camera / task manager
open youtube / netflix / amazon / github / gmail / whatsapp / maps / spotify
volume up / down / mute
system info · battery level · what's running
kill [app name] · lock screen
shutdown / restart my pc · cancel shutdown
```

### 🖐️ Gesture Control
```
enable gesture control / gesture mode / start gesture
disable gesture / gesture off
enable tracing / air drawing
clear trace / erase drawing
```

### 🔐 Biometric
```
take reference photo          → registers your face for auth
(set face_auth_enabled: true in settings.json to activate)
```

### 📸 Screen & Files
```
take a screenshot
what's on my screen           → Gemini Vision describes it
type [any text]
switch to [app name]
read my [filename.txt / filename.pdf]
read my clipboard · copy [text] to clipboard
```

### 🧠 Knowledge
```
tell me about [topic]         → Wikipedia
who is [person]               → Wikipedia bio
weather in [city]             → real-time, free
latest [topic] news           → Google News
what is [concept]             → AI explanation
tell me a joke
```

### 🔢 Math & Conversions *(instant, offline)*
```
what is 25% of 2000           → 500
25 times 48                   → 1200
100 plus / minus / divided by
convert 10 km to miles
convert 37 celsius to fahrenheit
convert 5 kg to pounds
```

### 🌍 Translation *(40+ languages, free)*
```
translate [text] to hindi / french / japanese / arabic / bengali / spanish...
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
go to [any website]
```

### ⏰ Reminders
```
remind me in [N] minutes to [task]
remind me in [N] hours to [task]
```

### ⚙️ Settings by Voice
```
enable / disable wake word
switch to elevenlabs / default voice
clear memory
```

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Voice recognition (Google STT + Whisper support)
- [x] JARVIS personality with wake word
- [x] **Groq LLM** — fastest AI, 14,400 free requests/day
- [x] Gemini 2.0 Flash Lite + Ollama + Wikipedia fallback chain
- [x] 35+ voice-triggered actions
- [x] Screenshot + Gemini Vision screen description
- [x] Real web browsing (Playwright)
- [x] Code generation with syntax highlighting + Copy button
- [x] SQLite memory + voice-controlled task manager
- [x] Morning briefing (weather + news + tasks)
- [x] Real-time weather (free, Open-Meteo, no key)
- [x] Google News headlines (free, no key)
- [x] Translation (40+ languages, free, no key)
- [x] Math calculator + unit conversions (instant, offline)
- [x] ElevenLabs natural voice TTS
- [x] Electron desktop app (frameless, system tray)
- [x] `settings.json` runtime configuration
- [x] Holographic React UI (Chat / Tasks / Memory tabs)
- [x] Floating Alexa-style voice orb
- [x] **MediaPipe Tasks API gesture control** (7 gestures + air tracing)
- [x] **Face biometric authentication** (face_recognition + dlib-bin)
- [x] **3D CAD model generation** (build123d → STL export)
- [x] Biometric app access control
- [x] Gesture overlay UI with real-time indicator
- [x] Incomplete expression detection (asks for clarification)
- [x] Cached LLM clients (reduced latency)

### 🔨 In Progress
- [ ] 3D model viewer in UI (Three.js)
- [ ] Whisper STT full polish
- [ ] ElevenLabs streaming playback

### 🔭 Planned — Phase 2: Advanced Vision
- [ ] Live screen monitoring + event alerts
- [ ] OCR from any screen region
- [ ] Object detection in screenshots
- [ ] QR code scanning via webcam

### 🔭 Planned — Phase 3: 3D Printing Pipeline
- [ ] OrcaSlicer auto-slicing after model creation
- [ ] 3D printer network discovery (mDNS)
- [ ] Print job submission (Moonraker / OctoPrint / PrusaLink)
- [ ] Print progress tracking with webcam
- [ ] Iterative model refinement: *"make the walls thicker"*

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
- [ ] Multi-modal: sees screen + hears voice simultaneously
- [ ] Long-term memory across sessions
- [ ] Code execution — run generated code, return output
- [ ] Autonomous agent chains — multi-step tasks

### 🔭 Planned — Phase 7: Mobile & Cross-Platform
- [ ] React Native mobile app (remote access to home PC)
- [ ] macOS + Linux support
- [ ] Remote access via secure tunnel

---

## 🛡️ Security & Privacy

| Aspect | Implementation |
|---|---|
| API Keys | `.env` file, gitignored — never committed |
| Face data | Processed 100% locally, never uploaded |
| Conversations | Local SQLite only — no cloud sync |
| No telemetry | Zero analytics or tracking of any kind |
| No cloud storage | Everything stays on your machine |

> ⚠️ **Never commit your `.env` file.** It is excluded by `.gitignore` by default.

---

## 📦 Full Requirements

```bash
# Core backend
fastapi uvicorn python-dotenv requests

# AI providers
groq                    # Groq API (recommended — fastest + most free)
google-genai            # Gemini API (backup)

# Voice
SpeechRecognition pyttsx3 PyAudio

# Actions & system
pyautogui psutil pyperclip

# Computer vision
opencv-python mediapipe
dlib-bin
face-recognition

# Browser automation
playwright

# Optional
openai-whisper          # better STT
pymupdf                 # PDF reading
build123d               # 3D CAD
pygetwindow             # window switching
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m "feat: add amazing feature"`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Tips
- `uvicorn backend.server:app --reload` — live backend logs in terminal
- All features toggled in `settings.json` — no code edits needed
- `sga_memory.db` — inspect with **DB Browser for SQLite**
- `cad_models/` — open `.stl` with **Microsoft 3D Viewer** (built-in Windows)
- Say *"what can you do"* to get the full capability list at any time

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by [Sanchayan Garai](https://github.com/Unwilling-mcu)**

*Inspired by [ADA v2](https://github.com/nazirlouis/ada_v2) — pushing personal AI further*

⭐ **Star this repo if S.G.A impresses you!**

[![GitHub stars](https://img.shields.io/github/stars/Unwilling-mcu/S.G.A-personal-Ai-assistant?style=social)](https://github.com/Unwilling-mcu/S.G.A-personal-Ai-assistant)
[![GitHub forks](https://img.shields.io/github/forks/Unwilling-mcu/S.G.A-personal-Ai-assistant?style=social)](https://github.com/Unwilling-mcu/S.G.A-personal-Ai-assistant/fork)

</div>