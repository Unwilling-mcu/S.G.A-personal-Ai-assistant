import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)

WAKE_WORDS = ("hey s.g.a", "hey sga", "sga", "jarvis")


def listen(timeout: int = 10, phrase_limit: int = 15) -> str:
    """Listen once and return recognised text, or empty string on failure."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        return recognizer.recognize_google(audio).strip()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        logger.error("Speech recognition error: %s", e)
        return ""
    except OSError as e:
        logger.error("Microphone error: %s", e)
        return ""


def detect_wake_word() -> bool:
    """Return True if a wake word is heard."""
    text = listen(timeout=5).lower()
    return any(wake in text for wake in WAKE_WORDS)