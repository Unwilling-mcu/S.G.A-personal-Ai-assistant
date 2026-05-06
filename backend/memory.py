"""
memory.py — SQLite-backed memory (replaces fragile JSON file).
Much faster, thread-safe, survives crashes, supports search.
"""
import sqlite3
import threading
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

DB_PATH  = "sga_memory.db"
MAX_KEEP = 200
_lock    = threading.Lock()


def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with _lock:
        conn = _get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                user     TEXT,
                ai       TEXT,
                intent   TEXT,
                actions  TEXT,
                ts       DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                task     TEXT NOT NULL,
                done     INTEGER DEFAULT 0,
                ts       DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

_init_db()


# ── Conversation memory ───────────────────────────────────────────────────────

def save_memory(user: str, ai: str, intent: str, actions: list):
    with _lock:
        conn = _get_conn()
        try:
            conn.execute(
                "INSERT INTO memory (user, ai, intent, actions) VALUES (?,?,?,?)",
                (user, ai, intent, ",".join(actions) if actions else "")
            )
            # Keep only last MAX_KEEP rows
            conn.execute(f"""
                DELETE FROM memory WHERE id NOT IN (
                    SELECT id FROM memory ORDER BY id DESC LIMIT {MAX_KEEP}
                )
            """)
            conn.commit()
        finally:
            conn.close()


def load_memory() -> list:
    with _lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT user, ai, intent, actions FROM memory ORDER BY id DESC LIMIT 50"
            ).fetchall()
            return [{"user": r["user"], "ai": r["ai"],
                     "intent": r["intent"],
                     "actions": r["actions"].split(",") if r["actions"] else []}
                    for r in reversed(rows)]
        finally:
            conn.close()


def get_last_command() -> Optional[dict]:
    with _lock:
        conn = _get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM memory ORDER BY id DESC LIMIT 1"
            ).fetchone()
            if row:
                return {"user": row["user"], "ai": row["ai"],
                        "intent": row["intent"],
                        "actions": row["actions"].split(",") if row["actions"] else []}
            return None
        finally:
            conn.close()


def get_most_used_intent() -> str:
    with _lock:
        conn = _get_conn()
        try:
            row = conn.execute(
                "SELECT intent, COUNT(*) as c FROM memory GROUP BY intent ORDER BY c DESC LIMIT 1"
            ).fetchone()
            return row["intent"] if row else "unknown"
        finally:
            conn.close()


def get_recent_context(n: int = 5) -> list:
    with _lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT user, ai, intent FROM memory ORDER BY id DESC LIMIT ?", (n,)
            ).fetchall()
            return [{"user": r["user"], "ai": r["ai"], "intent": r["intent"]}
                    for r in reversed(rows)]
        finally:
            conn.close()


def search_memory(query: str) -> list:
    """Search past conversations for a keyword."""
    with _lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT user, ai FROM memory WHERE user LIKE ? OR ai LIKE ? LIMIT 5",
                (f"%{query}%", f"%{query}%")
            ).fetchall()
            return [{"user": r["user"], "ai": r["ai"]} for r in rows]
        finally:
            conn.close()


def clear_memory():
    with _lock:
        conn = _get_conn()
        try:
            conn.execute("DELETE FROM memory")
            conn.commit()
            logger.info("Memory cleared")
        finally:
            conn.close()


# ── Task / To-do list ─────────────────────────────────────────────────────────

def add_task(task: str) -> str:
    if not task or not task.strip():
        return "No task given"
    with _lock:
        conn = _get_conn()
        try:
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (task.strip(),))
            conn.commit()
            return f"Task added: {task.strip()}"
        finally:
            conn.close()


def list_tasks() -> str:
    with _lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT id, task, done FROM tasks ORDER BY done ASC, id DESC"
            ).fetchall()
            if not rows:
                return "You have no tasks, Sir."
            pending   = [r for r in rows if not r["done"]]
            completed = [r for r in rows if r["done"]]
            result = ""
            if pending:
                result += "Pending: " + "; ".join(f"{r['id']}. {r['task']}" for r in pending)
            if completed:
                result += (" Done: " if result else "Done: ") + \
                           "; ".join(f"{r['task']}" for r in completed[:3])
            return result or "No tasks."
        finally:
            conn.close()


def complete_task(identifier: str) -> str:
    """Mark task done by ID number or partial name."""
    if not identifier:
        return "Which task?"
    with _lock:
        conn = _get_conn()
        try:
            # Try by ID
            if identifier.strip().isdigit():
                conn.execute("UPDATE tasks SET done=1 WHERE id=?", (int(identifier),))
            else:
                conn.execute("UPDATE tasks SET done=1 WHERE task LIKE ? AND done=0",
                             (f"%{identifier}%",))
            conn.commit()
            return f"Task marked as done."
        finally:
            conn.close()


def delete_task(identifier: str) -> str:
    if not identifier:
        return "Which task to delete?"
    with _lock:
        conn = _get_conn()
        try:
            if identifier.strip().isdigit():
                conn.execute("DELETE FROM tasks WHERE id=?", (int(identifier),))
            else:
                conn.execute("DELETE FROM tasks WHERE task LIKE ?", (f"%{identifier}%",))
            conn.commit()
            return "Task deleted."
        finally:
            conn.close()


def clear_completed_tasks() -> str:
    with _lock:
        conn = _get_conn()
        try:
            conn.execute("DELETE FROM tasks WHERE done=1")
            conn.commit()
            return "Completed tasks cleared."
        finally:
            conn.close()