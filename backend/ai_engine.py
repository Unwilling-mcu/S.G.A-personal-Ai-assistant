import re
import logging
from backend.memory import save_memory, get_last_command, get_most_used_intent
from backend.speaker import speak
from backend.personality import (
    greeting_response, status_report, time_response, date_response,
    farewell_response, wrap_answer, acknowledgement, unknown_response
)

logger = logging.getLogger(__name__)


def process_input(user_input: str) -> dict:
    from backend.connection import broadcast

    user_input = user_input.lower().strip()
    logger.info("Processing: %s", user_input)

    actions, text, intent = [], "", "unknown"

    # ── Repeat last ───────────────────────────────────────────────────────────
    if "again" in user_input or "repeat that" in user_input:
        last = get_last_command()
        if last:
            speak("Repeating your last command.")
            return {
                "raw": last["ai"], "actions": last.get("actions", []),
                "text": "", "intent": last["intent"]
            }

    # ── Greetings ─────────────────────────────────────────────────────────────
    if any(g in user_input for g in ("hello", "hi ", "hey", "good morning", "good evening")):
        intent, text = "greeting", user_input
        response_text = greeting_response()

    # ── Status ────────────────────────────────────────────────────────────────
    elif "status" in user_input or "systems" in user_input:
        intent, text = "status", user_input
        response_text = status_report()

    # ── Time / Date ───────────────────────────────────────────────────────────
    elif "time" in user_input:
        intent, text = "time", user_input
        response_text = time_response()

    elif "date" in user_input or "day is it" in user_input:
        intent, text = "date", user_input
        response_text = date_response()

    # ── Farewell ──────────────────────────────────────────────────────────────
    elif any(b in user_input for b in ("goodbye", "bye", "shut down")):
        intent, text = "farewell", user_input
        response_text = farewell_response()

    # ── Search ────────────────────────────────────────────────────────────────
    elif any(s in user_input for s in ("search", "look up", "find", "what is", "who is")):
        intent = "search"
        actions = ["search_google"]
        match = re.search(r"(?:search|look up|find|what is|who is)\s+(.*)", user_input)
        text = match.group(1).strip() if match else user_input
        response_text = wrap_answer(text, "search")

    # ── Open apps ─────────────────────────────────────────────────────────────
    elif "open chrome" in user_input:
        intent, actions = "open_app", ["open_chrome"]
        response_text = acknowledgement() + " Opening Chrome."

    elif "open notepad" in user_input or "open note" in user_input:
        intent, actions = "open_app", ["open_notepad"]
        response_text = acknowledgement() + " Opening Notepad."

    elif "open camera" in user_input:
        intent, actions = "open_app", ["open_camera"]
        response_text = acknowledgement() + " Launching camera."

    elif "open vs code" in user_input or "open vscode" in user_input:
        intent, actions = "open_app", ["open_vscode"]
        response_text = acknowledgement() + " Opening VS Code."

    # ── Adaptive fallback ─────────────────────────────────────────────────────
    else:
        most_used = get_most_used_intent()
        if most_used == "search":
            intent, actions, text = "search", ["search_google"], user_input
            response_text = wrap_answer(user_input, "search")
        else:
            intent, actions, text = "conversation", ["none"], user_input
            response_text = unknown_response()

    ai_output = {"raw": response_text, "actions": actions, "text": text, "intent": intent}

    speak(response_text)
    save_memory(user_input, response_text, intent, actions)

    try:
        broadcast({
            "user": user_input, "ai": response_text,
            "intent": intent, "actions": actions, "parsed_text": text
        })
    except Exception as e:
        logger.warning("Broadcast failed: %s", e)

    return ai_output