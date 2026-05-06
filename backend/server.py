import asyncio
import threading
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.auth import authenticate
from backend.voice_loop import start_voice_loop
from backend.connection import add_connection, remove_connection, set_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting S.G.A...")
    set_loop(asyncio.get_running_loop())

    if not authenticate():
        logger.critical("❌ Authentication failed — shutting down")
        raise SystemExit(1)

    voice_thread = threading.Thread(
        target=start_voice_loop, daemon=True, name="VoiceLoop"
    )
    voice_thread.start()
    logger.info("🎤 Voice loop started (thread: %s)", voice_thread.name)
    logger.info("✅ S.G.A is now active!")

    yield

    logger.info("🛑 S.G.A shutting down cleanly")


app = FastAPI(title="S.G.A Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "S.G.A"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await add_connection(websocket)
    try:
        while True:
            try:
                # Use wait_for so CancelledError on shutdown is caught gracefully
                await asyncio.wait_for(asyncio.sleep(15), timeout=16)
                await websocket.send_json({"type": "keepalive"})
            except asyncio.TimeoutError:
                pass   # normal, just loop
            except asyncio.CancelledError:
                break  # server shutting down — exit cleanly, no traceback
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.debug("WebSocket closed: %s", e)
    finally:
        remove_connection(websocket)