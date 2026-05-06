import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const GESTURE_ICONS = {
  fist:        { icon: "✊", label: "Grab",        color: "#ff6b6b" },
  open_palm:   { icon: "✋", label: "Pause",       color: "#ffaa00" },
  pinch:       { icon: "🤏", label: "Click",       color: "#00ffe1" },
  point:       { icon: "☝️",  label: "Move cursor", color: "#00ccff" },
  peace:       { icon: "✌️",  label: "Scroll",      color: "#aa88ff" },
  thumbs_up:   { icon: "👍", label: "Volume ↑",    color: "#88ffaa" },
  thumbs_down: { icon: "👎", label: "Volume ↓",    color: "#ff8888" },
  five:        { icon: "🖐️",  label: "Screenshot",  color: "#ffdd44" },
};

function GestureOverlay({ lastGesture, gestureActive }) {
  const [tracePoints, setTracePoints] = useState([]);
  const [showGuide, setShowGuide]     = useState(false);
  const canvasRef = useRef(null);

  // Draw trace on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (tracePoints.length < 2) return;
    ctx.beginPath();
    ctx.strokeStyle = "#00ffe1";
    ctx.lineWidth   = 2;
    ctx.lineCap     = "round";
    ctx.lineJoin    = "round";
    ctx.shadowBlur  = 8;
    ctx.shadowColor = "#00ffe1";
    ctx.moveTo(tracePoints[0].x, tracePoints[0].y);
    tracePoints.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.stroke();
  }, [tracePoints]);

  const info = lastGesture ? GESTURE_ICONS[lastGesture] : null;

  return (
    <>
      {/* Gesture indicator badge */}
      <AnimatePresence>
        {info && gestureActive && (
          <motion.div
            initial={{ opacity: 0, scale: 0.7, y: 20 }}
            animate={{ opacity: 1, scale: 1,   y: 0  }}
            exit={{    opacity: 0, scale: 0.7, y: 20  }}
            transition={{ duration: 0.2 }}
            style={{
              position: "fixed", bottom: 120, right: 28,
              background: "rgba(2,4,10,0.92)",
              border: `1px solid ${info.color}`,
              borderRadius: 12, padding: "10px 16px",
              display: "flex", alignItems: "center", gap: 10,
              boxShadow: `0 0 20px ${info.color}40`,
              fontFamily: "'Courier New', monospace",
              zIndex: 9998,
            }}
          >
            <span style={{ fontSize: 24 }}>{info.icon}</span>
            <div>
              <div style={{ color: info.color, fontSize: 12, letterSpacing: 2 }}>
                GESTURE
              </div>
              <div style={{ color: "#fff", fontSize: 13, fontWeight: 500 }}>
                {info.label}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Gesture guide button */}
      <button
        onClick={() => setShowGuide(s => !s)}
        style={{
          position: "fixed", bottom: 28, left: 28,
          background: "transparent",
          border: "1px solid rgba(0,255,225,0.3)",
          borderRadius: 8, padding: "6px 12px",
          color: "rgba(0,255,225,0.6)",
          fontFamily: "'Courier New', monospace",
          fontSize: 11, letterSpacing: 1,
          cursor: "pointer", zIndex: 9998,
        }}
      >
        ✋ GESTURES
      </button>

      {/* Gesture guide panel */}
      <AnimatePresence>
        {showGuide && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0  }}
            exit={{    opacity: 0, x: -20 }}
            style={{
              position: "fixed", bottom: 70, left: 28,
              background: "rgba(2,4,10,0.96)",
              border: "1px solid rgba(0,255,225,0.3)",
              borderRadius: 12, padding: 16, minWidth: 200,
              fontFamily: "'Courier New', monospace",
              zIndex: 9997,
            }}
          >
            <div style={{ color: "#00ffe1", fontSize: 11, letterSpacing: 2, marginBottom: 12 }}>
              GESTURE REFERENCE
            </div>
            {Object.entries(GESTURE_ICONS).map(([key, val]) => (
              <div key={key} style={{ display:"flex", gap:10, marginBottom:6, alignItems:"center" }}>
                <span style={{ fontSize:18, width:24, textAlign:"center" }}>{val.icon}</span>
                <span style={{ color: val.color, fontSize:11, letterSpacing:1 }}>{val.label}</span>
              </div>
            ))}
            <div style={{ marginTop:10, paddingTop:8,
                          borderTop:"1px solid rgba(0,255,225,0.1)",
                          color:"rgba(0,255,225,0.4)", fontSize:10, lineHeight:1.6 }}>
              Say "enable gesture control" to activate
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default GestureOverlay;