import asyncio
import json
import logging

logger = logging.getLogger(__name__)

active_connections: set = set()
_main_loop: asyncio.AbstractEventLoop | None = None


def set_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop
    logger.info("Event loop registered in connection manager")


async def _prune_dead_connections():
    """Eagerly remove WebSocket objects that are no longer open."""
    dead = set()
    for ws in list(active_connections):
        try:
            # Starlette WebSocketState: 0=CONNECTING, 1=CONNECTED, 2=DISCONNECTED
            if ws.client_state.value >= 2:
                dead.add(ws)
        except Exception:
            dead.add(ws)
    for ws in dead:
        active_connections.discard(ws)
    if dead:
        logger.info("Pruned %d stale connection(s) (total now: %d)", len(dead), len(active_connections))


async def add_connection(websocket):
    await websocket.accept()
    await _prune_dead_connections()
    active_connections.add(websocket)
    logger.info("UI connected  (total: %d)", len(active_connections))


def remove_connection(websocket):
    active_connections.discard(websocket)
    logger.info("UI disconnected (total: %d)", len(active_connections))


async def _broadcast_async(message: dict):
    if not active_connections:
        return

    dead: set = set()
    payload = json.dumps(message)

    for ws in list(active_connections):
        try:
            await ws.send_text(payload)
        except Exception:
            dead.add(ws)

    for ws in dead:
        remove_connection(ws)


def broadcast(message: dict):
    """
    Thread-safe broadcast. Safe to call from any thread (voice loop, agent, etc.).
    """
    if _main_loop and _main_loop.is_running():
        asyncio.run_coroutine_threadsafe(_broadcast_async(message), _main_loop)
    else:
        logger.debug("broadcast skipped (no running loop): %s", message)