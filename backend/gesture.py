import logging

logger = logging.getLogger(__name__)


def start_gesture():
    """Start gesture detection loop (runs in its own thread)."""
    try:
        import cv2
        import mediapipe as mp
    except ImportError as e:
        logger.warning("Gesture detection unavailable: %s", e)
        return

    hands_detector = mp.solutions.hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    cam = None

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logger.warning("Camera unavailable for gesture detection")
            return

        logger.info("✋ Gesture detection started")

        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands_detector.process(rgb)

            if results.multi_hand_landmarks:
                logger.debug("Gesture detected: %d hand(s)", len(results.multi_hand_landmarks))
                # TODO: Add gesture command mapping here

            cv2.imshow("S.G.A Gesture", frame)
            if cv2.waitKey(1) & 0xFF == 27:   # ESC to quit
                break

    except Exception as e:
        logger.error("Gesture detection error: %s", e)

    finally:
        if cam is not None:
            cam.release()
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        try:
            hands_detector.close()
        except Exception:
            pass
        logger.info("Gesture detection stopped")