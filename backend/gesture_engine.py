"""
gesture_engine.py — Hand gesture control using MediaPipe Tasks API (v0.10+).

Gestures:
  ✊ FIST        → grab/select
  ✋ OPEN_PALM   → pause S.G.A
  🤏 PINCH       → click
  ☝️  POINT       → move mouse cursor
  ✌️  PEACE       → scroll
  👍 THUMBS_UP   → volume up
  👎 THUMBS_DOWN → volume down
  🖐️  FIVE        → screenshot
"""
import cv2
import threading
import logging
import time
import math
import os
import urllib.request

logger = logging.getLogger(__name__)

# Gesture names
FIST        = "fist"
OPEN_PALM   = "open_palm"
PINCH       = "pinch"
POINT       = "point"
PEACE       = "peace"
THUMBS_UP   = "thumbs_up"
THUMBS_DOWN = "thumbs_down"
FIVE        = "five"
NONE        = "none"

_running         = False
_last_gesture    = NONE
_gesture_lock    = threading.Lock()
_on_gesture_cb   = None
_trace_points    = []
_tracing_enabled = False

# MediaPipe model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")
MODEL_URL  = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"


def set_gesture_callback(fn):
    global _on_gesture_cb
    _on_gesture_cb = fn

def enable_tracing(enabled: bool):
    global _tracing_enabled, _trace_points
    _tracing_enabled = enabled
    if not enabled:
        _trace_points = []

def get_trace_points():
    return list(_trace_points)

def stop():
    global _running
    _running = False


def _download_model():
    """Download the MediaPipe hand landmarker model if not present."""
    if os.path.exists(MODEL_PATH):
        return True
    try:
        logger.info("Downloading MediaPipe hand model (~30MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        logger.info("Model downloaded: %s", MODEL_PATH)
        return True
    except Exception as e:
        logger.error("Model download failed: %s", e)
        return False


def _dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def _finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y

def _classify(landmarks) -> str:
    lm = landmarks
    thumb_ext  = lm[4].x < lm[3].x   # right hand: tip left of knuckle
    index_ext  = _finger_up(lm, 8,  6)
    middle_ext = _finger_up(lm, 12, 10)
    ring_ext   = _finger_up(lm, 16, 14)
    pinky_ext  = _finger_up(lm, 20, 18)
    n_up = sum([index_ext, middle_ext, ring_ext, pinky_ext])

    if _dist(lm[4], lm[8]) < 0.06:
        return PINCH
    if index_ext and middle_ext and not ring_ext and not pinky_ext:
        return PEACE
    if index_ext and not middle_ext and not ring_ext and not pinky_ext:
        return POINT
    if n_up == 0:
        return THUMBS_UP if thumb_ext else FIST
    if n_up == 4:
        return FIVE
    if n_up >= 3:
        return OPEN_PALM
    return NONE


def _execute(gesture: str, lm, frame_shape):
    global _last_gesture, _trace_points
    with _gesture_lock:
        if gesture == _last_gesture:
            return
        _last_gesture = gesture
    if gesture == NONE:
        return

    logger.info("✋ Gesture: %s", gesture)

    try:
        import pyautogui
        pyautogui.FAILSAFE = False
        sw, sh = pyautogui.size()
        h, w   = frame_shape[:2]

        if gesture == POINT:
            x = int(lm[8].x * sw)
            y = int(lm[8].y * sh)
            pyautogui.moveTo(x, y, duration=0.05)
            if _tracing_enabled:
                _trace_points.append((x, y))
                if len(_trace_points) > 200:
                    _trace_points.pop(0)
        elif gesture == PINCH:
            pyautogui.click()
        elif gesture == THUMBS_UP:
            for _ in range(3): pyautogui.press("volumeup")
        elif gesture == THUMBS_DOWN:
            for _ in range(3): pyautogui.press("volumedown")
        elif gesture == FIVE:
            from backend.action_engine import take_screenshot
            take_screenshot()
        elif gesture == OPEN_PALM:
            from backend.connection import broadcast
            broadcast({"type": "gesture", "gesture": "pause"})
    except ImportError:
        pass
    except Exception as e:
        logger.error("Gesture action error: %s", e)

    if _on_gesture_cb:
        try: _on_gesture_cb(gesture, lm)
        except Exception: pass

    try:
        from backend.connection import broadcast
        broadcast({"type": "gesture", "gesture": gesture})
    except Exception:
        pass


def _run_with_tasks_api(show_window: bool):
    """Use MediaPipe Tasks API (v0.10+) — the correct modern approach."""
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision as mp_vision
    except (ImportError, AttributeError) as e:
        logger.error("MediaPipe Tasks API unavailable: %s", e)
        return False

    if not _download_model():
        return False

    try:
        base_opts = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        opts = mp_vision.HandLandmarkerOptions(
            base_options=base_opts,
            running_mode=mp_vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.6
        )
        landmarker = mp_vision.HandLandmarker.create_from_options(opts)
    except Exception as e:
        logger.error("HandLandmarker init failed: %s", e)
        return False

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        logger.warning("Camera not available")
        landmarker.close()
        return False

    global _running
    _running = True
    logger.info("✋ Gesture engine started (Tasks API)")
    ts_ms = 0

    try:
        while _running:
            ret, frame = cam.read()
            if not ret:
                time.sleep(0.03)
                continue

            frame = cv2.flip(frame, 1)
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ts_ms += 33  # ~30fps timestamp

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result   = landmarker.detect_for_video(mp_image, ts_ms)

            if result.hand_landmarks:
                lm = result.hand_landmarks[0]
                gesture = _classify(lm)
                _execute(gesture, lm, frame.shape)

                if show_window:
                    # Draw landmarks manually
                    h, w = frame.shape[:2]
                    for point in lm:
                        cx, cy = int(point.x * w), int(point.y * h)
                        cv2.circle(frame, (cx, cy), 4, (0, 255, 225), -1)

                    # Draw trace
                    if _tracing_enabled and len(_trace_points) > 1:
                        for i in range(1, min(len(_trace_points), 50)):
                            p1 = (_trace_points[-i][0] % w, _trace_points[-i][1] % h)
                            p2 = (_trace_points[-(i+1)][0] % w, _trace_points[-(i+1)][1] % h)
                            cv2.line(frame, p1, p2, (0, 255, 225), 2)
            else:
                with _gesture_lock:
                    _last_gesture = NONE

            if show_window:
                cv2.putText(frame, f"Gesture: {_last_gesture}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 225), 2)
                cv2.imshow("S.G.A Gesture Control — ESC to close", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            time.sleep(0.02)

    except Exception as e:
        logger.error("Gesture loop error: %s", e)
    finally:
        _running = False
        landmarker.close()
        cam.release()
        try: cv2.destroyAllWindows()
        except Exception: pass
        logger.info("Gesture engine stopped")

    return True


def _run_with_solutions_api(show_window: bool):
    """Fallback: try old mediapipe.solutions API (v0.9 and below)."""
    try:
        import mediapipe as mp
        hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.6
        )
        draw = mp.solutions.drawing_utils
    except Exception as e:
        logger.error("Solutions API also failed: %s", e)
        return False

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        hands.close(); return False

    global _running
    _running = True
    logger.info("✋ Gesture engine started (solutions API fallback)")

    try:
        while _running:
            ret, frame = cam.read()
            if not ret: time.sleep(0.03); continue
            frame   = cv2.flip(frame, 1)
            rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hlm in results.multi_hand_landmarks:
                    gesture = _classify(hlm.landmark)
                    _execute(gesture, hlm.landmark, frame.shape)
                    if show_window:
                        draw.draw_landmarks(frame, hlm, mp.solutions.hands.HAND_CONNECTIONS)
            else:
                with _gesture_lock: _last_gesture = NONE

            if show_window:
                cv2.putText(frame, f"Gesture: {_last_gesture}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 225), 2)
                cv2.imshow("S.G.A Gesture Control — ESC to close", frame)
                if cv2.waitKey(1) & 0xFF == 27: break
            time.sleep(0.02)
    finally:
        _running = False
        hands.close(); cam.release()
        try: cv2.destroyAllWindows()
        except Exception: pass
    return True


def start_gesture_engine(show_window: bool = True):
    """Try Tasks API first, fall back to solutions API."""
    try:
        import mediapipe
        version = tuple(int(x) for x in mediapipe.__version__.split(".")[:2])
        logger.info("MediaPipe version: %s", mediapipe.__version__)

        if version >= (0, 10):
            if not _run_with_tasks_api(show_window):
                _run_with_solutions_api(show_window)
        else:
            _run_with_solutions_api(show_window)
    except ImportError:
        logger.error("MediaPipe not installed. Run: pip install mediapipe opencv-python")
    except Exception as e:
        logger.error("Gesture engine error: %s", e)


def start_gesture_thread(show_window: bool = True):
    t = threading.Thread(
        target=start_gesture_engine,
        args=(show_window,),
        daemon=True,
        name="GestureEngine"
    )
    t.start()
    return t