import os
import re
import logging
from typing import Optional, Callable
from dotenv import load_dotenv

load_dotenv()

from backend.action_engine import execute_action
from backend.web_agent import get_web_answer
from backend.memory import save_memory, get_recent_context
from backend.personality import (
    jarvis_llm_system_prompt, wrap_answer,
    search_intro, acknowledgement, error_response
)

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
OLLAMA_URL     = "http://localhost:11434/api/generate"
OLLAMA_MODEL   = "mistral"
OLLAMA_TIMEOUT = 45

# Cached clients — created once, reused every call
_gemini_client = None
_groq_client   = None


def _get_groq_client():
    global _groq_client
    if _groq_client is None and GROQ_API_KEY:
        try:
            from groq import Groq
            _groq_client = Groq(api_key=GROQ_API_KEY)
            logger.info("Groq client initialised")
        except ImportError:
            logger.warning("groq not installed — run: pip install groq")
        except Exception as e:
            logger.error("Groq init failed: %s", e)
    return _groq_client


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None and GEMINI_API_KEY:
        try:
            from google import genai
            _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
            logger.info("Gemini client initialised")
        except Exception as e:
            logger.error("Gemini init failed: %s", e)
    return _gemini_client


# ── All valid actions S.G.A can perform ──────────────────────────────────────
VALID_ACTIONS = {
    # Apps & system
    "open_chrome","open_notepad","open_camera","open_vscode",
    "open_calculator","open_taskmanager","open_website",
    "switch_to_app","lock_screen","shutdown","restart","cancel_shutdown",
    # Screen
    "take_screenshot","describe_screen","type_text","click_mouse","move_mouse",
    # Volume & clipboard
    "volume_up","volume_down","volume_mute","read_clipboard","write_clipboard",
    # System info
    "get_system_info","get_battery","list_processes","kill_process",
    # Knowledge
    "search_google","get_weather","get_news","calculate",
    "convert_units","translate","wiki_summary","tell_joke",
    # Files & reminders
    "set_reminder","read_file",
    # Code & CAD
    "generate_code","create_3d_model",
    # Gesture & biometric
    "enable_gesture","disable_gesture","enable_tracing","clear_trace",
    "take_reference_photo",
    # Control tokens
    "final","none"
}


# ── Fast pattern list — zero LLM latency ─────────────────────────────────────
PATTERNS = [
    # Screen
    (["what's on my screen","describe my screen","what do you see",
      "look at my screen","describe screen"],          "describe_screen",  None),
    (["take a screenshot","screenshot"],               "take_screenshot",  None),

    # Volume
    (["volume up","louder","increase volume"],         "volume_up",        None),
    (["volume down","quieter","lower volume"],         "volume_down",      None),
    (["mute","unmute","silence"],                      "volume_mute",      None),

    # System
    (["system info","cpu usage","ram usage","memory usage","how is my computer"],
                                                       "get_system_info",  None),
    (["battery","battery level","how much battery"],   "get_battery",      None),
    (["list processes","running apps","what's running","what is running"],
                                                       "list_processes",   None),
    (["lock screen","lock my screen","lock computer"], "lock_screen",      None),
    (["shutdown","shut down my pc","turn off my pc"],  "shutdown",         None),
    (["restart my pc","reboot my pc"],                 "restart",          None),
    (["cancel shutdown"],                              "cancel_shutdown",  None),

    # Apps
    (["open chrome"],                                  "open_chrome",      None),
    (["open notepad"],                                 "open_notepad",     None),
    (["open camera"],                                  "open_camera",      None),
    (["open calculator","open calc"],                  "open_calculator",  None),
    (["open task manager","task manager"],             "open_taskmanager", None),
    (["open vs code","open vscode","open code"],       "open_vscode",      None),

    # Clipboard
    (["what's in my clipboard","read clipboard","clipboard content"],
                                                       "read_clipboard",   None),

    # Joke
    (["tell me a joke","tell a joke","say a joke","make me laugh","joke"],
                                                       "tell_joke",        None),

    # Popular websites
    (["open youtube"],   "open_website", lambda _: "youtube.com"),
    (["open google"],    "open_website", lambda _: "google.com"),
    (["open facebook"],  "open_website", lambda _: "facebook.com"),
    (["open instagram"], "open_website", lambda _: "instagram.com"),
    (["open twitter","open x dot com"], "open_website", lambda _: "twitter.com"),
    (["open github"],    "open_website", lambda _: "github.com"),
    (["open netflix"],   "open_website", lambda _: "netflix.com"),
    (["open spotify"],   "open_website", lambda _: "open.spotify.com"),
    (["open amazon"],    "open_website", lambda _: "amazon.in"),
    (["open whatsapp"],  "open_website", lambda _: "web.whatsapp.com"),
    (["open gmail"],     "open_website", lambda _: "mail.google.com"),
    (["open maps","google maps"], "open_website", lambda _: "maps.google.com"),

    # Gesture control
    (["enable gesture control","start gesture","activate gesture",
      "gesture mode on","enable gesture mode","gesture mode",
      "start gesture mode","hand gesture","turn on gesture"],
                                                       "enable_gesture",   None),
    (["disable gesture","stop gesture","gesture off",
      "disable gesture mode","turn off gesture"],       "disable_gesture",  None),
    (["enable tracing","start tracing","air drawing",
      "finger tracing","start drawing","draw mode"],
                                                       "enable_tracing",   None),
    (["clear trace","erase trace","clear drawing",
      "erase drawing","reset trace"],                  "clear_trace",      None),

    # Biometric
    (["take reference photo","setup face auth","register my face",
      "take my photo for auth"],                       "take_reference_photo", None),
]


# ── Keyword trigger lists ─────────────────────────────────────────────────────
CAD_TRIGGERS = [
    "create a 3d model","make a 3d model","design a","create a cube",
    "make a cylinder","create a sphere","generate a 3d","make a 3d",
    "design me a","cad model","3d print","stl file",
    "create a box","make a bracket","phone stand","make a cone",
    "parametric","build a model","create a shape","make a sphere",
]

CODE_TRIGGERS = [
    "write a","write me","generate code","code for","create a program",
    "make a script","python script","java program","c++ program","c program",
    "html page","write code","give me code","write function","write class",
    "write a function","write a class","create function","build a program",
    "write algorithm","write a script",
]


def _is_cad_request(text: str) -> bool:
    t = text.lower()
    return any(tr in t for tr in CAD_TRIGGERS)

def _is_code_request(text: str) -> bool:
    t = text.lower()
    return any(tr in t for tr in CODE_TRIGGERS)


# ── Fast pattern matching (no LLM) ────────────────────────────────────────────
def _quick_action(text: str) -> Optional[tuple]:
    """Returns (action, value) if a fast pattern matches, else None."""
    t = text.lower().strip()

    # Weather
    if any(w in t for w in ["weather","temperature","forecast","how hot","how cold"]):
        m = re.search(r"(?:weather|temperature|forecast)\s+(?:in|at|for)?\s*([a-zA-Z\s]+)", t)
        city = m.group(1).strip() if m else "Asansol"
        return ("get_weather", city)

    # News
    if any(w in t for w in ["news","headlines","latest news","what's happening"]):
        m = re.search(r"(?:news|headlines)\s+(?:about|on|for)?\s*([a-zA-Z\s]+)", t)
        topic = m.group(1).strip() if m else "technology"
        return ("get_news", topic)

    # Math
    if re.search(r"\d+\s*[+\-*/]\s*\d+", t) or "% of" in t or \
       any(w in t for w in ["calculate","what is","whats","compute"]):
        expr = re.sub(r"(?:calculate|what is|whats|compute)\s*", "", t).strip()
        if expr and re.search(r"\d", expr):
            return ("calculate", expr)

    # Unit conversion
    if re.search(r"\d+\s*(?:km|miles?|kg|lbs?|°?[cf]|celsius|fahrenheit|m\b|feet?|inch|cm|litre?s?)", t):
        if any(w in t for w in ["to","in","convert"]):
            return ("convert_units", t)

    # Translation
    if t.startswith("translate") or re.search(
        r"\bto\s+(?:hindi|spanish|french|german|japanese|chinese|arabic|bengali|tamil|telugu|urdu|russian|italian|korean)\b", t
    ):
        return ("translate", text)

    # Wikipedia
    if t.startswith("tell me about") or t.startswith("who is") or t.startswith("what is"):
        topic = re.sub(r"^(?:tell me about|who is|what is)\s+", "", t).strip()
        if topic and len(topic) > 2:
            return ("wiki_summary", topic)

    # Reminder
    if any(w in t for w in ["remind me","set a reminder","alarm in"]):
        return ("set_reminder", text)

    # File reading
    if any(w in t for w in ["read my","read file","open file","summarise my","summarize my"]):
        m = re.search(r"(?:read|open|summarise|summarize)\s+(?:my\s+)?(.+)", t)
        return ("read_file", m.group(1).strip() if m else "")

    # Type text
    if t.startswith("type "):
        return ("type_text", t[5:].strip())

    # Kill process
    if "kill " in t or ("close " in t and len(t.split()) <= 4):
        m = re.search(r"(?:kill|close)\s+(.+)", t)
        if m:
            return ("kill_process", m.group(1).strip())

    # Switch to app
    if "switch to " in t or "bring up " in t:
        m = re.search(r"(?:switch to|bring up)\s+(.+)", t)
        if m:
            return ("switch_to_app", m.group(1).strip())

    # Copy to clipboard
    if "copy " in t and "clipboard" in t:
        m = re.search(r"copy\s+(.+?)\s+to clipboard", t)
        if m:
            return ("write_clipboard", m.group(1).strip())

    # Search
    if t.startswith("search ") or "search for " in t:
        query = re.sub(r"^search for |^search ", "", t, flags=re.IGNORECASE).strip()
        if query and len(query) > 2:
            return ("search_google", query)

    # Open website / go to URL
    if any(p in t for p in ["go to ","visit ","open "]):
        m = re.search(r"(?:go to|visit|open)\s+([\w\.\-]+(?:\.[a-z]{2,}))", t)
        if m:
            return ("open_website", m.group(1))

    # Static patterns list
    for triggers, action, val_fn in PATTERNS:
        if any(tr in t for tr in triggers):
            return (action, val_fn(t) if val_fn else None)

    return None


# ── LLM callers ───────────────────────────────────────────────────────────────

def _ollama_is_running() -> bool:
    try:
        import requests as req
        req.get("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


def _call_groq(prompt: str, system: str = None, max_tokens: int = 600) -> Optional[str]:
    """
    Groq API — fastest LLM in the world (LPU hardware).
    Free tier: 14,400 requests/day. Get key: https://console.groq.com
    Models: llama-3.3-70b-versatile, gemma2-9b-it, mixtral-8x7b-32768
    """
    client = _get_groq_client()
    if not client:
        return None
    try:
        from backend.settings import get
        model = get("groq_model", "llama-3.3-70b-versatile")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system or jarvis_llm_system_prompt()},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        text = response.choices[0].message.content
        return text.strip() if text else None
    except Exception as e:
        logger.error("Groq error: %s", e)
        return None


def _call_gemini(prompt: str, system: str = None, max_tokens: int = 600) -> Optional[str]:
    client = _get_gemini_client()
    if not client:
        return None
    try:
        from google.genai import types
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system or jarvis_llm_system_prompt(),
                max_output_tokens=max_tokens,
                temperature=0.7,
            )
        )
        return response.text.strip() if response.text else None
    except Exception as e:
        logger.error("Gemini error: %s", e)
        return None


def _call_ollama(prompt: str) -> Optional[str]:
    if not _ollama_is_running():
        return None
    try:
        import requests
        res = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL,
                  "prompt": f"{jarvis_llm_system_prompt()}\n\nUser: {prompt}",
                  "stream": False},
            timeout=OLLAMA_TIMEOUT
        )
        res.raise_for_status()
        return res.json().get("response", "").strip() or None
    except Exception as e:
        logger.warning("Ollama error: %s", e)
        return None


def _call_llm(prompt: str) -> Optional[str]:
    """
    Priority: Groq (fastest, 14,400/day free)
           → Gemini (slower free tier)
           → Ollama (local, offline)
           → None  (falls back to Wikipedia/DDG)
    """
    # 1. Groq — fastest and most generous free tier
    if GROQ_API_KEY:
        logger.info("Using Groq API")
        r = _call_groq(prompt)
        if r:
            return r
        logger.warning("Groq failed — trying Gemini")

    # 2. Gemini fallback
    if GEMINI_API_KEY:
        logger.info("Using Gemini API")
        r = _call_gemini(prompt)
        if r:
            return r
        logger.warning("Gemini failed — trying Ollama")

    # 3. Local Ollama last resort
    return _call_ollama(prompt)


# ── Code generation ───────────────────────────────────────────────────────────
CODE_SYSTEM = """You are S.G.A, an expert coding assistant.
Generate clean, well-commented, production-quality code.
Format: brief explanation, then code block with language tag, then usage note.
Supported: Python, C, C++, Java, JavaScript, HTML, CSS, SQL, Bash."""

def generate_code(request: str) -> str:
    # Groq first — fastest responses
    if GROQ_API_KEY:
        r = _call_groq(request, system=CODE_SYSTEM, max_tokens=1500)
        if r:
            return r
    # Gemini fallback
    if GEMINI_API_KEY:
        r = _call_gemini(request, system=CODE_SYSTEM, max_tokens=1500)
        if r:
            return r
    # Local Ollama last
    if _ollama_is_running():
        return _call_ollama(f"Generate code for: {request}") or "LLM unavailable."
    return "Code generation requires GROQ_API_KEY, GEMINI_API_KEY, or Ollama running."


# ── Helpers ───────────────────────────────────────────────────────────────────

def _safe_broadcast(broadcast, msg):
    if broadcast:
        try:
            broadcast(msg)
        except Exception:
            pass

def _build_prompt(user_input: str) -> str:
    recent = get_recent_context(3)
    ctx = ""
    if recent:
        ctx = "\n\nRecent conversation:\n"
        for e in recent:
            ctx += f"User: {e.get('user','')}\nS.G.A: {e.get('ai','')}\n"
    return f"{ctx}\nUser: {user_input}"

def _parse_response(text: str) -> dict:
    r = {"action": "", "input": ""}
    for line in text.strip().split("\n"):
        line = line.strip()
        if line.upper().startswith("ACTION:"):
            r["action"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("INPUT:"):
            r["input"]  = line.split(":", 1)[1].strip()
    return r

def _has_action_format(text: str) -> bool:
    return any(l.strip().upper().startswith("ACTION:") for l in text.split("\n"))

def _sanitize(inp: str) -> str:
    if not inp:
        return ""
    inp = inp.replace('"', "").replace("'", "").strip()
    return inp.split(",")[0].strip() if "," in inp else inp

def _fallback(user_input, broadcast) -> dict:
    _safe_broadcast(broadcast, {"type": "thinking", "step": search_intro()})
    raw    = get_web_answer(user_input, broadcast)
    spoken = wrap_answer(raw, "fallback")
    save_memory(user_input, spoken, "fallback", [])
    return {"raw": spoken, "actions": [], "text": user_input, "intent": "fallback"}


# ── Main agent loop ───────────────────────────────────────────────────────────

def agent_loop(user_input: str, broadcast: Optional[Callable] = None) -> dict:
    user_input = user_input.strip()

    if not user_input:
        return {"raw": "I didn't catch that, Sir.", "actions": [], "text": "", "intent": "empty"}

    # Bare search guard
    words = user_input.split()
    if user_input.lower() in ("search", "search for", "find") or \
       (words[0].lower() in ("search", "find") and len(words) <= 2):
        return {"raw": "What would you like me to search for, Sir?",
                "actions": [], "text": "", "intent": "clarification"}

    # ── Step 1: CAD model generation ──────────────────────────────────────────
    if _is_cad_request(user_input):
        _safe_broadcast(broadcast, {"type": "thinking", "step": "Designing 3D model..."})
        result = execute_action("create_3d_model", user_input)
        save_memory(user_input, result, "cad_generation", ["create_3d_model"])
        return {"raw": result, "actions": ["create_3d_model"],
                "text": user_input, "intent": "cad_generation"}

    # ── Step 2: Code generation ───────────────────────────────────────────────
    if _is_code_request(user_input):
        _safe_broadcast(broadcast, {"type": "thinking", "step": "Writing code..."})
        result = generate_code(user_input)
        save_memory(user_input, result, "code_generation", ["generate_code"])
        return {"raw": result, "actions": ["generate_code"],
                "text": user_input, "intent": "code_generation"}

    # ── Step 3: Fast pattern matching (no LLM) ────────────────────────────────
    quick = _quick_action(user_input)
    if quick:
        action, value = quick
        _safe_broadcast(broadcast, {"type": "thinking", "step": f"Executing {action}..."})
        result = execute_action(action, value)
        spoken = result or error_response()
        save_memory(user_input, spoken, "action", [action])
        return {"raw": spoken, "actions": [action],
                "text": value or "", "intent": "action"}

    # ── Step 4: LLM (Gemini → Ollama → web fallback) ─────────────────────────
    _safe_broadcast(broadcast, {"type": "thinking", "step": "Processing your request..."})
    raw_llm = _call_llm(_build_prompt(user_input))

    if not raw_llm:
        return _fallback(user_input, broadcast)

    # Conversational reply — no action format
    if not _has_action_format(raw_llm):
        spoken = wrap_answer(raw_llm, "conversation")
        save_memory(user_input, spoken, "conversation", [])
        return {"raw": spoken, "actions": [], "text": user_input, "intent": "conversation"}

    # Action reply
    parsed  = _parse_response(raw_llm)
    actions = [a.strip().lower() for a in parsed["action"].split(",") if a.strip()]
    actions = [a for a in actions if a in VALID_ACTIONS and a not in ("final", "none")]
    query   = _sanitize(parsed["input"])

    if not actions:
        return _fallback(user_input, broadcast)

    results = []
    for act in actions:
        _safe_broadcast(broadcast, {"type": "thinking",
                                    "step": f"{acknowledgement()} Executing {act}..."})
        if act == "generate_code":
            results.append(generate_code(query or user_input))
        elif act == "search_google" and "open_chrome" not in actions:
            _safe_broadcast(broadcast, {"type": "thinking", "step": search_intro()})
            results.append(wrap_answer(
                get_web_answer(query or user_input, broadcast), "search"
            ))
        else:
            results.append(execute_action(act, query or None))

    final = " | ".join(r for r in results if r) or error_response()
    save_memory(user_input, final, "agent", actions)
    return {"raw": final, "actions": actions, "text": query, "intent": "agent"}