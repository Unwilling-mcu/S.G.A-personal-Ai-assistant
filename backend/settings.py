"""
settings.py — Runtime settings loaded from settings.json.
Change settings.json to toggle features without editing code.
"""
import json
import os
import logging

logger = logging.getLogger(__name__)

SETTINGS_FILE = "settings.json"

DEFAULTS = {
    "face_auth_enabled":      False,
    "wake_word_mode":         False,
    "wake_word":              "hey sga",
    "tts_engine":             "pyttsx3",        # "pyttsx3" or "elevenlabs"
    "elevenlabs_voice_id":    "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
    "stt_engine":             "google",          # "google" or "whisper"
    "whisper_model":          "base",            # tiny/base/small/medium
    "gemini_model":           "gemini-2.0-flash-lite",
    "groq_model":             "llama-3.3-70b-versatile",
    "ollama_model":           "mistral",
    "user_name":              "Sir",
    "assistant_name":         "S.G.A",
    "morning_briefing":       True,
    "default_city":           "Asansol",
    "max_memory":             200,
    "response_max_tokens":    600,
    "code_max_tokens":        1500,
    "stream_responses":       True,
    "debug_mode":             False,
}


def load_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULTS)
        return DEFAULTS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Merge with defaults so new keys always exist
        merged = {**DEFAULTS, **data}
        return merged
    except Exception as e:
        logger.warning("Settings load error (%s) — using defaults", e)
        return DEFAULTS.copy()


def save_settings(settings: dict):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        logger.error("Settings save error: %s", e)


def get(key: str, default=None):
    return load_settings().get(key, default)


def set_setting(key: str, value):
    s = load_settings()
    s[key] = value
    save_settings(s)
    logger.info("Setting updated: %s = %s", key, value)