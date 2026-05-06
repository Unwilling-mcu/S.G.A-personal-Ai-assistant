import React from "react";

/**
 * TitleBar — Custom window controls for the frameless Electron window.
 * Only renders when running inside Electron (window.electronAPI exists).
 */
function TitleBar() {
  // Don't render in browser (only in Electron)
  const isElectron = typeof window !== "undefined" && window.electronAPI?.isElectron;
  if (!isElectron) return null;

  return (
    <div style={styles.bar}>
      <span style={styles.appName}>⚡ S.G.A</span>
      <div style={styles.controls}>
        <button style={styles.btn} onClick={() => window.electronAPI.minimize()} title="Minimise">─</button>
        <button style={styles.btn} onClick={() => window.electronAPI.maximize()} title="Maximise">□</button>
        <button style={{ ...styles.btn, ...styles.closeBtn }} onClick={() => window.electronAPI.close()} title="Close">✕</button>
      </div>
    </div>
  );
}

const styles = {
  bar: {
    position:       "fixed",
    top:            0,
    left:           0,
    right:          0,
    height:         36,
    background:     "rgba(2,4,10,0.95)",
    borderBottom:   "1px solid rgba(0,255,225,0.15)",
    display:        "flex",
    alignItems:     "center",
    justifyContent: "space-between",
    paddingLeft:    14,
    zIndex:         99999,
    WebkitAppRegion: "drag",    // makes bar draggable like a real window
    userSelect:     "none",
  },
  appName: {
    color:       "#00ffe1",
    fontSize:    12,
    letterSpacing: 3,
    fontFamily:  "'Courier New', monospace",
  },
  controls: {
    display:         "flex",
    WebkitAppRegion: "no-drag",  // buttons must NOT be draggable
  },
  btn: {
    background:   "transparent",
    border:       "none",
    color:        "rgba(0,255,225,0.6)",
    fontSize:     14,
    width:        46,
    height:       36,
    cursor:       "pointer",
    transition:   "background 0.15s, color 0.15s",
    fontFamily:   "monospace",
  },
  closeBtn: {
    color: "rgba(255,80,80,0.7)",
  },
};

export default TitleBar;