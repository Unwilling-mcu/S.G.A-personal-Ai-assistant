"""
auth.py — Biometric face authentication using MediaPipe + OpenCV.

Setup:
  1. Take a clear photo of your face
  2. Save it as backend/reference.jpg
  3. Set face_auth_enabled=true in settings.json

Features:
  - Face detection via MediaPipe
  - Face similarity via face_recognition library (optional, better accuracy)
  - Fallback to presence-only detection
  - App-level access control (require re-auth for sensitive apps)
"""
import os
import cv2
import logging
import time

logger = logging.getLogger(__name__)

REFERENCE_PHOTO = os.path.join(os.path.dirname(__file__), "reference.jpg")
AUTH_TIMEOUT    = 30   # seconds to wait for face
MAX_FRAMES      = 900  # 30s at 30fps


def _try_face_recognition_auth() -> bool:
    """
    High-accuracy auth using face_recognition library.
    Compares live face to reference.jpg encoding.
    Install: pip install face-recognition
    """
    try:
        import face_recognition
        import numpy as np

        if not os.path.exists(REFERENCE_PHOTO):
            logger.warning("reference.jpg not found — falling back to presence detection")
            return None   # signal fallback

        logger.info("Loading reference face from %s", REFERENCE_PHOTO)
        ref_img      = face_recognition.load_image_file(REFERENCE_PHOTO)
        ref_encodings = face_recognition.face_encodings(ref_img)

        if not ref_encodings:
            logger.error("No face found in reference.jpg — retake the photo")
            return None

        ref_encoding = ref_encodings[0]

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logger.warning("Camera unavailable — granting access")
            return True

        logger.info("🔐 Face authentication starting (face_recognition mode)...")
        print("🔐 Look at the camera...")

        for _ in range(MAX_FRAMES):
            ret, frame = cam.read()
            if not ret: continue

            rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locs    = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, locs)

            for enc in encodings:
                dist = face_recognition.face_distance([ref_encoding], enc)[0]
                if dist < 0.55:   # 0.6 is default threshold, 0.55 is stricter
                    cam.release(); cv2.destroyAllWindows()
                    logger.info("✅ Face matched (distance=%.3f) — access granted", dist)
                    return True

            cv2.imshow("S.G.A — Face Authentication", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cam.release(); cv2.destroyAllWindows()
        logger.warning("❌ Face not matched")
        return False

    except ImportError:
        logger.info("face_recognition not installed — trying MediaPipe fallback")
        return None   # signal fallback
    except Exception as e:
        logger.error("face_recognition auth error: %s", e)
        return None


def _try_mediapipe_auth() -> bool:
    """
    Presence-only auth using MediaPipe FaceDetection.
    Not as secure as face_recognition but works without extra setup.
    """
    try:
        import mediapipe as mp
        mp_face = mp.solutions.face_detection
        detector = mp_face.FaceDetection(min_detection_confidence=0.7)
    except Exception as e:
        logger.warning("MediaPipe init failed (%s) — granting access", e)
        return True

    cam = None
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logger.warning("Camera unavailable — granting access")
            return True

        logger.info("🔐 Face authentication starting (presence mode)...")
        print("🔐 Look at the camera...")

        for _ in range(MAX_FRAMES):
            ret, frame = cam.read()
            if not ret: continue

            rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.process(rgb)

            if results.detections:
                logger.info("✅ Face detected — access granted")
                return True

            cv2.imshow("S.G.A — Face Authentication (any face)", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        logger.warning("❌ No face detected in time")
        return False

    except Exception as e:
        logger.error("MediaPipe auth error (%s) — granting access", e)
        return True
    finally:
        if cam: cam.release()
        try: cv2.destroyAllWindows()
        except Exception: pass
        try: detector.close()
        except Exception: pass


def authenticate() -> bool:
    """
    Main authentication function.
    Tries face_recognition (accurate) then MediaPipe (presence) then grants access.
    """
    from backend.settings import get
    if os.environ.get("SGA_SKIP_AUTH") == "1":
        logger.info("Auth skipped via SGA_SKIP_AUTH env var")
        return True

    if not get("face_auth_enabled", False):
        logger.info("Face auth disabled in settings — granting access")
        return True

    try:
        import cv2
    except ImportError:
        logger.warning("OpenCV not installed — granting access (pip install opencv-python)")
        return True

    # Try high-accuracy first
    result = _try_face_recognition_auth()
    if result is not None:
        return result

    # Fallback to presence detection
    return _try_mediapipe_auth()


# ── Per-app biometric access control ─────────────────────────────────────────

PROTECTED_APPS = {
    "banking apps": ["Edge", "Chrome"],
    "password manager": ["Bitwarden", "KeePass", "1Password"],
    "private files": ["Documents", "Downloads"],
}

_session_verified  = False
_session_timestamp = 0
SESSION_DURATION   = 300   # 5 minutes before requiring re-auth


def require_biometric_for_app(app_name: str) -> bool:
    """
    Returns True if the app can open (auth passed or not required).
    Call before launching any sensitive app.
    """
    global _session_verified, _session_timestamp
    from backend.settings import get

    if not get("face_auth_enabled", False):
        return True

    # Is this app protected?
    is_protected = any(
        app_name.lower() in [a.lower() for a in apps]
        for apps in PROTECTED_APPS.values()
    )
    if not is_protected:
        return True

    # Check session validity
    if _session_verified and (time.time() - _session_timestamp) < SESSION_DURATION:
        return True

    # Require fresh authentication
    logger.info("App '%s' requires biometric authentication", app_name)
    from backend.speaker import speak
    speak(f"Biometric authentication required to open {app_name}.")

    result = authenticate()
    if result:
        _session_verified  = True
        _session_timestamp = time.time()

    return result


def take_reference_photo():
    """
    Take a reference photo for face auth.
    Say 'take reference photo' or call this function.
    """
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return "Camera not available"

        from backend.speaker import speak
        speak("Please look at the camera. Taking photo in 3 seconds.")
        time.sleep(3)

        ret, frame = cam.read()
        cam.release()

        if ret:
            cv2.imwrite(REFERENCE_PHOTO, frame)
            logger.info("Reference photo saved to %s", REFERENCE_PHOTO)
            return f"Reference photo saved. Face authentication is ready."
        return "Failed to capture photo"

    except Exception as e:
        return f"Photo capture failed: {e}"