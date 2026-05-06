import subprocess
import urllib.parse
import sys
import os
import logging
import threading
import re

logger = logging.getLogger(__name__)

# ── Chrome ────────────────────────────────────────────────────────────────────
CHROME_PATH     = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_FALLBACK = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE  = "--profile-directory=Default"

def _get_chrome():
    for p in [CHROME_PATH, CHROME_FALLBACK]:
        if os.path.exists(p): return p
    return "chrome"

def clean_query(q):
    if not q: return ""
    q = q.replace('"',"").replace("'","").strip()
    if "http" in q or "," in q:
        q = q.split(",")[0].strip()
    return q

# ── App launchers ─────────────────────────────────────────────────────────────

def open_chrome(_=None):
    try: subprocess.Popen([_get_chrome(), CHROME_PROFILE]); return "Chrome opened"
    except Exception as e: return f"Chrome failed: {e}"

def search_google(query):
    query = clean_query(query)
    if not query: return "No search query"
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    try: subprocess.Popen([_get_chrome(), CHROME_PROFILE, url]); return f'Searching "{query}"'
    except Exception:
        import webbrowser; webbrowser.open(url); return f'Searching "{query}"'

def open_website(url):
    if not url: return "No URL"
    if not url.startswith("http"): url = "https://" + url
    try: subprocess.Popen([_get_chrome(), CHROME_PROFILE, url]); return f"Opening {url}"
    except Exception:
        import webbrowser; webbrowser.open(url); return f"Opening {url}"

def open_notepad(_=None):
    try: subprocess.Popen(["notepad.exe"]); return "Notepad opened"
    except Exception as e: return f"Failed: {e}"

def open_camera(_=None):
    try: subprocess.Popen("start microsoft.windows.camera:", shell=True); return "Camera opened"
    except Exception as e: return f"Failed: {e}"

def open_vscode(_=None):
    try: subprocess.Popen(["code"]); return "VS Code opened"
    except Exception as e: return f"Failed: {e}"

def open_calculator(_=None):
    try: subprocess.Popen(["calc.exe"]); return "Calculator opened"
    except Exception as e: return f"Failed: {e}"

def open_taskmanager(_=None):
    try: subprocess.Popen(["taskmgr.exe"]); return "Task Manager opened"
    except Exception as e: return f"Failed: {e}"

# ── App switcher ──────────────────────────────────────────────────────────────

def switch_to_app(app_name):
    """Bring a running app window to focus using pyautogui/pygetwindow."""
    if not app_name: return "No app name given"
    try:
        import pygetwindow as gw
        name = app_name.lower().strip()
        windows = gw.getAllTitles()
        match = next((w for w in windows if name in w.lower() and w.strip()), None)
        if match:
            win = gw.getWindowsWithTitle(match)[0]
            win.activate()
            return f"Switched to {match}"
        return f"No open window found for '{app_name}'"
    except ImportError:
        # Fallback: use Alt+Tab simulation
        try:
            import pyautogui
            pyautogui.hotkey("alt", "tab")
            return f"Switched window (tip: pip install pygetwindow for precise switching)"
        except Exception as e:
            return f"Switch failed: {e}"
    except Exception as e:
        return f"Switch failed: {e}"

# ── Screenshot & Vision ───────────────────────────────────────────────────────

def take_screenshot(_=None):
    try:
        import pyautogui, datetime
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        fname   = f"sga_{datetime.datetime.now().strftime('%H%M%S')}.png"
        fpath   = os.path.join(desktop, fname)
        pyautogui.screenshot(fpath)
        logger.info("Screenshot saved: %s", fpath)
        return f"Screenshot saved to your Desktop as {fname}"
    except ImportError: return "ERROR: pip install pyautogui"
    except Exception as e: return f"Screenshot failed: {e}"

def describe_screen(_=None):
    path = take_screenshot()
    if not path.endswith(".png"): return path
    try:
        import base64
        from dotenv import load_dotenv; load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return f"Screenshot saved to Desktop. Add GEMINI_API_KEY for AI description."
        from google import genai
        from google.genai import types
        with open(path,"rb") as f: img_data = base64.b64encode(f.read()).decode()
        client   = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[
                types.Part.from_bytes(data=base64.b64decode(img_data), mime_type="image/png"),
                "Describe what is on this screen in 2-3 sentences. Be specific about apps and content visible."
            ]
        )
        return response.text.strip() if response.text else "Could not describe screen."
    except Exception as e:
        return f"Screenshot saved. Vision failed: {e}"

# ── Typing & Mouse ────────────────────────────────────────────────────────────

def type_text(text):
    if not text: return "No text to type"
    try:
        import pyautogui, time; time.sleep(0.5)
        pyautogui.typewrite(text, interval=0.05)
        return f'Typed: "{text}"'
    except ImportError: return "ERROR: pip install pyautogui"
    except Exception as e: return f"Type failed: {e}"

def click_mouse(_=None):
    try: import pyautogui; pyautogui.click(); return "Clicked"
    except Exception as e: return f"Click failed: {e}"

def move_mouse(coords):
    try:
        import pyautogui
        x, y = (int(v.strip()) for v in coords.split(","))
        pyautogui.moveTo(x, y, duration=0.3); return f"Mouse moved to {x},{y}"
    except Exception as e: return f"Move failed: {e}"

# ── Volume ────────────────────────────────────────────────────────────────────

def volume_up(_=None):
    try:
        import pyautogui
        for _ in range(5): pyautogui.press("volumeup")
        return "Volume increased"
    except Exception as e: return f"Failed: {e}"

def volume_down(_=None):
    try:
        import pyautogui
        for _ in range(5): pyautogui.press("volumedown")
        return "Volume decreased"
    except Exception as e: return f"Failed: {e}"

def volume_mute(_=None):
    try: import pyautogui; pyautogui.press("volumemute"); return "Muted/unmuted"
    except Exception as e: return f"Failed: {e}"

# ── Clipboard ─────────────────────────────────────────────────────────────────

def read_clipboard(_=None):
    try:
        import pyperclip
        text = pyperclip.paste()
        if text.strip():
            return f"Clipboard contains: {text[:300]}"
        return "Clipboard is empty"
    except ImportError: return "ERROR: pip install pyperclip"
    except Exception as e: return f"Clipboard read failed: {e}"

def write_clipboard(text):
    if not text: return "Nothing to copy"
    try:
        import pyperclip
        pyperclip.copy(text)
        return f"Copied to clipboard: {text[:100]}"
    except ImportError: return "ERROR: pip install pyperclip"
    except Exception as e: return f"Clipboard write failed: {e}"

# ── System info ───────────────────────────────────────────────────────────────

def get_system_info(_=None):
    try:
        import psutil
        cpu   = psutil.cpu_percent(interval=1)
        ram   = psutil.virtual_memory()
        disk  = psutil.disk_usage("/")
        ram_used  = ram.used  // (1024**3)
        ram_total = ram.total // (1024**3)
        disk_used  = disk.used  // (1024**3)
        disk_total = disk.total // (1024**3)

        battery_info = ""
        try:
            bat = psutil.sensors_battery()
            if bat:
                status = "charging" if bat.power_plugged else "on battery"
                battery_info = f" Battery {int(bat.percent)}% ({status})."
        except Exception: pass

        return (
            f"CPU usage {cpu}%. "
            f"RAM {ram_used}GB of {ram_total}GB used. "
            f"Disk {disk_used}GB of {disk_total}GB used.{battery_info}"
        )
    except ImportError: return "ERROR: pip install psutil"
    except Exception as e: return f"System info failed: {e}"

def get_battery(_=None):
    try:
        import psutil
        bat = psutil.sensors_battery()
        if bat:
            status = "charging" if bat.power_plugged else "on battery"
            mins   = bat.secsleft // 60 if bat.secsleft > 0 else 0
            time_str = f", about {mins} minutes remaining" if mins > 0 and not bat.power_plugged else ""
            return f"Battery is at {int(bat.percent)}%, {status}{time_str}."
        return "No battery detected — running on AC power."
    except ImportError: return "ERROR: pip install psutil"
    except Exception as e: return f"Battery check failed: {e}"

# ── Process manager ───────────────────────────────────────────────────────────

def list_processes(_=None):
    try:
        import psutil
        procs = [(p.info["name"], p.info["pid"], p.info["cpu_percent"])
                 for p in psutil.process_iter(["name","pid","cpu_percent"])
                 if p.info["cpu_percent"] and p.info["cpu_percent"] > 0.5]
        procs.sort(key=lambda x: x[2], reverse=True)
        top = procs[:8]
        if not top: return "No high CPU processes right now."
        lines = [f"{n} (PID {pid}) — {cpu:.1f}% CPU" for n, pid, cpu in top]
        return "Top processes: " + "; ".join(lines)
    except ImportError: return "ERROR: pip install psutil"
    except Exception as e: return f"Process list failed: {e}"

def kill_process(name):
    if not name: return "No process name given"
    try:
        import psutil
        killed = []
        for p in psutil.process_iter(["name","pid"]):
            if name.lower() in p.info["name"].lower():
                p.kill(); killed.append(p.info["name"])
        if killed: return f"Killed: {', '.join(killed)}"
        return f"No process named '{name}' found"
    except ImportError: return "ERROR: pip install psutil"
    except Exception as e: return f"Kill failed: {e}"

# ── Weather ───────────────────────────────────────────────────────────────────

def get_weather(city="Asansol"):
    if not city or city.strip() == "": city = "Asansol"
    city = city.strip()
    try:
        import requests
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=6
        ).json()
        if not geo.get("results"): return f"Could not find weather for {city}."
        r = geo["results"][0]
        lat, lon, name = r["latitude"], r["longitude"], r.get("name", city)
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon,
                    "current": "temperature_2m,weathercode,windspeed_10m,relative_humidity_2m",
                    "timezone": "auto"}, timeout=6
        ).json()
        c = w["current"]
        desc = _wmo_desc(c["weathercode"])
        return (f"{name}: {desc}, {c['temperature_2m']}°C. "
                f"Wind {c['windspeed_10m']} km/h, humidity {c['relative_humidity_2m']}%.")
    except Exception as e: return f"Weather failed: {e}"

def _wmo_desc(code):
    m = {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
         45:"Foggy",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",
         61:"Light rain",63:"Moderate rain",65:"Heavy rain",
         71:"Light snow",73:"Moderate snow",75:"Heavy snow",
         80:"Light showers",81:"Showers",82:"Heavy showers",95:"Thunderstorm"}
    return m.get(code, f"Code {code}")

# ── News ──────────────────────────────────────────────────────────────────────

def get_news(topic="technology"):
    """Free news via Google News RSS — no API key."""
    if not topic or topic.strip() == "": topic = "technology"
    topic = topic.strip()
    try:
        import requests
        from xml.etree import ElementTree as ET
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(topic)}&hl=en-IN&gl=IN&ceid=IN:en"
        res = ET.fromstring(requests.get(url, timeout=8, headers={
            "User-Agent": "Mozilla/5.0"}).content)
        items = res.findall(".//item")[:5]
        if not items: return f"No news found for '{topic}'"
        headlines = [item.find("title").text.split(" - ")[0] for item in items if item.find("title") is not None]
        return f"Top {topic} news: " + ". ".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
    except Exception as e: return f"News failed: {e}"

# ── Math & conversions ────────────────────────────────────────────────────────

def calculate(expression):
    """Safe math evaluator."""
    if not expression: return "No expression given"
    try:
        expr = expression.lower().strip()
        # Remove spoken filler words
        for word in ["calculate", "what is", "whats", "compute", "equals"]:
            expr = expr.replace(word, "").strip()

        # Step 1: Handle "X% of Y" BEFORE stripping non-numeric chars
        expr = re.sub(
            r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)",
            lambda m: str(float(m.group(1)) / 100 * float(m.group(2))),
            expr
        )

        # Step 2: Now strip everything except math operators
        safe = re.sub(r"[^0-9+\-*/().^ ]", "", expr)
        safe = safe.replace("^", "**").strip()

        if not safe or not re.search(r"\d", safe):
            return f"Could not calculate: {expression}"

        # Detect incomplete "X% of" — missing second number
        if safe.endswith("%") or re.search(r"of\s*$", expr.strip()):
            return "Of what number, Sir? Please say the full expression, like 25 percent of 2000."

        result = eval(safe, {"__builtins__": {}})

        # Format nicely
        if isinstance(result, float) and result == int(result):
            result = int(result)

        return f"The answer is {result}"
    except Exception:
        return f"Could not calculate: {expression}"

def convert_units(text):
    """Simple unit converter."""
    if not text: return "Nothing to convert"
    text = text.lower().strip()
    conversions = {
        r"(\d+(?:\.\d+)?)\s*km?\s*(?:to|in)\s*miles?":
            lambda m: f"{float(m.group(1))} km = {float(m.group(1)) * 0.621371:.2f} miles",
        r"(\d+(?:\.\d+)?)\s*miles?\s*(?:to|in)\s*km?":
            lambda m: f"{float(m.group(1))} miles = {float(m.group(1)) * 1.60934:.2f} km",
        r"(\d+(?:\.\d+)?)\s*kg\s*(?:to|in)\s*(?:lbs?|pounds?)":
            lambda m: f"{float(m.group(1))} kg = {float(m.group(1)) * 2.20462:.2f} lbs",
        r"(\d+(?:\.\d+)?)\s*(?:lbs?|pounds?)\s*(?:to|in)\s*kg":
            lambda m: f"{float(m.group(1))} lbs = {float(m.group(1)) * 0.453592:.2f} kg",
        r"(\d+(?:\.\d+)?)\s*(?:°?c|celsius)\s*(?:to|in)\s*(?:°?f|fahrenheit)":
            lambda m: f"{float(m.group(1))}°C = {float(m.group(1)) * 9/5 + 32:.1f}°F",
        r"(\d+(?:\.\d+)?)\s*(?:°?f|fahrenheit)\s*(?:to|in)\s*(?:°?c|celsius)":
            lambda m: f"{float(m.group(1))}°F = {(float(m.group(1)) - 32) * 5/9:.1f}°C",
        r"(\d+(?:\.\d+)?)\s*(?:metre?s?|m)\s*(?:to|in)\s*feet?":
            lambda m: f"{float(m.group(1))} m = {float(m.group(1)) * 3.28084:.2f} feet",
        r"(\d+(?:\.\d+)?)\s*feet?\s*(?:to|in)\s*(?:metre?s?|m)":
            lambda m: f"{float(m.group(1))} feet = {float(m.group(1)) * 0.3048:.2f} m",
        r"(\d+(?:\.\d+)?)\s*(?:litre?s?|l)\s*(?:to|in)\s*(?:gallon|gal)":
            lambda m: f"{float(m.group(1))} litres = {float(m.group(1)) * 0.264172:.2f} gallons",
        r"(\d+(?:\.\d+)?)\s*(?:inch|inches|in)\s*(?:to|in)\s*cm":
            lambda m: f"{float(m.group(1))} inches = {float(m.group(1)) * 2.54:.2f} cm",
        r"(\d+(?:\.\d+)?)\s*cm\s*(?:to|in)\s*(?:inch|inches)":
            lambda m: f"{float(m.group(1))} cm = {float(m.group(1)) / 2.54:.2f} inches",
    }
    for pattern, fn in conversions.items():
        m = re.search(pattern, text)
        if m: return fn(m)
    return f"Could not parse conversion: {text}. Try e.g. '5 km to miles'"

# ── Translation ───────────────────────────────────────────────────────────────

def translate_text(text):
    """Translate using MyMemory free API (no key, 5000 chars/day)."""
    if not text: return "Nothing to translate"
    try:
        # Extract language from request: "translate hello to spanish"
        lang_map = {
            "spanish":"es","french":"fr","german":"de","hindi":"hi",
            "bengali":"bn","japanese":"ja","chinese":"zh","arabic":"ar",
            "portuguese":"pt","russian":"ru","italian":"it","korean":"ko",
            "tamil":"ta","telugu":"te","urdu":"ur","dutch":"nl","turkish":"tr"
        }
        target_lang = "hi"   # default Hindi
        clean_text  = text

        match = re.search(r"(?:to|in)\s+(\w+)\s*$", text.lower())
        if match:
            lang_word = match.group(1).lower()
            if lang_word in lang_map:
                target_lang = lang_map[lang_word]
                clean_text  = re.sub(r"(?:translate\s+)?(.+?)\s+(?:to|in)\s+\w+$",
                                     r"\1", text, flags=re.IGNORECASE).strip()

        # Remove "translate" prefix
        clean_text = re.sub(r"^translate\s+", "", clean_text, flags=re.IGNORECASE).strip()

        import requests
        res = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": clean_text, "langpair": f"en|{target_lang}"},
            timeout=8
        ).json()
        translated = res.get("responseData", {}).get("translatedText", "")
        if translated and translated != clean_text:
            return f"Translation: {translated}"
        return f"Could not translate '{clean_text}'"
    except Exception as e: return f"Translation failed: {e}"

# ── Reminders ─────────────────────────────────────────────────────────────────

_reminder_threads = []

def set_reminder(text):
    import time
    from backend.speaker import speak
    match_min  = re.search(r"(\d+)\s*(?:minute|min)", text, re.IGNORECASE)
    match_hour = re.search(r"(\d+)\s*(?:hour|hr)",   text, re.IGNORECASE)
    if match_min:   seconds, n, unit = int(match_min.group(1))*60,  int(match_min.group(1)),  "minute(s)"
    elif match_hour: seconds, n, unit = int(match_hour.group(1))*3600, int(match_hour.group(1)), "hour(s)"
    else: return "Please specify time, e.g. 'remind me in 10 minutes to drink water'"

    msg = re.sub(r"remind me (in )?\d+ (minute|min|minutes|hour|hr|hours)( to)?",
                 "", text, flags=re.IGNORECASE).strip(" .,!") or "Time's up!"

    def _fire():
        time.sleep(seconds); speak(f"Reminder, Sir: {msg}")
    t = threading.Thread(target=_fire, daemon=True); t.start(); _reminder_threads.append(t)
    return f"Reminder set for {n} {unit}: {msg}"

# ── File reading ──────────────────────────────────────────────────────────────

def read_file(path):
    path = (path or "").strip().strip('"')
    if not path: return "No file path given"
    if not os.path.exists(path):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop", path)
        docs    = os.path.join(os.path.expanduser("~"), "Documents", path)
        for p in [desktop, docs]:
            if os.path.exists(p): path = p; break
        else: return f"File not found: {path}"
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            try:
                import fitz
                doc  = fitz.open(path)
                text = "\n".join(p.get_text() for p in doc); doc.close()
                return text[:2000] + ("..." if len(text)>2000 else "")
            except ImportError: return "ERROR: pip install pymupdf"
        elif ext in (".txt",".md",".py",".js",".html",".css",".json",".csv"):
            with open(path,"r",encoding="utf-8",errors="ignore") as f: content = f.read()
            return content[:2000] + ("..." if len(content)>2000 else "")
        else: return f"Unsupported file type: {ext}"
    except Exception as e: return f"File read error: {e}"

# ── Jokes ─────────────────────────────────────────────────────────────────────

def tell_joke(_=None):
    try:
        import requests
        res = requests.get("https://icanhazdadjoke.com/",
                           headers={"Accept":"application/json"}, timeout=5).json()
        return res.get("joke", "Why don't scientists trust atoms? Because they make up everything!")
    except Exception:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
            "Why was the computer cold? It left its Windows open.",
            "I told my computer I needed a break. Now it won't stop sending me Kit Kat ads.",
            "Why do Java developers wear glasses? Because they don't C#.",
        ]
        import random; return random.choice(jokes)

# ── Wikipedia summary ─────────────────────────────────────────────────────────

def wiki_summary(topic):
    if not topic: return "What topic would you like to know about?"
    try:
        import requests
        headers = {"User-Agent": "SGA-Assistant/1.0"}
        search  = requests.get("https://en.wikipedia.org/w/api.php",
                               params={"action":"query","list":"search",
                                       "srsearch":topic,"format":"json","srlimit":1},
                               headers=headers, timeout=6).json()
        results = search.get("query",{}).get("search",[])
        if not results: return f"No Wikipedia article found for '{topic}'"
        title   = results[0]["title"]
        summary = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}",
                               headers=headers, timeout=6).json()
        extract = summary.get("extract","")
        if extract:
            sentences = re.split(r'(?<=[.!?])\s+', extract)
            return " ".join(sentences[:3])
        return f"Found article: {title}, but no summary available."
    except Exception as e: return f"Wikipedia lookup failed: {e}"

# ── System commands ───────────────────────────────────────────────────────────

def system_shutdown(_=None):
    subprocess.Popen(["shutdown","/s","/t","10"])
    return "System will shut down in 10 seconds. Say cancel shutdown to abort."

def system_restart(_=None):
    subprocess.Popen(["shutdown","/r","/t","10"])
    return "System will restart in 10 seconds."

def cancel_shutdown(_=None):
    subprocess.Popen(["shutdown","/a"])
    return "Shutdown cancelled."

def lock_screen(_=None):
    try: subprocess.Popen(["rundll32.exe","user32.dll,LockWorkStation"]); return "Screen locked"
    except Exception as e: return f"Lock failed: {e}"


# ── Biometric & Gesture ───────────────────────────────────────────────────────

def take_reference_photo(_=None) -> str:
    """Take and save face reference photo for biometric auth."""
    try:
        from backend.auth import take_reference_photo as _take_ref
        return _take_ref()
    except Exception as e:
        return f"Photo capture failed: {e}"


def enable_gesture_control(_=None) -> str:
    """Start gesture engine in a background thread."""
    try:
        from backend.gesture_engine import start_gesture_thread
        start_gesture_thread(show_window=True)
        return "Gesture control activated. Show your hand to the camera, Sir."
    except ImportError:
        return "ERROR: pip install mediapipe opencv-python"
    except Exception as e:
        return f"Gesture control failed: {e}"


def disable_gesture_control(_=None) -> str:
    try:
        from backend.gesture_engine import stop
        stop(); return "Gesture control deactivated."
    except Exception as e:
        return f"Error: {e}"


def enable_air_tracing(_=None) -> str:
    try:
        from backend.gesture_engine import enable_tracing, start_gesture_thread
        enable_tracing(True)
        start_gesture_thread(show_window=True)
        return "Air tracing enabled. Point your index finger to draw."
    except Exception as e:
        return f"Tracing failed: {e}"


def clear_trace(_=None) -> str:
    try:
        from backend.gesture_engine import enable_tracing, _trace_points
        _trace_points.clear()
        return "Trace cleared."
    except Exception as e:
        return f"Error: {e}"


def create_3d_model(description: str) -> str:
    """Generate a 3D model from voice description using build123d."""
    try:
        from backend.cad_agent import handle_cad_voice
        return handle_cad_voice(description)
    except ImportError:
        return "ERROR: pip install build123d"
    except Exception as e:
        return f"3D model error: {e}"

# ── Dispatcher ────────────────────────────────────────────────────────────────

ACTION_MAP = {
    "open_chrome":      open_chrome,
    "search_google":    search_google,
    "open_website":     open_website,
    "open_notepad":     open_notepad,
    "open_camera":      open_camera,
    "open_vscode":      open_vscode,
    "open_calculator":  open_calculator,
    "open_taskmanager": open_taskmanager,
    "switch_to_app":    switch_to_app,
    "take_screenshot":  take_screenshot,
    "describe_screen":  describe_screen,
    "type_text":        type_text,
    "click_mouse":      click_mouse,
    "move_mouse":       move_mouse,
    "volume_up":        volume_up,
    "volume_down":      volume_down,
    "volume_mute":      volume_mute,
    "read_clipboard":   read_clipboard,
    "write_clipboard":  write_clipboard,
    "get_system_info":  get_system_info,
    "get_battery":      get_battery,
    "list_processes":   list_processes,
    "kill_process":     kill_process,
    "get_weather":      get_weather,
    "get_news":         get_news,
    "calculate":        calculate,
    "convert_units":    convert_units,
    "translate":        translate_text,
    "set_reminder":     set_reminder,
    "read_file":        read_file,
    "tell_joke":        tell_joke,
    "wiki_summary":     wiki_summary,
    "shutdown":         system_shutdown,
    "restart":          system_restart,
    "cancel_shutdown":      cancel_shutdown,
    "lock_screen":          lock_screen,
    # Gesture & biometric
    "enable_gesture":       enable_gesture_control,
    "disable_gesture":      disable_gesture_control,
    "enable_tracing":       enable_air_tracing,
    "clear_trace":          clear_trace,
    "take_reference_photo": take_reference_photo,
    # 3D CAD
    "create_3d_model":      create_3d_model,
}

def execute_action(action, value=None):
    action = action.strip().lower()
    fn = ACTION_MAP.get(action)
    if fn: return fn(value) if value else fn()
    logger.warning("Unknown action: %s", action)
    return f"Unknown action: {action}"