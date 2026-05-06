import logging
import sys

logger = logging.getLogger(__name__)


def execute(command: str):
    """Simple automation executor for direct OS commands."""
    command = command.lower().strip()
    logger.info("Automation execute: %s", command)

    try:
        import subprocess

        if "notepad" in command:
            subprocess.Popen(["notepad.exe"] if sys.platform == "win32" else ["gedit"])

        elif "chrome" in command:
            subprocess.Popen(["start", "chrome"] if sys.platform == "win32" else ["google-chrome"], shell=(sys.platform == "win32"))

        elif "vs code" in command or "vscode" in command:
            subprocess.Popen(["code"])

        elif "shutdown" in command:
            if sys.platform == "win32":
                subprocess.Popen(["shutdown", "/s", "/t", "5"])
            else:
                subprocess.Popen(["shutdown", "-h", "+1"])

        elif "restart" in command:
            if sys.platform == "win32":
                subprocess.Popen(["shutdown", "/r", "/t", "5"])
            else:
                subprocess.Popen(["reboot"])

        elif "search" in command:
            from backend.web_agent import get_web_answer
            query = command.replace("search", "").strip()
            return get_web_answer(query)

        elif "move mouse" in command:
            try:
                import pyautogui
                pyautogui.moveTo(500, 500, duration=0.3)
            except ImportError:
                logger.warning("pyautogui not installed")

        elif "click" in command:
            try:
                import pyautogui
                pyautogui.click()
            except ImportError:
                logger.warning("pyautogui not installed")

        else:
            logger.warning("No automation rule for: %s", command)

    except Exception as e:
        logger.error("Automation error: %s", e)