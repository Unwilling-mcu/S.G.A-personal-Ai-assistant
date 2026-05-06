import datetime
import logging

logger = logging.getLogger(__name__)


def offline_response(text: str) -> str:
    """Simple rule-based responses when no internet/LLM is available."""
    text = text.lower().strip()

    if "chrome" in text:
        return "ACTION: open_chrome\nTEXT: Opening Chrome"

    elif "notepad" in text or "note" in text:
        return "ACTION: open_notepad\nTEXT: Opening Notepad"

    elif "vs code" in text or "vscode" in text or "code" in text:
        return "ACTION: open_vscode\nTEXT: Opening VS Code"

    elif "camera" in text:
        return "ACTION: open_camera\nTEXT: Opening Camera"

    elif "search" in text or "find" in text or "look up" in text:
        query = text.replace("search", "").replace("find", "").replace("look up", "").strip()
        return f"ACTION: search_google\nTEXT: {query or 'your query'}"

    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"ACTION: none\nTEXT: The current time is {now}"

    elif "date" in text:
        today = datetime.datetime.now().strftime("%A, %B %d %Y")
        return f"ACTION: none\nTEXT: Today is {today}"

    elif any(g in text for g in ("hello", "hi", "hey")):
        return "ACTION: none\nTEXT: Hello! I'm S.G.A, running in offline mode."

    return "ACTION: none\nTEXT: I'm in offline mode and couldn't process that request."