"""
browser_agent.py — Real web browsing using Playwright.
S.G.A can open websites, click buttons, search, and extract info.
Install: pip install playwright && playwright install chromium
"""
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)


def _check_playwright() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        return False


def browse_and_answer(task: str, broadcast=None) -> str:
    """
    Use Playwright to browse the web and complete a task.
    Examples:
      - "Go to Amazon and find headphones under 500 rupees"
      - "Check the weather on timesofindia.com"
      - "Search YouTube for Python tutorials"
    """
    if not _check_playwright():
        return "Browser agent requires Playwright. Run: pip install playwright && playwright install chromium"

    if broadcast:
        try: broadcast({"type": "thinking", "step": "Opening browser..."})
        except Exception: pass

    try:
        from playwright.sync_api import sync_playwright
        import os
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)   # visible browser
            page    = browser.new_page()
            page.set_default_timeout(15000)

            result = _execute_task(page, task, broadcast)
            browser.close()
            return result

    except Exception as e:
        logger.error("Browser agent error: %s", e)
        return f"Browser task failed: {e}"


def _execute_task(page, task: str, broadcast) -> str:
    """Execute a browser task step by step."""
    t = task.lower()

    def _broadcast(step):
        if broadcast:
            try: broadcast({"type": "thinking", "step": step})
            except Exception: pass

    # YouTube search
    if "youtube" in t:
        query = t.replace("youtube","").replace("search","").replace("on","").strip()
        _broadcast("Opening YouTube...")
        page.goto("https://www.youtube.com")
        page.fill('input[name="search_query"]', query)
        page.press('input[name="search_query"]', "Enter")
        page.wait_for_load_state("networkidle")
        # Get first 5 video titles
        titles = page.locator("ytd-video-renderer #video-title").all_text_contents()[:5]
        if titles:
            return "Top YouTube results: " + "; ".join(t.strip() for t in titles if t.strip())
        return "YouTube search completed."

    # Amazon search
    if "amazon" in t:
        query = t.replace("amazon","").replace("search","").replace("find","").replace("on","").strip()
        _broadcast("Searching Amazon...")
        page.goto("https://www.amazon.in")
        page.fill('input[name="field-keywords"]', query)
        page.press('input[name="field-keywords"]', "Enter")
        page.wait_for_load_state("networkidle")
        # Get first 3 products
        items = page.locator('[data-component-type="s-search-result"] h2 span').all_text_contents()[:3]
        prices = page.locator('[data-component-type="s-search-result"] .a-price-whole').all_text_contents()[:3]
        if items:
            results = []
            for i, item in enumerate(items):
                price = f"₹{prices[i]}" if i < len(prices) else "price unknown"
                results.append(f"{item.strip()} — {price}")
            return "Amazon results: " + "; ".join(results)
        return "Amazon search completed."

    # Google search
    if "google" in t or "search" in t:
        query = t.replace("google","").replace("search","").replace("for","").strip()
        _broadcast("Searching Google...")
        page.goto(f"https://www.google.com/search?q={query}")
        page.wait_for_load_state("networkidle")
        # Extract featured snippet or first results
        try:
            snippet = page.locator(".hgKElc, .LGOjhe, .kno-rdesc span").first.text_content()
            if snippet and len(snippet) > 20:
                return f"Google says: {snippet[:400]}"
        except Exception: pass
        results = page.locator("h3").all_text_contents()[:3]
        if results:
            return "Top results: " + "; ".join(r.strip() for r in results if r.strip())
        return "Google search completed."

    # Generic: just navigate and extract page text
    if "go to " in t or "open " in t or "visit " in t:
        import re
        m = re.search(r"(?:go to|open|visit)\s+([\w\.\-]+(?:\.[a-z]{2,}))", t)
        url = m.group(1) if m else task
        if not url.startswith("http"): url = "https://" + url
        _broadcast(f"Opening {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        # Extract main text
        try:
            body = page.inner_text("body")[:500]
            return f"Page loaded: {body.strip()}"
        except Exception:
            return f"Opened {url}"

    return f"Browser task '{task}' completed."


def web_search_and_extract(query: str, broadcast=None) -> str:
    """Search Google and extract actual content from the first result."""
    if not _check_playwright():
        return ""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # headless for search
            page    = browser.new_page()
            page.goto(f"https://www.google.com/search?q={query}", timeout=10000)
            page.wait_for_load_state("networkidle")

            # Try featured snippet first
            try:
                snippet = page.locator(".hgKElc, .LGOjhe, .kno-rdesc span").first.text_content()
                if snippet and len(snippet) > 30:
                    browser.close()
                    return snippet[:600]
            except Exception: pass

            # Get first organic result URL and scrape it
            try:
                first_link = page.locator("h3").first
                first_link.click()
                page.wait_for_load_state("networkidle")
                text = page.inner_text("body")
                browser.close()
                # Clean up
                import re
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:600]
            except Exception:
                browser.close()
                return ""
    except Exception as e:
        logger.error("Web extract error: %s", e)
        return ""
