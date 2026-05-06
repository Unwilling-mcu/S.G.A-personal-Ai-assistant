import requests
import logging
from typing import Optional, Callable

logger = logging.getLogger(__name__)

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"
REQUEST_TIMEOUT = 30

HEADERS = {
    "User-Agent": "SGA-Assistant/1.0 (personal AI project; contact@localhost)"
}


def call_llm(prompt: str) -> str:
    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=REQUEST_TIMEOUT
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running — LLM unavailable")
        return ""
    except requests.exceptions.Timeout:
        logger.warning("Ollama timeout after %ds", REQUEST_TIMEOUT)
        return ""
    except Exception as e:
        logger.error("LLM call error: %s", e)
        return ""


def clean_query(q: str) -> str:
    """Clean query for Wikipedia search — do NOT add filler words."""
    q = q.lower().strip()
    # Remove only command words, keep the actual topic intact
    for word in ["search", "look up", "find", "tell me about",
                 "what is", "who is", "explain", "define", "about"]:
        if q.startswith(word):
            q = q[len(word):].strip()
    # Remove trailing filler
    q = q.strip(" .,?!")
    return q if q else "artificial intelligence"


def wiki_search(query: str) -> str:
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3
        }
        res = requests.get(search_url, params=params, headers=HEADERS, timeout=8)
        res.raise_for_status()

        results = res.json().get("query", {}).get("search", [])
        if not results:
            return ""

        title = results[0]["title"]
        logger.info("Wikipedia match: '%s'", title)

        summary_url = (
            f"https://en.wikipedia.org/api/rest_v1/page/summary/"
            f"{requests.utils.quote(title)}"
        )
        summary_res = requests.get(summary_url, headers=HEADERS, timeout=8)
        summary_res.raise_for_status()
        return summary_res.json().get("extract", "")

    except requests.exceptions.HTTPError as e:
        logger.error("Wikipedia HTTP error: %s", e)
        return ""
    except requests.exceptions.ConnectionError:
        logger.warning("No internet — Wikipedia unavailable")
        return ""
    except Exception as e:
        logger.error("Wiki search error: %s", e)
        return ""


def ddg_search(query: str) -> str:
    try:
        res = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            headers=HEADERS,
            timeout=8
        )
        res.raise_for_status()
        data = res.json()
        text = data.get("AbstractText", "").strip()
        if text:
            return text
        topics = data.get("RelatedTopics", [])
        if topics and isinstance(topics[0], dict):
            return topics[0].get("Text", "")
        return ""
    except Exception as e:
        logger.error("DuckDuckGo search error: %s", e)
        return ""


def get_web_answer(query: str, broadcast: Optional[Callable] = None) -> str:
    query = clean_query(query)
    logger.info("Web answer query: '%s'", query)

    _broadcast_step(broadcast, "Searching knowledge base...")

    content = wiki_search(query)

    if not content:
        logger.info("Wikipedia empty — trying DuckDuckGo")
        _broadcast_step(broadcast, "Trying alternative sources...")
        content = ddg_search(query)

    if not content:
        return (
            "I couldn't find reliable information on that topic. "
            "Try rephrasing or asking something more specific."
        )

    _broadcast_step(broadcast, "Generating answer...")

    summary = call_llm(
        f"Summarise the following in 2-3 clear, friendly sentences:\n\n{content[:1500]}"
    )

    return summary if summary else (content[:400].strip() + ("..." if len(content) > 400 else ""))


def _broadcast_step(broadcast: Optional[Callable], step: str):
    if broadcast:
        try:
            broadcast({"type": "thinking", "step": step})
        except Exception:
            pass