"""
briefing.py — Morning briefing: weather + news + tasks on startup.
Runs once when S.G.A starts (if enabled in settings.json).
"""
import logging
import datetime
from backend.action_engine import get_weather, get_news
from backend.memory import list_tasks
from backend.settings import get
from backend.speaker import speak

logger = logging.getLogger(__name__)


def morning_briefing():
    """Deliver a morning briefing when S.G.A starts."""
    try:
        now  = datetime.datetime.now()
        hour = now.hour
        name = get("user_name", "Sir")

        if hour < 12:   greeting = f"Good morning, {name}."
        elif hour < 17: greeting = f"Good afternoon, {name}."
        else:           greeting = f"Good evening, {name}."

        parts = [greeting, "Here is your briefing."]

        # Time
        parts.append(f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}.")

        # Weather
        city = get("default_city", "Asansol")
        try:
            weather = get_weather(city)
            parts.append(weather)
        except Exception as e:
            logger.warning("Briefing weather failed: %s", e)

        # News (top 3 headlines)
        try:
            news = get_news("india")
            if news and "Top" in news:
                # Extract just first 2 headlines for briefing
                headlines = news.split(". ")[:3]
                parts.append("Today's top news: " + ". ".join(headlines))
        except Exception as e:
            logger.warning("Briefing news failed: %s", e)

        # Pending tasks
        try:
            tasks = list_tasks()
            if tasks and "no tasks" not in tasks.lower():
                parts.append(f"Your tasks: {tasks}")
        except Exception as e:
            logger.warning("Briefing tasks failed: %s", e)

        parts.append("S.G.A is ready and fully operational.")

        full_briefing = " ".join(parts)
        logger.info("Morning briefing: %s", full_briefing[:100])
        speak(full_briefing)

    except Exception as e:
        logger.error("Morning briefing error: %s", e)
        speak(f"Good day. S.G.A is online and ready.")
