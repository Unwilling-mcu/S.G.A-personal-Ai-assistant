import React, { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * VoiceOrb — the floating Alexa-style corner widget.
 *
 * States:
 *   idle      → small pulsing dot, barely visible
 *   wake      → orb expands with ripple (wake word detected)
 *   listening → animated ring, waiting for command
 *   thinking  → spinning arc + step text
 *   speaking  → bouncing waveform bars
 */
function VoiceOrb({ state, thinkingStep, lastWords }) {
  const SIZE = {
    idle:      52,
    wake:      72,
    listening: 80,
    thinking:  80,
    speaking:  80,
  };

  const ORB_COLOR = {
    idle:      "rgba(0,255,225,0.25)",
    wake:      "#00ffe1",
    listening: "#00ffe1",
    thinking:  "#ffaa00",
    speaking:  "#00ccff",
  };

  const GLOW = {
    idle:      "0 0 12px rgba(0,255,225,0.15)",
    wake:      "0 0 40px #00ffe1, 0 0 80px rgba(0,255,225,0.3)",
    listening: "0 0 30px #00ffe1",
    thinking:  "0 0 30px #ffaa00",
    speaking:  "0 0 30px #00ccff",
  };

  const size = SIZE[state] || 52;

  return (
    <div style={styles.wrapper}>
      {/* Ripple rings on wake */}
      <AnimatePresence>
        {(state === "wake" || state === "listening") && (
          <>
            {[1, 2, 3].map((i) => (
              <motion.div
                key={i}
                initial={{ scale: 0.8, opacity: 0.6 }}
                animate={{ scale: 2.5, opacity: 0 }}
                exit={{ opacity: 0 }}
                transition={{ repeat: Infinity, duration: 1.8, delay: i * 0.4, ease: "easeOut" }}
                style={{
                  ...styles.ripple,
                  width: size, height: size,
                  borderColor: ORB_COLOR[state],
                }}
              />
            ))}
          </>
        )}
      </AnimatePresence>

      {/* Main orb */}
      <motion.div
        animate={{
          width: size, height: size,
          background: ORB_COLOR[state],
          boxShadow: GLOW[state],
          scale: state === "speaking" ? [1, 1.08, 1] : 1,
        }}
        transition={{
          width: { duration: 0.3 },
          height: { duration: 0.3 },
          scale: { repeat: Infinity, duration: 0.5 },
          background: { duration: 0.3 },
        }}
        style={styles.orb}
      >
        {/* Inner icon by state */}
        {state === "idle" && <span style={styles.icon}>●</span>}
        {state === "wake"  && <span style={{ ...styles.icon, fontSize: 22 }}>◉</span>}
        {state === "listening" && <MicIcon />}
        {state === "thinking"  && <SpinnerIcon />}
        {state === "speaking"  && <WaveIcon />}
      </motion.div>

      {/* Caption bubble */}
      <AnimatePresence>
        {state !== "idle" && (
          <motion.div
            initial={{ opacity: 0, y: 8, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.9 }}
            transition={{ duration: 0.2 }}
            style={styles.caption}
          >
            {state === "wake"      && "Yes, Sir?"}
            {state === "listening" && "Listening..."}
            {state === "thinking"  && (thinkingStep || "Processing...")}
            {state === "speaking"  && (lastWords ? `"${lastWords}"` : "Speaking...")}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function MicIcon() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#02040a" strokeWidth="2.5">
      <rect x="9" y="2" width="6" height="12" rx="3" />
      <path d="M5 10a7 7 0 0 0 14 0" />
      <line x1="12" y1="17" x2="12" y2="22" />
      <line x1="8"  y1="22" x2="16" y2="22" />
    </svg>
  );
}

function SpinnerIcon() {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
      style={{ width: 24, height: 24, border: "3px solid #02040a",
               borderTopColor: "transparent", borderRadius: "50%" }}
    />
  );
}

function WaveIcon() {
  const bars = [0.4, 0.9, 0.6, 1, 0.7, 0.85, 0.5];
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 2 }}>
      {bars.map((h, i) => (
        <motion.div
          key={i}
          animate={{ scaleY: [h, 1, h * 0.6, h] }}
          transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.07 }}
          style={{
            width: 3, height: 18, background: "#02040a",
            borderRadius: 2, transformOrigin: "center",
          }}
        />
      ))}
    </div>
  );
}

const styles = {
  wrapper: {
    position: "fixed",
    bottom: 28,
    right: 28,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 10,
    zIndex: 9999,
  },
  orb: {
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    position: "relative",
  },
  ripple: {
    position: "absolute",
    borderRadius: "50%",
    border: "2px solid",
    pointerEvents: "none",
  },
  caption: {
    background: "rgba(2,4,10,0.92)",
    border: "1px solid #00ffe1",
    borderRadius: 20,
    padding: "6px 14px",
    fontSize: 12,
    color: "#00ffe1",
    fontFamily: "'Courier New', monospace",
    letterSpacing: 1,
    maxWidth: 220,
    textAlign: "center",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
  },
  icon: {
    color: "#02040a",
    fontSize: 16,
    lineHeight: 1,
  },
};

export default VoiceOrb;