import requests
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"


def local_ai_response(prompt: str) -> str:
    system_prompt = f"""You are S.G.A, an AI assistant.

Reply in EXACTLY this format — no extra words:
ACTION: <comma-separated actions>
TEXT: <clean relevant text>

Allowed actions: open_chrome, open_notepad, open_vscode, open_camera, search_google, move_mouse, click_mouse, none

Examples:
User: open chrome and notepad
ACTION: open_chrome, open_notepad
TEXT: Opening Chrome and Notepad

User: search latest AI news
ACTION: search_google
TEXT: latest AI news

User: {prompt}"""

    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": system_prompt, "stream": False},
            timeout=30
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running — using offline fallback")
        from backend.offline_ai import offline_response
        return offline_response(prompt)
    except Exception as e:
        logger.error("local_ai_response error: %s", e)
        return "ACTION: none\nTEXT: Error processing request"


def parse_local_response(raw: str) -> dict:
    """Parse ACTION/TEXT response into a dict."""
    result = {"actions": [], "text": ""}
    for line in raw.strip().split("\n"):
        line = line.strip()
        if line.upper().startswith("ACTION:"):
            raw_actions = line.split(":", 1)[1].strip()
            result["actions"] = [a.strip().lower() for a in raw_actions.split(",") if a.strip()]
        elif line.upper().startswith("TEXT:"):
            result["text"] = line.split(":", 1)[1].strip()
    return result