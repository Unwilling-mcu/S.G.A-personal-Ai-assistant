"""
voice_loop.py — Main voice loop with Whisper STT option + morning briefing.
"""
import time
import logging
from typing import Optional
import speech_recognition as sr

from backend.agent_engine import agent_loop
from backend.connection import broadcast
from backend.speaker import speak
from backend.personality import (
    greeting_response, status_report, time_response,
    date_response, farewell_response
)
from backend.memory import save_memory, add_task, list_tasks, complete_task, delete_task
from backend.settings import get

logger = logging.getLogger(__name__)

WAKE_WORDS   = ("hey sga","hey s g a","sga","jarvis","computer","hey jarvis")
MAX_ERRORS   = 10
RETRY_DELAY  = 2
LISTEN_TIMEOUT = 10
PHRASE_LIMIT   = 15


def _listen_google(recognizer, source) -> str:
    audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_LIMIT)
    return recognizer.recognize_google(audio).lower().strip()


def _listen_whisper(recognizer, source) -> str:
    """Use OpenAI Whisper for much more accurate STT."""
    audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_LIMIT)
    return recognizer.recognize_whisper(audio, model=get("whisper_model","base")).lower().strip()


def _listen(recognizer, source) -> str:
    engine = get("stt_engine", "google")
    if engine == "whisper":
        try:
            return _listen_whisper(recognizer, source)
        except Exception as e:
            logger.warning("Whisper failed (%s) — falling back to Google", e)
    return _listen_google(recognizer, source)


def _quick_response(text: str) -> Optional[str]:
    t = text.lower().strip()
    name = get("user_name", "Sir")

    # Task management quick responses
    if t.startswith("add task") or t.startswith("add to my list"):
        task = t.replace("add task","").replace("add to my list","").strip(" .,")
        return add_task(task) if task else "What task would you like to add?"
    if any(x in t for x in ("my tasks","my to do","my todo","list tasks","show tasks","what are my tasks")):
        return list_tasks()
    if t.startswith("complete task") or t.startswith("done with") or t.startswith("mark done"):
        item = t.replace("complete task","").replace("done with","").replace("mark done","").strip()
        return complete_task(item) if item else "Which task is complete?"
    if t.startswith("delete task") or t.startswith("remove task"):
        item = t.replace("delete task","").replace("remove task","").strip()
        return delete_task(item) if item else "Which task to delete?"

    # Settings changes
    if "enable wake word" in t:
        from backend.settings import set_setting
        set_setting("wake_word_mode", True)
        return "Wake word mode enabled. Say 'Hey S.G.A' to activate me."
    if "disable wake word" in t:
        from backend.settings import set_setting
        set_setting("wake_word_mode", False)
        return "Wake word mode disabled. I will always be listening."
    if "switch to elevenlabs" in t or "use elevenlabs" in t:
        from backend.settings import set_setting
        set_setting("tts_engine","elevenlabs")
        return "Switched to ElevenLabs voice. Add ELEVENLABS_API_KEY to .env file."
    if "switch to pyttsx3" in t or "use default voice" in t:
        from backend.settings import set_setting
        set_setting("tts_engine","pyttsx3")
        return "Switched back to default voice."
    if "clear memory" in t or "forget everything" in t:
        from backend.memory import clear_memory
        clear_memory()
        return "Memory cleared, Sir."
    if "search memory" in t or "what did i say about" in t:
        from backend.memory import search_memory
        query = t.replace("search memory","").replace("what did i say about","").strip()
        results = search_memory(query)
        if results:
            return f"I found {len(results)} past interactions about '{query}'."
        return f"Nothing found about '{query}' in memory."

    # Standard quick responses
    if any(g in t for g in ("hello","hi ","hey ","good morning","good afternoon","good evening","sup ")):
        return greeting_response()
    if "how are you" in t or "you doing" in t:
        return f"Fully operational and at your disposal, {name}."
    if "status" in t or "diagnostics" in t or "systems check" in t:
        return status_report()
    if any(x in t for x in ("what time","current time","time is it","what's the time")):
        return time_response()
    if any(x in t for x in ("what date","today's date","what day","what's today")):
        return date_response()
    if any(b in t for b in ("goodbye","bye","shut down voice","stop listening","farewell")):
        return farewell_response()
    if "who are you" in t or "your name" in t or "introduce yourself" in t or "what are you" in t:
        return (f"I am S.G.A — your personal AI assistant, {name}. "
                "I can control your PC, browse the web, write code, manage tasks, "
                "check weather, translate languages, set reminders, and much more.")
    if "what can you do" in t or "your capabilities" in t or "help" in t:
        return ("I can: open apps and websites, search Google, check weather anywhere, "
                "get news headlines, write code in any language, take screenshots, "
                "describe your screen, set reminders, manage your task list, "
                "translate text, calculate math, control volume, "
                "read your files, tell jokes, and answer questions — all by voice.")
    if "thank" in t:
        return f"My pleasure, {name}."
    if "sorry" in t:
        return "No need to apologize. How can I help?"
    if "clear" in t and "task" in t:
        from backend.memory import clear_completed_tasks
        return clear_completed_tasks()
    return None


def _safe_broadcast(message: dict):
    try: broadcast(message)
    except Exception: pass

def _is_wake_word(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in WAKE_WORDS)

def _strip_wake_word(text: str) -> str:
    t = text.lower().strip()
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        if t.startswith(w): t = t[len(w):].strip(" ,."); break
    return t or text

def _backoff(errors: int):
    time.sleep(30 if errors >= MAX_ERRORS else RETRY_DELAY)


def start_voice_loop():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.7

    wake_word_mode = get("wake_word_mode", False)
    logger.info("🎤 S.G.A voice loop started (wake_word_mode=%s, stt=%s)",
                wake_word_mode, get("stt_engine","google"))

    # Morning briefing
    if get("morning_briefing", True):
        try:
            from backend.briefing import morning_briefing
            import threading
            threading.Thread(target=morning_briefing, daemon=True).start()
        except Exception as e:
            logger.warning("Briefing failed: %s", e)
            speak(greeting_response())
    else:
        speak(greeting_response())

    consecutive_errors = 0

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                text = _listen(recognizer, source)

            if not text: continue
            consecutive_errors = 0

            if wake_word_mode:
                if not _is_wake_word(text): continue
                text = _strip_wake_word(text)
                if not text: speak("Yes?"); continue

            logger.info("👤 You: %s", text)
            _safe_broadcast({"type": "thinking", "step": "Listening..."})

            quick = _quick_response(text)
            if quick:
                logger.info("⚡ Quick: %s", quick[:80])
                speak(quick)
                save_memory(text, quick, "conversation", [])
                _safe_broadcast({"type":"response","user":text,"ai":quick,
                                 "intent":"conversation","actions":[],"parsed_text":text})
                continue

            ai_output = agent_loop(text, broadcast=broadcast)
            raw = ai_output.get("raw","")
            logger.info("🤖 S.G.A: %s", raw[:120])
            if raw: speak(raw)
            _safe_broadcast({"type":"response","user":text,"ai":raw,
                             "intent":ai_output.get("intent",""),
                             "actions":ai_output.get("actions",[]),
                             "parsed_text":ai_output.get("text","")})

        except sr.WaitTimeoutError: continue
        except sr.UnknownValueError: continue
        except sr.RequestError as e:
            consecutive_errors += 1
            logger.error("STT error: %s", e)
            _backoff(consecutive_errors)
        except OSError as e:
            consecutive_errors += 1
            logger.error("Microphone error: %s", e)
            time.sleep(5)
        except Exception as e:
            consecutive_errors += 1
            logger.exception("Voice loop error: %s", e)
            _backoff(consecutive_errors)