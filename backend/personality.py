"""
personality.py — JARVIS-style AI personality layer for S.G.A.
"""
import datetime
import random
import re
import logging

logger = logging.getLogger(__name__)

ASSISTANT_NAME = "S.G.A"
USER_NAME      = "Sir"   # change to your name if preferred


def _time_of_day() -> str:
    h = datetime.datetime.now().hour
    if h < 12:  return "morning"
    if h < 17:  return "afternoon"
    return "evening"


# ── Canned responses ──────────────────────────────────────────────────────────

def greeting_response() -> str:
    options = [
        f"Good {_time_of_day()}, {USER_NAME}. All systems are operational.",
        f"Welcome back, {USER_NAME}. How may I assist you today?",
        f"At your service, {USER_NAME}.",
        f"Online and ready, {USER_NAME}. What do you need?",
    ]
    return random.choice(options)


def farewell_response() -> str:
    options = [
        f"Very well, {USER_NAME}. I'll be here should you need me.",
        f"Understood. Signing off for now.",
        f"Goodbye, {USER_NAME}. Stay brilliant.",
    ]
    return random.choice(options)


def acknowledgement() -> str:
    return random.choice(["Right away.", "On it.", "Consider it done.",
                          "Executing now.", "Of course, {USER_NAME}.".replace("{USER_NAME}", USER_NAME)])


def search_intro() -> str:
    return random.choice([
        "Pulling that up for you.",
        "Scanning available sources.",
        "One moment while I retrieve that.",
        "Accessing knowledge base.",
    ])


def error_response() -> str:
    return random.choice([
        f"My apologies, {USER_NAME}. I encountered an issue with that request.",
        "I wasn't able to process that. Shall I try a different approach?",
        f"Something went wrong on my end, {USER_NAME}. Please try again.",
    ])


def unknown_response() -> str:
    return random.choice([
        f"I'm afraid I didn't catch that clearly, {USER_NAME}.",
        "Could you rephrase that? I want to make sure I assist you correctly.",
        f"That one's beyond my current parameters, {USER_NAME}.",
    ])


def status_report() -> str:
    now = datetime.datetime.now()
    return (
        f"All systems nominal, {USER_NAME}. "
        f"Current time is {now.strftime('%I:%M %p')}. "
        f"Voice recognition active. Knowledge base online."
    )


def time_response() -> str:
    now = datetime.datetime.now()
    return f"It is currently {now.strftime('%I:%M %p')}, {USER_NAME}."


def date_response() -> str:
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}, {USER_NAME}."


# ── Answer wrapping ───────────────────────────────────────────────────────────

def wrap_answer(raw_answer: str, intent: str) -> str:
    """
    Wrap a raw factual answer in a JARVIS-style delivery.
    Trims to 3 sentences max so TTS stays snappy.
    """
    if not raw_answer or raw_answer.strip() == "":
        return unknown_response()

    intros = {
        "search":       ["Here's what I found. ", "According to my sources, ", ""],
        "agent":        ["", acknowledgement() + " "],
        "fallback":     ["Here's what I could gather. ", ""],
        "conversation": [""],
    }
    intro = random.choice(intros.get(intent, [""]))
    answer = _trim_for_speech(raw_answer)
    return f"{intro}{answer}".strip()


def _trim_for_speech(text: str, max_sentences: int = 3) -> str:
    """Keep only the first N sentences for comfortable TTS length."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    trimmed = " ".join(sentences[:max_sentences])
    if len(sentences) > max_sentences:
        trimmed += "."
    return trimmed


# ── LLM system prompt ─────────────────────────────────────────────────────────

def jarvis_llm_system_prompt() -> str:
    tod = _time_of_day()
    return f"""You are {ASSISTANT_NAME}, an advanced personal AI assistant — modelled after JARVIS from Iron Man.

Personality rules:
- Calm, precise, highly intelligent
- Address the user as "{USER_NAME}" naturally but not in every sentence
- Occasionally witty, never sarcastic or casual
- CONCISE: maximum 3 sentences for any answer unless asked to elaborate
- Never say "I am an AI" or "As a language model" — you ARE {ASSISTANT_NAME}
- Speak in first person confidently

For COMMANDS (open apps, search), use EXACTLY:
ACTION: <comma-separated actions>
INPUT: <clean text>

Allowed actions: open_chrome, open_notepad, open_camera, open_vscode, search_google, none

For QUESTIONS or CONVERSATION, reply naturally — no ACTION/INPUT format needed.

Examples:
User: open chrome and search python
ACTION: open_chrome, search_google
INPUT: python tutorials

User: what is quantum computing
Quantum computing harnesses quantum mechanical phenomena like superposition and entanglement to process information in ways classical computers cannot, {USER_NAME}. It holds promise for breakthroughs in cryptography, drug discovery, and optimisation problems.

User: hello
Good {tod}, {USER_NAME}. All systems are fully operational. How may I assist you?

User: what time is it
It is currently {datetime.datetime.now().strftime('%I:%M %p')}, {USER_NAME}."""