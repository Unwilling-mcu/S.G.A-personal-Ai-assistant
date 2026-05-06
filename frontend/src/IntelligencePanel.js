import React from "react";

const INTENT_COLORS = {
  search: "#00ffe1",
  open_app: "#00ccff",
  conversation: "#aa88ff",
  greeting: "#88ffaa",
  fallback: "#ffaa00",
  agent: "#00ffe1",
  clarification: "#ffdd00",
  unknown: "rgba(0,255,225,0.4)",
  empty: "rgba(0,255,225,0.4)",
};

function IntelligencePanel({ intent, actions, text }) {
  const color = INTENT_COLORS[intent] || INTENT_COLORS.unknown;

  return (
    <div style={styles.panel}>
      <h3 style={styles.heading}>🧠 AI INTELLIGENCE</h3>

      <div style={styles.row}>
        <span style={styles.key}>INTENT</span>
        <span style={{ ...styles.value, color }}>
          {intent || "—"}
        </span>
      </div>

      <div style={styles.row}>
        <span style={styles.key}>ACTIONS</span>
        <div style={styles.tags}>
          {actions && actions.length > 0 ? (
            actions.map((a, i) => (
              <span key={i} style={styles.tag}>{a}</span>
            ))
          ) : (
            <span style={styles.empty}>—</span>
          )}
        </div>
      </div>

      <div style={styles.row}>
        <span style={styles.key}>PARSED</span>
        <span style={styles.value}>{text || "—"}</span>
      </div>
    </div>
  );
}

const styles = {
  panel: {
    border: "1px solid #00ffe1",
    padding: "14px",
    borderRadius: "10px",
    boxShadow: "0 0 20px rgba(0,255,225,0.2)",
    background: "rgba(0,255,225,0.03)",
    fontFamily: "'Courier New', monospace",
  },
  heading: {
    margin: "0 0 14px 0",
    borderBottom: "1px solid rgba(0,255,225,0.3)",
    paddingBottom: "8px",
    fontSize: "13px",
    letterSpacing: "2px",
  },
  row: {
    display: "flex",
    flexDirection: "column",
    marginBottom: "12px",
    gap: "4px",
  },
  key: {
    fontSize: "10px",
    color: "rgba(0,255,225,0.4)",
    letterSpacing: "2px",
  },
  value: {
    fontSize: "13px",
    color: "#00ffe1",
    wordBreak: "break-word",
  },
  tags: {
    display: "flex",
    flexWrap: "wrap",
    gap: "6px",
  },
  tag: {
    fontSize: "11px",
    padding: "2px 8px",
    borderRadius: "20px",
    border: "1px solid #00ffe1",
    color: "#00ffe1",
    background: "rgba(0,255,225,0.07)",
    letterSpacing: "1px",
  },
  empty: {
    color: "rgba(0,255,225,0.3)",
    fontSize: "13px",
  },
};

export default IntelligencePanel;