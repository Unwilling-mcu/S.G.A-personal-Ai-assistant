"""
speaker.py — Smart TTS with pyttsx3 (default) or ElevenLabs (premium).
Set tts_engine in settings.json to switch.
"""
import threading
import logging
import re

logger = logging.getLogger(__name__)

TTS_RATE    = 155
TTS_VOLUME  = 1.0
TTS_TIMEOUT = 30
MAX_CHUNK   = 200
_speak_lock = threading.Lock()


def _run_pyttsx3(text: str):
    import pyttsx3
    engine = None
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", TTS_RATE)
        engine.setProperty("volume", TTS_VOLUME)
        voices = engine.getProperty("voices")
        if voices:
            preferred = next(
                (v for v in voices if any(n in v.name.lower() for n in ("david","mark","george"))),
                voices[0]
            )
            engine.setProperty("voice", preferred.id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error("pyttsx3 error: %s", e)
    finally:
        try:
            if engine: engine.stop()
        except Exception: pass


def _run_elevenlabs(text: str):
    """ElevenLabs TTS — natural voice. Needs ELEVENLABS_API_KEY in .env"""
    try:
        import os, requests
        from dotenv import load_dotenv
        load_dotenv()
        api_key  = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            logger.warning("ELEVENLABS_API_KEY not set — falling back to pyttsx3")
            _run_pyttsx3(text); return

        from backend.settings import get
        voice_id = get("elevenlabs_voice_id", "21m00Tcm4TlvDq8ikWAM")

        res = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json={"text": text, "model_id": "eleven_turbo_v2",
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
            timeout=15
        )
        if res.status_code != 200:
            logger.warning("ElevenLabs error %s — falling back to pyttsx3", res.status_code)
            _run_pyttsx3(text); return

        # Play audio bytes
        import tempfile, subprocess
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(res.content)
            tmp = f.name
        # Use Windows Media Player CLI
        subprocess.run(["powershell","-c",
                        f'(New-Object Media.SoundPlayer).PlaySync()'],
                       capture_output=True)
        # Fallback: play via playsound
        try:
            from playsound import playsound
            playsound(tmp, block=True)
        except Exception:
            pass
        os.unlink(tmp)
    except Exception as e:
        logger.error("ElevenLabs TTS error: %s — falling back to pyttsx3", e)
        _run_pyttsx3(text)


def _split_chunks(text: str, max_chars: int) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current: chunks.append(current)
            while len(s) > max_chars:
                chunks.append(s[:max_chars]); s = s[max_chars:]
            current = s
    if current: chunks.append(current)
    return chunks or [text[:max_chars]]


def speak(text: str):
    if not text or not text.strip(): return

    # Strip markdown code blocks from TTS (don't read out code)
    clean = re.sub(r'```[\s\S]*?```', 'Code block generated.', text.strip())
    clean = re.sub(r'`[^`]+`', '', clean)
    clean = clean.strip()
    if not clean: return

    try:
        from backend.settings import get
        engine = get("tts_engine", "pyttsx3")
    except Exception:
        engine = "pyttsx3"

    tts_fn = _run_elevenlabs if engine == "elevenlabs" else _run_pyttsx3

    chunks = _split_chunks(clean, MAX_CHUNK)
    for chunk in chunks:
        with _speak_lock:
            t = threading.Thread(target=tts_fn, args=(chunk,), daemon=True)
            t.start()
            t.join(timeout=TTS_TIMEOUT)
            if t.is_alive():
                logger.warning("TTS timed out — skipping remainder")
                break